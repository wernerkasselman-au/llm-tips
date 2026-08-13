#!/usr/bin/env python3
"""Check a proposal packet against the High-Signal Proposal Triage contract.

Executes the hard gates that contract-declaration.toml declares: synopsis
presence and cap (REQ:synopsis), ownership attestation (REQ:ownership-present),
structural minimums (REQ:structure), and evidence-pack shape
(REQ:evidence-pack). REQ:high-signal stays with lint_writing_style.py, which
this tool can invoke with --lint-policy.

Thresholds are never hardcoded here. They are read from the triage DAG at run
time, and a DAG that does not state them unambiguously is an invocation error,
not a default. Requires Python 3.11+ (uses tomllib).

Exit codes match the linter: 0 clean, 1 violations, 2 invocation error.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parent.parent
DEFAULT_DAG = REPO_ROOT / "tools" / "proposal_triage_dag.toml"
LINTER = REPO_ROOT / "tools" / "lint_writing_style.py"

DOC_TYPES = ("design-doc", "rfc", "sad", "adr-lite")

# Heading sets per document type. Each entry is (label, alternatives).
STRUCTURE_REQUIREMENTS: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "design-doc": (
        ("Goals", ("goals",)),
        ("Non-goals", ("non-goals", "non goals", "nongoals")),
        ("Alternatives considered", ("alternatives considered", "alternatives")),
        ("Consequences or Impact", ("consequences", "impact", "impacted systems")),
    ),
    "adr-lite": (
        ("Context", ("context",)),
        ("Decision", ("decision",)),
        ("Consequences", ("consequences",)),
    ),
}
STRUCTURE_REQUIREMENTS["rfc"] = STRUCTURE_REQUIREMENTS["design-doc"]
STRUCTURE_REQUIREMENTS["sad"] = STRUCTURE_REQUIREMENTS["design-doc"]

# The four elements REQ:synopsis demands, as labelled lines.
SYNOPSIS_ELEMENTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("problem", ("problem",)),
    ("proposed action", ("proposed action", "proposal", "decision")),
    ("trade-off or impact", ("trade-off", "tradeoff", "impact")),
    ("ask", ("ask", "request")),
)

# The word "Rejected" anywhere in the Alternatives section satisfies the
# rejected-alternative rule. Anchoring this to line start was tried first and
# rejected: it forced authors to break a paragraph mid-thought to satisfy a
# regex, which is the kind of gate people route around rather than obey.
REJECTED_MARKER = re.compile(r"\brejected\b", re.IGNORECASE)


class InvocationError(Exception):
    """Raised for conditions that must fail closed rather than pass silently."""


@dataclass
class Violation:
    req_id: str
    message: str
    path: str | None = None


@dataclass
class Packet:
    proposal: Path
    synopsis: Path | None = None
    ownership: Path | None = None
    evidence_pack: Path | None = None
    doc_type: str = "design-doc"
    violations: list[Violation] = field(default_factory=list)


def load_linter_helpers() -> tuple:
    """Import word_count and strip_code_blocks from the shipped linter.

    Counting must agree with the linter exactly; reimplementing it here would
    create a second definition of "word" that could drift from the first.
    """
    if not LINTER.is_file():
        raise InvocationError(f"linter not found at {LINTER}")
    spec = importlib.util.spec_from_file_location("_hs_linter", LINTER)
    if spec is None or spec.loader is None:
        raise InvocationError(f"cannot load linter module from {LINTER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["_hs_linter"] = module
    spec.loader.exec_module(module)
    for attr in ("word_count", "strip_code_blocks", "strip_front_matter"):
        if not hasattr(module, attr):
            raise InvocationError(f"linter is missing {attr}(); cannot count consistently")
    return module.word_count, module.strip_code_blocks, module.strip_front_matter


def read_thresholds(dag_path: Path) -> tuple[int, int]:
    """Extract the synopsis trigger and cap from the DAG.

    Fails closed. A DAG that states no threshold, or states more than one, is an
    invocation error: guessing a default here would silently weaken the gate the
    tool exists to enforce.
    """
    if not dag_path.is_file():
        raise InvocationError(f"DAG not found: {dag_path}")
    text = dag_path.read_text(encoding="utf-8")
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise InvocationError(f"DAG does not parse as TOML: {exc}") from exc

    triggers = {int(m) for m in re.findall(r"[≥>]=?\s*(\d+)\s*words", text)}
    caps = {int(m) for m in re.findall(r"[≤<]=?\s*(\d+)\s*words", text)}

    if len(triggers) != 1:
        raise InvocationError(
            f"cannot read a single synopsis trigger from {dag_path}: found {sorted(triggers) or 'none'}"
        )
    if len(caps) != 1:
        raise InvocationError(
            f"cannot read a single synopsis cap from {dag_path}: found {sorted(caps) or 'none'}"
        )
    trigger, cap = triggers.pop(), caps.pop()
    if cap >= trigger:
        raise InvocationError(
            f"incoherent thresholds in {dag_path}: cap {cap} is not below trigger {trigger}"
        )
    return trigger, cap


def headings(text: str) -> list[str]:
    return [h.strip().strip("#").strip().lower() for h in re.findall(r"^#{1,6}\s+.*$", text, re.MULTILINE)]


def section_body(text: str, names: tuple[str, ...]) -> str | None:
    """Return the body under the first heading matching any of `names`."""
    lines = text.splitlines()
    start = None
    level = 0
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        title = m.group(2).strip().lower().rstrip(":")
        if start is None and any(title == n or title.startswith(n) for n in names):
            start, level = i + 1, len(m.group(1))
            continue
        if start is not None and len(m.group(1)) <= level:
            return "\n".join(lines[start:i])
    return "\n".join(lines[start:]) if start is not None else None


def check_structure(packet: Packet, text: str) -> None:
    required = STRUCTURE_REQUIREMENTS[packet.doc_type]
    present = headings(text)
    for label, names in required:
        if not any(any(h == n or h.startswith(n) for n in names) for h in present):
            packet.violations.append(
                Violation("REQ:structure", f"missing required section: {label}", str(packet.proposal))
            )
    if packet.doc_type != "adr-lite":
        body = section_body(text, ("alternatives considered", "alternatives"))
        if body is not None and not REJECTED_MARKER.search(body):
            packet.violations.append(
                Violation(
                    "REQ:structure",
                    "Alternatives section names no rejected alternative; "
                    "say which one you rejected and why",
                    str(packet.proposal),
                )
            )


def check_synopsis(packet: Packet, doc_words: int, trigger: int, cap: int, count_words, strip) -> None:
    if doc_words < trigger:
        return
    if packet.synopsis is None or not packet.synopsis.is_file():
        packet.violations.append(
            Violation(
                "REQ:synopsis",
                f"document is {doc_words} words (trigger {trigger}) and has no synopsis file",
                str(packet.proposal),
            )
        )
        return
    text = packet.synopsis.read_text(encoding="utf-8")
    words = count_words(strip(text))
    if words > cap:
        packet.violations.append(
            Violation("REQ:synopsis", f"synopsis is {words} words, cap is {cap}", str(packet.synopsis))
        )
    lowered = text.lower()
    for label, names in SYNOPSIS_ELEMENTS:
        if not any(re.search(rf"^\s*(?:[-*+]\s*)?(?:\*\*)?{re.escape(n)}\b\s*:?", lowered, re.MULTILINE) for n in names):
            packet.violations.append(
                Violation("REQ:synopsis", f"synopsis is missing a labelled '{label}' element", str(packet.synopsis))
            )


def check_ownership(packet: Packet) -> None:
    if packet.ownership is None or not packet.ownership.is_file():
        packet.violations.append(Violation("REQ:ownership-present", "no ownership attestation file"))
        return
    try:
        data = tomllib.loads(packet.ownership.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        packet.violations.append(
            Violation("REQ:ownership-present", f"attestation does not parse: {exc}", str(packet.ownership))
        )
        return
    att = data.get("attestation")
    if not isinstance(att, dict):
        packet.violations.append(
            Violation("REQ:ownership-present", "missing [attestation] table", str(packet.ownership))
        )
        return
    author = str(att.get("author", "")).strip()
    if not author:
        packet.violations.append(
            Violation("REQ:ownership-present", "attestation has no named author", str(packet.ownership))
        )
    statement = str(att.get("statement", "")).strip()
    if not statement:
        packet.violations.append(
            Violation("REQ:ownership-present", "attestation has no statement", str(packet.ownership))
        )
    signed = att.get("signed")
    if signed is None:
        packet.violations.append(
            Violation("REQ:ownership-present", "attestation is not signed (no date)", str(packet.ownership))
        )
    elif not isinstance(signed, _dt.date):
        try:
            _dt.date.fromisoformat(str(signed))
        except ValueError:
            packet.violations.append(
                Violation(
                    "REQ:ownership-present",
                    f"signed date is not an ISO date: {signed!r}",
                    str(packet.ownership),
                )
            )


def check_evidence_pack(packet: Packet) -> None:
    if packet.evidence_pack is None or not packet.evidence_pack.is_file():
        packet.violations.append(Violation("REQ:evidence-pack", "no evidence pack file"))
        return
    try:
        data = tomllib.loads(packet.evidence_pack.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        packet.violations.append(
            Violation("REQ:evidence-pack", f"evidence pack does not parse: {exc}", str(packet.evidence_pack))
        )
        return
    items = data.get("pack", {}).get("items")
    if not isinstance(items, list) or not items:
        packet.violations.append(
            Violation("REQ:evidence-pack", "pack.items is missing or empty", str(packet.evidence_pack))
        )
        return
    # Lead with the synopsis, but only when there is one. A document below the
    # trigger has no synopsis to lead with, and demanding one here would punish
    # short proposals for a rule that deliberately exempts them.
    if packet.synopsis is not None and packet.synopsis.is_file():
        first = str(items[0]).strip()
        expected = packet.synopsis.name
        if Path(first).name != expected:
            packet.violations.append(
                Violation(
                    "REQ:evidence-pack",
                    f"first pack item is {first!r}, must be the synopsis ({expected})",
                    str(packet.evidence_pack),
                )
            )
    for item in items:
        target = (packet.evidence_pack.parent / str(item)).resolve()
        if not target.exists():
            packet.violations.append(
                Violation("REQ:evidence-pack", f"pack item does not exist: {item}", str(packet.evidence_pack))
            )


def run_linter(packet: Packet, policy: Path) -> None:
    targets = [packet.proposal] + ([packet.synopsis] if packet.synopsis else [])
    proc = subprocess.run(
        [sys.executable, str(LINTER), "--policy", str(policy), *[str(t) for t in targets]],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    if proc.returncode == 2:
        raise InvocationError(f"linter invocation failed: {proc.stderr.strip()}")
    if proc.returncode == 1:
        packet.violations.append(
            Violation("REQ:high-signal", "linter reported violations:\n" + proc.stdout.strip())
        )


def resolve_packet(args: argparse.Namespace) -> Packet:
    if args.packet:
        base = Path(args.packet).resolve()
        if not base.is_dir():
            raise InvocationError(f"packet directory not found: {base}")
        proposal = Path(args.proposal).resolve() if args.proposal else base / "proposal.md"
        packet = Packet(
            proposal=proposal,
            synopsis=Path(args.synopsis).resolve() if args.synopsis else base / "synopsis.md",
            ownership=Path(args.ownership).resolve() if args.ownership else base / "ownership.toml",
            evidence_pack=Path(args.evidence_pack).resolve() if args.evidence_pack else base / "evidence-pack.toml",
            doc_type=args.doc_type,
        )
    else:
        if not args.proposal:
            raise InvocationError("give a proposal file or --packet DIR")
        packet = Packet(
            proposal=Path(args.proposal).resolve(),
            synopsis=Path(args.synopsis).resolve() if args.synopsis else None,
            ownership=Path(args.ownership).resolve() if args.ownership else None,
            evidence_pack=Path(args.evidence_pack).resolve() if args.evidence_pack else None,
            doc_type=args.doc_type,
        )
    if not packet.proposal.is_file():
        raise InvocationError(f"proposal not found: {packet.proposal}")
    return packet


def check(packet: Packet, dag: Path, lint_policy: Path | None) -> Packet:
    count_words, strip_code, strip_fm = load_linter_helpers()
    trigger, cap = read_thresholds(dag)
    raw = packet.proposal.read_text(encoding="utf-8")
    body = strip_code(strip_fm(raw))
    doc_words = count_words(body)

    check_structure(packet, raw)
    check_synopsis(packet, doc_words, trigger, cap, count_words, strip_code)
    check_ownership(packet)
    check_evidence_pack(packet)
    if lint_policy is not None:
        run_linter(packet, lint_policy)
    return packet


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Check a proposal packet against the High-Signal Proposal Triage contract."
    )
    p.add_argument("proposal", nargs="?", help="Proposal document (markdown).")
    p.add_argument("--packet", help="Packet directory holding proposal.md, synopsis.md, ownership.toml, evidence-pack.toml.")
    p.add_argument("--synopsis", help="Synopsis file (overrides packet default).")
    p.add_argument("--ownership", help="Ownership attestation TOML (overrides packet default).")
    p.add_argument("--evidence-pack", dest="evidence_pack", help="Evidence pack TOML (overrides packet default).")
    p.add_argument("--doc-type", default="design-doc", choices=DOC_TYPES, help="Document type (default: design-doc).")
    p.add_argument("--dag", default=str(DEFAULT_DAG), help="Triage DAG that states the thresholds.")
    p.add_argument("--lint-policy", dest="lint_policy", help="Also run lint_writing_style.py with this policy (REQ:high-signal).")
    p.add_argument("--format", default="text", choices=("text", "json"), help="Output format.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        packet = resolve_packet(args)
        dag = Path(args.dag).resolve()
        policy = Path(args.lint_policy).resolve() if args.lint_policy else None
        if policy is not None and not policy.is_file():
            raise InvocationError(f"lint policy not found: {policy}")
        trigger, cap = read_thresholds(dag)
        check(packet, dag, policy)
    except InvocationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(
            json.dumps(
                {
                    "proposal": str(packet.proposal),
                    "doc_type": packet.doc_type,
                    "thresholds": {"synopsis_trigger_words": trigger, "synopsis_max_words": cap},
                    "violations": [
                        {"id": v.req_id, "message": v.message, "path": v.path} for v in packet.violations
                    ],
                },
                indent=2,
            )
        )
    else:
        print(f"proposal:   {packet.proposal}")
        print(f"doc type:   {packet.doc_type}")
        print(f"thresholds: synopsis required at {trigger} words, capped at {cap} (read from {dag.name})")
        if not packet.violations:
            print("no violations")
        else:
            print(f"{len(packet.violations)} violation(s):")
            for v in packet.violations:
                where = f" [{v.path}]" if v.path else ""
                print(f"  [{v.req_id}]{where} {v.message}")
    return 1 if packet.violations else 0


if __name__ == "__main__":
    sys.exit(main())
