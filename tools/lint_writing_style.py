#!/usr/bin/env python3
"""Lint prose against a high-signal style-policy TOML file.

Reads a contract-declaration TOML (e.g., tools/style_policy.toml)
and applies each scannable contract to a prose document, reporting violations
with rule IDs, line numbers, and excerpts.

Example:
    python3 tools/lint_writing_style.py \\
        --policy tools/style_policy.toml \\
        /path/to/prose.md

Exit codes:
    0  no violations
    1  one or more violations found
    2  invocation or parse error
"""

from __future__ import annotations

import argparse
import math
import pathlib
import re
import statistics
import sys
import tomllib
from dataclasses import dataclass, field


MATCH_MODES = {
    "word_boundary_case_insensitive",
    "word_boundary_case_sensitive",
    "phrase_case_insensitive",
    "phrase_case_sensitive",
    "sentence_start_case_insensitive",
    "regex",
    "regex_multiline",
}

APPLICABILITY_SYNONYMS = {
    "prose": {"prose", "markdown", "article", "blog", "essay"},
    "documentation": {"documentation", "docs", "readme", "guide"},
    "technical_docs": {"technical_docs", "technical", "reference", "spec"},
    "marketing": {"marketing", "copy", "landing"},
    "code_comments": {"code_comments", "code", "comments"},
    "commit_messages": {"commit_messages", "commit", "changelog", "pr"},
}


@dataclass
class Violation:
    rule_id: str
    domain: str
    message: str
    line: int | None = None
    excerpt: str | None = None

    def format(self) -> str:
        loc = f":{self.line}" if self.line is not None else ""
        head = f"{self.rule_id}{loc} [{self.domain}] {self.message}"
        if self.excerpt:
            return f"{head}\n    {self.excerpt}"
        return head


@dataclass
class LintReport:
    file: pathlib.Path
    policy: pathlib.Path
    applied: int = 0
    skipped: int = 0
    violations: list[Violation] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint prose against a high-signal policy TOML.")
    parser.add_argument("files", nargs="+", help="Prose file(s) to lint (markdown, plain text).")
    parser.add_argument(
        "--policy",
        required=True,
        help="Path to style-policy TOML (contract-declaration).",
    )
    parser.add_argument(
        "--applicability",
        default="prose",
        help=(
            "Document type for selecting applicable contracts: "
            "prose | documentation | technical_docs | marketing | code_comments | commit_messages. "
            "Default: prose."
        ),
    )
    parser.add_argument(
        "--fail-on",
        choices=("any", "tier1", "never"),
        default="any",
        help="Exit status policy. any: any violation fails. tier1: only lexical_tier1/opener_banned/closer_banned fail. never: always 0.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="1.0.0",
    )
    return parser.parse_args()


def load_policy(path: pathlib.Path) -> dict:
    with path.open("rb") as handle:
        doc = tomllib.load(handle)
    contracts = doc.get("contracts")
    if not isinstance(contracts, list):
        raise SystemExit(f"{path}: missing [[contracts]] array")
    return doc


def normalize_applicability(target: str) -> set[str]:
    target = target.strip().lower()
    if target in APPLICABILITY_SYNONYMS:
        return APPLICABILITY_SYNONYMS[target]
    return {target}


