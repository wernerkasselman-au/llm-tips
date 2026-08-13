#!/usr/bin/env python3
"""Tests for check_proposal.py.

Every negative test works in ADD form: it starts from the shipped example packet,
which passes, then ADDS a violation and asserts the checker reports that specific
requirement. Deleting something the checker already lists would only prove the
fixture matches itself.

Stdlib only, to match the linter. Run:
    python3 -m unittest discover -s skills/high-signal-proposal-triage/tests
"""

from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parent.parent
EXAMPLE = SKILL_DIR / "examples" / "minimal-proposal-packet"
DAG = REPO_ROOT / "tools" / "proposal_triage_dag.toml"

sys.path.insert(0, str(SKILL_DIR))
import check_proposal  # noqa: E402


def run(args: list[str]) -> tuple[int, str]:
    """Run the checker in-process, returning (exit_code, combined_output)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = check_proposal.main(args)
    return code, out.getvalue() + err.getvalue()


class PacketTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="proposal-packet-"))
        self.packet = self.tmp / "packet"
        shutil.copytree(EXAMPLE, self.packet)
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def check(self, *extra: str) -> tuple[int, str]:
        return run(["--packet", str(self.packet), "--dag", str(DAG), *extra])

    def read(self, name: str) -> str:
        return (self.packet / name).read_text(encoding="utf-8")

    def write(self, name: str, text: str) -> None:
        (self.packet / name).write_text(text, encoding="utf-8")


class TestShippedExamplePasses(PacketTestCase):
    def test_example_packet_is_clean(self) -> None:
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("no violations", out)

    def test_example_packet_passes_the_linter_too(self) -> None:
        code, out = self.check("--lint-policy", str(REPO_ROOT / "tools" / "style_policy.toml"))
        self.assertEqual(code, 0, out)


class TestSynopsisGate(PacketTestCase):
    def test_missing_synopsis_on_long_document_fires(self) -> None:
        (self.packet / "synopsis.md").unlink()
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("REQ:synopsis", out)
        self.assertIn("no synopsis file", out)

    def test_synopsis_over_cap_fires(self) -> None:
        body = self.read("synopsis.md") + "\n\n" + ("padding word " * 200)
        self.write("synopsis.md", body)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("REQ:synopsis", out)
        self.assertIn("cap is", out)

    def test_missing_ask_element_fires(self) -> None:
        self.write("synopsis.md", self.read("synopsis.md").replace("Ask:", "Closing thought:"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("missing a labelled 'ask' element", out)

    def test_missing_problem_element_fires(self) -> None:
        self.write("synopsis.md", self.read("synopsis.md").replace("Problem:", "Background:"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("missing a labelled 'problem' element", out)

    def test_short_document_needs_no_synopsis(self) -> None:
        self.write("proposal.md", "# Tiny\n\n## Goals\n\nOne.\n\n## Non-goals\n\nTwo.\n\n"
                                  "## Alternatives considered\n\nWe rejected doing nothing.\n\n"
                                  "## Consequences\n\nNone.\n")
        (self.packet / "synopsis.md").unlink()
        self.write("evidence-pack.toml", '[pack]\nitems = ["proposal.md"]\n')
        code, out = self.check()
        self.assertNotIn("REQ:synopsis", out)


class TestStructureGate(PacketTestCase):
    def test_missing_non_goals_fires(self) -> None:
        self.write("proposal.md", self.read("proposal.md").replace("## Non-goals", "## Scope notes"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("REQ:structure", out)
        self.assertIn("Non-goals", out)

    def test_missing_alternatives_fires(self) -> None:
        self.write("proposal.md", self.read("proposal.md").replace("## Alternatives considered", "## Other ideas"))
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("Alternatives considered", out)

    def test_alternatives_without_a_rejection_fires(self) -> None:
        text = self.read("proposal.md")
        start = text.index("## Alternatives considered")
        end = text.index("## Consequences")
        gutted = text[:start] + "## Alternatives considered\n\nWe looked at several options.\n\n" + text[end:]
        self.write("proposal.md", gutted)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("no rejected alternative", out)

    def test_adr_lite_uses_its_own_heading_set(self) -> None:
        self.write("proposal.md", "# ADR\n\n## Context\n\nWhy.\n\n## Decision\n\nWhat.\n\n## Consequences\n\nSo what.\n")
        (self.packet / "synopsis.md").unlink()
        self.write("evidence-pack.toml", '[pack]\nitems = ["proposal.md"]\n')
        code, out = self.check("--doc-type", "adr-lite")
        self.assertEqual(code, 0, out)


class TestOwnershipGate(PacketTestCase):
    def test_missing_file_fires(self) -> None:
        (self.packet / "ownership.toml").unlink()
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("REQ:ownership-present", out)

    def test_empty_author_fires(self) -> None:
        self.write("ownership.toml", '[attestation]\nauthor = ""\nsigned = 2026-08-13\nstatement = "Mine."\n')
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("no named author", out)

    def test_unsigned_fires(self) -> None:
        self.write("ownership.toml", '[attestation]\nauthor = "A"\nstatement = "Mine."\n')
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("not signed", out)

    def test_non_iso_date_fires(self) -> None:
        self.write("ownership.toml", '[attestation]\nauthor = "A"\nsigned = "last tuesday"\nstatement = "Mine."\n')
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("not an ISO date", out)

    def test_missing_statement_fires(self) -> None:
        self.write("ownership.toml", '[attestation]\nauthor = "A"\nsigned = 2026-08-13\n')
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("no statement", out)


class TestEvidencePackGate(PacketTestCase):
    def test_synopsis_not_first_fires(self) -> None:
        self.write("evidence-pack.toml", '[pack]\nitems = ["proposal.md", "synopsis.md"]\n')
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("must be the synopsis", out)

    def test_missing_item_file_fires(self) -> None:
        self.write("evidence-pack.toml", '[pack]\nitems = ["synopsis.md", "nonexistent.md"]\n')
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("does not exist", out)

    def test_empty_pack_fires(self) -> None:
        self.write("evidence-pack.toml", "[pack]\nitems = []\n")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("missing or empty", out)


class TestThresholdsComeFromTheDag(PacketTestCase):
    """The thresholds must be READ, not hardcoded. These tests fail if anyone
    inlines 600 or 180 into the checker."""

    def write_dag(self, text: str) -> Path:
        path = self.tmp / "dag.toml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_raising_the_cap_changes_the_verdict(self) -> None:
        # ~194 words: over the shipped cap of 180, under a loosened cap of 300.
        self.write("synopsis.md", self.read("synopsis.md") + "\n\n" + ("padding word " * 25))
        self.assertEqual(self.check()[0], 1)
        loose = self.write_dag('[meta]\nx = "≥ 600 words trigger, ≤ 300 words cap"\n')
        code, out = run(["--packet", str(self.packet), "--dag", str(loose)])
        self.assertEqual(code, 0, out)
        self.assertIn("capped at 300", out)

    def test_lowering_the_trigger_changes_the_verdict(self) -> None:
        (self.packet / "synopsis.md").unlink()
        self.write("evidence-pack.toml", '[pack]\nitems = ["proposal.md"]\n')
        low = self.write_dag('[meta]\nx = "≥ 10 words trigger, ≤ 5 words cap"\n')
        code, out = run(["--packet", str(self.packet), "--dag", str(low)])
        self.assertEqual(code, 1)
        self.assertIn("no synopsis file", out)

    def test_dag_without_thresholds_is_an_invocation_error(self) -> None:
        bare = self.write_dag('[meta]\ntitle = "no numbers here"\n')
        code, out = run(["--packet", str(self.packet), "--dag", str(bare)])
        self.assertEqual(code, 2)
        self.assertIn("cannot read a single synopsis trigger", out)

    def test_ambiguous_dag_is_an_invocation_error(self) -> None:
        ambiguous = self.write_dag('[meta]\na = "≥ 600 words"\nb = "≥ 800 words"\nc = "≤ 180 words"\n')
        code, out = run(["--packet", str(self.packet), "--dag", str(ambiguous)])
        self.assertEqual(code, 2)
        self.assertIn("cannot read a single synopsis trigger", out)

    def test_incoherent_thresholds_are_an_invocation_error(self) -> None:
        bad = self.write_dag('[meta]\na = "≥ 100 words"\nb = "≤ 500 words"\n')
        code, out = run(["--packet", str(self.packet), "--dag", str(bad)])
        self.assertEqual(code, 2)
        self.assertIn("not below trigger", out)

    def test_missing_dag_is_an_invocation_error(self) -> None:
        code, out = run(["--packet", str(self.packet), "--dag", str(self.tmp / "absent.toml")])
        self.assertEqual(code, 2)
        self.assertIn("DAG not found", out)

    def test_shipped_dag_still_states_both_thresholds(self) -> None:
        trigger, cap = check_proposal.read_thresholds(DAG)
        self.assertGreater(trigger, cap)
        self.assertGreater(cap, 0)


class TestInvocation(PacketTestCase):
    def test_missing_proposal_is_an_invocation_error(self) -> None:
        (self.packet / "proposal.md").unlink()
        code, out = self.check()
        self.assertEqual(code, 2)
        self.assertIn("proposal not found", out)

    def test_json_output_lists_violations(self) -> None:
        (self.packet / "ownership.toml").unlink()
        code, out = self.check("--format", "json")
        self.assertEqual(code, 1)
        self.assertIn('"REQ:ownership-present"', out)

    def test_word_counting_matches_the_linter(self) -> None:
        count_words, _, _ = check_proposal.load_linter_helpers()
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        import lint_writing_style

        self.assertEqual(count_words("one two three"), lint_writing_style.word_count("one two three"))


if __name__ == "__main__":
    unittest.main()