def contract_applies(contract: dict, target_set: set[str]) -> bool:
    applies_to = contract.get("applies_to")
    if not applies_to:
        return True
    if not isinstance(applies_to, list):
        return False
    return any(entry in target_set for entry in applies_to)


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and inline code from markdown so lexical checks
    don't flag legitimate code."""
    text = re.sub(r"```.*?```", "\n", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "\n", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    return text


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def compute_line_map(text: str) -> list[int]:
    """Return list of character offsets where each 1-indexed line begins."""
    starts = [0]
    for m in re.finditer(r"\n", text):
        starts.append(m.end())
    return starts


def offset_to_line(offset: int, line_starts: list[int]) -> int:
    lo, hi = 0, len(line_starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if line_starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def excerpt_around(text: str, start: int, end: int, width: int = 60) -> str:
    left = max(0, start - width)
    right = min(len(text), end + width)
    snippet = text[left:right].replace("\n", " ").strip()
    if left > 0:
        snippet = "..." + snippet
    if right < len(text):
        snippet = snippet + "..."
    return snippet


def tokenize_sentences(text: str) -> list[str]:
    # Simple sentence splitter: split on sentence-ending punctuation followed by whitespace+capital.
    # Good enough for coarse sentence-length statistics.
    text = re.sub(r"\s+", " ", text)
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", text)
    return [p.strip() for p in pieces if p.strip()]


def split_paragraphs(text: str) -> list[str]:
    paras = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paras if p.strip()]


def word_count(s: str) -> int:
    return len(re.findall(r"\b\w[\w'-]*\b", s))


def compile_blacklist(items: list[str], mode: str) -> list[tuple[str, re.Pattern]]:
    patterns: list[tuple[str, re.Pattern]] = []
    flags_ci = re.IGNORECASE
    flags_ml = re.MULTILINE
    for raw in items:
        if mode == "word_boundary_case_insensitive":
            patterns.append((raw, re.compile(rf"\b{re.escape(raw)}\b", flags_ci)))
        elif mode == "word_boundary_case_sensitive":
            patterns.append((raw, re.compile(rf"\b{re.escape(raw)}\b")))
        elif mode == "phrase_case_insensitive":
            patterns.append((raw, re.compile(re.escape(raw), flags_ci)))
        elif mode == "phrase_case_sensitive":
            patterns.append((raw, re.compile(re.escape(raw))))
        elif mode == "sentence_start_case_insensitive":
            # Match at start of string or after sentence-terminator or newline.
            patterns.append((raw, re.compile(rf"(?:^|(?<=[.!?]\s)|(?<=\n\n)){re.escape(raw)}", flags_ci)))
        elif mode == "regex":
            patterns.append((raw, re.compile(raw, flags_ci)))
        elif mode == "regex_multiline":
            patterns.append((raw, re.compile(raw, flags_ci | flags_ml)))
        else:
            raise SystemExit(f"unknown match_mode: {mode}")
    return patterns


def apply_blacklist_contract(contract: dict, text: str, line_starts: list[int]) -> list[Violation]:
    rule_id = contract["id"]
    domain = contract.get("domain", "unknown")
    mode = contract.get("match_mode", "word_boundary_case_insensitive")
    if mode not in MATCH_MODES:
        return [Violation(rule_id, domain, f"unsupported match_mode: {mode}")]

    threshold = contract.get("density_threshold", 0)
    per_words = contract.get("density_per_words")
    items = list(contract.get("blacklist", [])) + list(contract.get("blacklist_regex", []))
    effective_mode = mode
    if contract.get("blacklist_regex") and mode not in {"regex", "regex_multiline"}:
        effective_mode = "regex" if mode != "regex_multiline" else "regex_multiline"

    if not items:
        return []

    patterns = compile_blacklist(items, effective_mode)
    hits: list[tuple[str, re.Match]] = []
    for raw, pattern in patterns:
        for m in pattern.finditer(text):
            hits.append((raw, m))

    violations: list[Violation] = []
    if not hits:
        return violations

    # Density threshold logic:
    # - threshold == 0: every hit is a violation
    # - threshold > 0 with per_words: compute hits per per_words; violate if exceeded
    # - threshold > 0 without per_words: allow up to `threshold` hits total
    if threshold == 0:
        for raw, m in hits:
            line = offset_to_line(m.start(), line_starts)
            violations.append(
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=f"banned phrase: '{raw}'",
                    line=line,
                    excerpt=excerpt_around(text, m.start(), m.end()),
                )
            )
    else:
        total_words = max(1, word_count(text))
        if per_words:
            density = (len(hits) * per_words) / total_words
            limit = float(threshold)
            if density > limit:
                violations.append(
                    Violation(
                        rule_id=rule_id,
                        domain=domain,
                        message=(
                            f"density exceeded: {len(hits)} hits in {total_words} words "
                            f"= {density:.2f} per {per_words} (limit {limit})"
                        ),
                        line=offset_to_line(hits[0][1].start(), line_starts),
                        excerpt=excerpt_around(text, hits[0][1].start(), hits[0][1].end()),
                    )
                )
        else:
            if len(hits) > int(threshold):
                violations.append(
                    Violation(
                        rule_id=rule_id,
                        domain=domain,
                        message=(
                            f"count exceeded: {len(hits)} hits (limit {threshold})"
                        ),
                        line=offset_to_line(hits[0][1].start(), line_starts),
                        excerpt=excerpt_around(text, hits[0][1].start(), hits[0][1].end()),
                    )
                )
    return violations


def apply_structural_metrics(contract: dict, text: str) -> list[Violation]:
    rule_id = contract["id"]
    domain = contract.get("domain", "unknown")
    metric = contract.get("density_metric")
    if not metric:
        return []

    if metric == "paragraph_length_coefficient_of_variation_minimum":
        threshold = float(contract.get("density_threshold", 0.40))
        paras = split_paragraphs(text)
        lengths = [word_count(p) for p in paras if word_count(p) > 0]
        if len(lengths) < 3:
            return []
        mean = statistics.mean(lengths)
        if mean == 0:
            return []
        std = statistics.pstdev(lengths)
        cov = std / mean
        if cov < threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"paragraph-length CoV too low: {cov:.3f} < {threshold:.2f} "
                        f"({len(lengths)} paragraphs, mean {mean:.1f}, std {std:.1f})"
                    ),
                )
            ]
        return []

    if metric == "sentence_length_coefficient_of_variation_minimum":
        threshold = float(contract.get("density_threshold", 0.35))
        sentences = tokenize_sentences(text)
        lengths = [word_count(s) for s in sentences if word_count(s) > 0]
        if len(lengths) < 5:
            return []
        mean = statistics.mean(lengths)
        if mean == 0:
            return []
        std = statistics.pstdev(lengths)
        cov = std / mean
        if cov < threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"sentence-length CoV too low: {cov:.3f} < {threshold:.2f} "
                        f"({len(lengths)} sentences, mean {mean:.1f}, std {std:.1f})"
                    ),
                )
            ]
        return []

    if metric == "em_dash_per_1000_words":
        threshold = float(contract.get("density_threshold", 5.0))
        words = max(1, word_count(text))
        count = text.count("\u2014")
        rate = (count * 1000) / words
        if rate > threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"em-dash rate too high: {rate:.2f} per 1,000 words "
                        f"({count} em-dashes in {words} words, limit {threshold})"
                    ),
                )
            ]
        return []

    if metric == "contractions_per_1000_words_minimum":
        threshold = float(contract.get("density_threshold", 8))
        words = max(1, word_count(text))
        # Minimal contraction detector: match common English contractions.
        pattern = re.compile(
            r"\b(?:don't|doesn't|didn't|won't|can't|shouldn't|wouldn't|couldn't|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|it's|that's|there's|here's|what's|who's|i'm|you're|we're|they're|i've|you've|we've|they've|i'll|you'll|he'll|she'll|we'll|they'll|i'd|you'd|he'd|she'd|we'd|they'd|let's|y'all)\b",
            re.IGNORECASE,
        )
        count = len(pattern.findall(text))
        rate = (count * 1000) / words
        if rate < threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"contraction rate too low: {rate:.2f} per 1,000 words "
                        f"({count} contractions in {words} words, minimum {threshold})"
                    ),
                )
            ]
        return []

    if metric == "inline_bold_phrases_per_200_words_maximum":
        threshold = float(contract.get("density_threshold", 1))
        words = max(1, word_count(text))
        count = len(re.findall(r"(?<!\*)\*\*[^*\n]+\*\*(?!\*)", text))
        rate = (count * 200) / words
        if rate > threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"inline-bold rate too high: {rate:.2f} per 200 words "
                        f"({count} bold phrases in {words} words, limit {threshold})"
                    ),
                )
            ]
        return []

    if metric == "trivial_restatement_comments_fraction_maximum":
        # Coarse heuristic for code-comment inputs: fraction of comment lines that
        # look like restatement (contain common filler openers like "Calculate",
        # "Return", "Initialize", "Iterate").
        threshold = float(contract.get("density_threshold", 0.15))
        comment_lines = re.findall(r"^\s*(?://|#)\s*.+$", text, re.MULTILINE)
        if not comment_lines:
            return []
        restatement = re.compile(
            r"^\s*(?://|#)\s*(?:Calculate|Return|Initialize|Initialise|Iterate|Loop|Increment|Decrement|Set|Get)\b",
            re.IGNORECASE,
        )
        hits = [line for line in comment_lines if restatement.match(line)]
        fraction = len(hits) / len(comment_lines)
        if fraction > threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"trivial-restatement comment fraction too high: "
                        f"{fraction:.2%} ({len(hits)}/{len(comment_lines)} comments, limit {threshold:.0%})"
                    ),
                )
            ]
        return []

    if metric == "version_strings_per_document_minimum":
        threshold = int(contract.get("density_threshold", 2))
        # Count version-like strings: x.y, x.y.z, vN, semantic version patterns.
        pattern = re.compile(r"\b(?:v?\d+\.\d+(?:\.\d+)?|python\s*[\d.]+|node\s*[\d.]+)\b", re.IGNORECASE)
        count = len(pattern.findall(text))
        if count < threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=f"too few specific version strings: {count} (minimum {threshold})",
                )
            ]
        return []

    if metric == "tricolon_fraction_of_enumerations":
        # Count comma-separated enumerations of N items; flag if fraction with N==3 exceeds threshold.
        threshold = float(contract.get("density_threshold", 0.30))
        enum_pattern = re.compile(
            r"(?:\b[\w-]+(?:,\s+[\w-]+){1,5}(?:,?\s+(?:and|or)\s+[\w-]+))",
            re.IGNORECASE,
        )
        enums = enum_pattern.findall(text)
        if len(enums) < 5:
            return []
        tricolons = [e for e in enums if e.count(",") == 2]
        fraction = len(tricolons) / len(enums)
        if fraction > threshold:
            return [
                Violation(
                    rule_id=rule_id,
                    domain=domain,
                    message=(
                        f"tricolon-fraction too high: {fraction:.2%} "
                        f"({len(tricolons)}/{len(enums)} enumerations, limit {threshold:.0%})"
                    ),
                )
            ]
        return []

    # Metrics we do not automate (opinion density, citation integrity, etc.).
    return []


def apply_contract(contract: dict, text: str, line_starts: list[int]) -> list[Violation]:
    has_blacklist = bool(contract.get("blacklist") or contract.get("blacklist_regex"))
    has_metric = bool(contract.get("density_metric"))
    violations: list[Violation] = []
    if has_blacklist:
        violations.extend(apply_blacklist_contract(contract, text, line_starts))
    if has_metric:
        violations.extend(apply_structural_metrics(contract, text))
    return violations


def failure_policy(violations: list[Violation], policy: str) -> bool:
    if policy == "never":
        return False
    if policy == "any":
        return bool(violations)
    if policy == "tier1":
        tier1_domains = {
            "lexical_tier1",
            "opener_banned",
            "closer_banned",
            "sycophancy",
            "integrity",
        }
        return any(v.domain in tier1_domains for v in violations)
    return bool(violations)


def render_report(report: LintReport, fmt: str) -> str:
    if fmt == "json":
        import json

        data = {
            "file": str(report.file),
            "policy": str(report.policy),
            "applied_contracts": report.applied,
            "skipped_contracts": report.skipped,
            "violation_count": len(report.violations),
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "domain": v.domain,
                    "message": v.message,
                    "line": v.line,
                    "excerpt": v.excerpt,
                }
                for v in report.violations
            ],
        }
        return json.dumps(data, indent=2)

    lines = []
    lines.append(f"file:   {report.file}")
    lines.append(f"policy: {report.policy}")
    lines.append(f"applied {report.applied} contracts (skipped {report.skipped} non-applicable)")
    if not report.violations:
        lines.append("no violations")
        return "\n".join(lines)

    lines.append(f"{len(report.violations)} violation(s):")
    by_rule: dict[str, list[Violation]] = {}
    for v in report.violations:
        by_rule.setdefault(v.rule_id, []).append(v)
    for rule_id in sorted(by_rule):
        vs = by_rule[rule_id]
        lines.append(f"  [{rule_id}] {vs[0].domain}  {len(vs)} hit(s)")
        for v in vs[:5]:
            loc = f"    line {v.line}" if v.line else "    (document-level)"
            lines.append(f"{loc}: {v.message}")
            if v.excerpt:
                lines.append(f"      > {v.excerpt}")
        if len(vs) > 5:
            lines.append(f"    ... {len(vs) - 5} more")
    return "\n".join(lines)


def lint_file(path: pathlib.Path, policy: dict, target_set: set[str]) -> LintReport:
    raw = path.read_text(encoding="utf-8")
    text = strip_front_matter(raw)
    text = strip_code_blocks(text)
    line_starts = compute_line_map(raw)

    report = LintReport(file=path, policy=pathlib.Path("<policy>"))
    for contract in policy.get("contracts", []):
        if not contract.get("id"):
            continue
        if not contract_applies(contract, target_set):
            report.skipped += 1
            continue
        report.applied += 1
        report.violations.extend(apply_contract(contract, text, line_starts))
    return report


def main() -> int:
    args = parse_args()
    policy_path = pathlib.Path(args.policy)
    if not policy_path.exists():
        sys.stderr.write(f"policy file not found: {policy_path}\n")
        return 2
    try:
        policy = load_policy(policy_path)
    except tomllib.TOMLDecodeError as exc:
        sys.stderr.write(f"failed to parse policy TOML: {exc}\n")
        return 2

    target_set = normalize_applicability(args.applicability)
    any_failed = False
    for file_arg in args.files:
        path = pathlib.Path(file_arg)
        if not path.exists():
            sys.stderr.write(f"file not found: {path}\n")
            any_failed = True
            continue
        report = lint_file(path, policy, target_set)
        report.policy = policy_path
        print(render_report(report, args.format))
        if failure_policy(report.violations, args.fail_on):
            any_failed = True

    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
