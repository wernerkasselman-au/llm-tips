#!/usr/bin/env python3
"""Tests for lint_writing_style.py, focused on the unimplemented-metric gap.

The defect these cover: a contract whose density_metric had no implementation was
counted as applied and returned no violations, which reads exactly like a clean
pass. Three independent reviewers found it by inspection; nothing in the repo
would have caught it.

Negative cases are in ADD form: they add a contract or a violation and assert the
linter reports it. Stdlib only. Run:
    python3 -m unittest discover -s tests
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import lint_writing_style as lint  # noqa: E402

POLICY = REPO_ROOT / "tools" / "style_policy.toml"

# The one gap we know about and have chosen to declare rather than fake.
# If this set changes, either someone implemented TN02 (update the test) or
# someone added a new unimplemented metric (implement it or declare it).
KNOWN_UNIMPLEMENTED = {"AIS:TN02"}

# Built with chr() so this file stays free of the character it tests for.
EM_DASH = chr(0x2014)

CLEAN_DOC = """# Title

We rejected the alternative because it doesn't scale, and that's the position
this document takes. It isn't a neutral survey.

Short para here.

A somewhat longer paragraph follows, so the paragraph-length coefficient of
variation doesn't collapse to zero and trip the uniformity contract that this
fixture isn't trying to exercise. We think that's reasonable.
"""


def run_cli(args: list[str]) -> tuple[int, str]:
    out, err = io.StringIO(), io.StringIO()
    argv = sys.argv
    sys.argv = ["lint_writing_style.py", *args]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = lint.main()
    finally:
        sys.argv = argv
    return code, out.getvalue() + err.getvalue()


class TestMetricRegistry(unittest.TestCase):
    def test_registry_is_derived_not_typed(self) -> None:
        """The set must come from the dispatch source, so it cannot drift."""
        derived = lint._implemented_metrics()
        self.assertEqual(derived, lint.IMPLEMENTED_METRICS)
        self.assertIn("contractions_per_1000_words_minimum", derived)
        self.assertIn("em_dash_per_1000_words", derived)

    def test_a_real_metric_is_not_reported_unimplemented(self) -> None:
        self.assertIsNone(lint.unimplemented_metric({"density_metric": "em_dash_per_1000_words"}))

    def test_an_invented_metric_is_reported(self) -> None:
        self.assertEqual(
            lint.unimplemented_metric({"density_metric": "vibes_per_paragraph_maximum"}),
            "vibes_per_paragraph_maximum",
        )

    def test_contract_without_a_metric_is_not_reported(self) -> None:
        self.assertIsNone(lint.unimplemented_metric({"blacklist": ["delve"]}))


class TestShippedPolicyGap(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="lint-tests-"))
        self.doc = self.tmp / "doc.md"
        self.doc.write_text(CLEAN_DOC, encoding="utf-8")

    def test_only_the_known_gap_is_unimplemented(self) -> None:
        """Fails if anyone adds a policy metric without implementing it."""
        with open(POLICY, "rb") as fh:
            policy = tomllib.load(fh)
        found = {
            c["id"]
            for c in policy.get("contracts", [])
            if c.get("id") and lint.unimplemented_metric(c)
        }
        self.assertEqual(found, KNOWN_UNIMPLEMENTED)

    def test_report_names_the_unchecked_contract(self) -> None:
        code, out = run_cli(["--policy", str(POLICY), str(self.doc)])
        self.assertEqual(code, 0, out)
        self.assertIn("NOT CHECKED", out)
        self.assertIn("AIS:TN02", out)

    def test_unimplemented_contracts_are_not_counted_as_applied(self) -> None:
        with open(POLICY, "rb") as fh:
            policy = tomllib.load(fh)
        report = lint.lint_file(self.doc, policy, lint.normalize_applicability("prose"))
        self.assertTrue(report.unimplemented)
        self.assertEqual({rid for rid, _ in report.unimplemented}, KNOWN_UNIMPLEMENTED)

    def test_counts_partition_the_policy(self) -> None:
        """applied + skipped + unimplemented must equal the contract total.

        Without this, a contract can be recorded as unimplemented AND counted as
        applied, which restores the exact overstatement this change removes.
        """
        with open(POLICY, "rb") as fh:
            policy = tomllib.load(fh)
        total = len([c for c in policy.get("contracts", []) if c.get("id")])
        report = lint.lint_file(self.doc, policy, lint.normalize_applicability("prose"))
        self.assertEqual(report.applied + report.skipped + len(report.unimplemented), total)
        self.assertNotIn("AIS:TN02", {v.rule_id for v in report.violations})

    def test_strict_metrics_exits_2(self) -> None:
        code, out = run_cli(["--policy", str(POLICY), "--strict-metrics", str(self.doc)])
        self.assertEqual(code, 2)
        self.assertIn("strict-metrics", out)

    def test_json_output_lists_unimplemented(self) -> None:
        code, out = run_cli(["--policy", str(POLICY), "--format", "json", str(self.doc)])
        self.assertEqual(code, 0, out)
        self.assertIn("unimplemented_contracts", out)
        self.assertIn("opinionated_claims_per_document_minimum", out)


class TestDetectionStillWorks(unittest.TestCase):
    """ADD form: introduce a violation and confirm the linter still fires. These
    guard the checks that the unimplemented-metric change routes around."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="lint-tests-"))
        self.doc = self.tmp / "doc.md"

    def lint_text(self, text: str) -> tuple[int, str]:
        self.doc.write_text(text, encoding="utf-8")
        return run_cli(["--policy", str(POLICY), str(self.doc)])

    def test_tier1_vocabulary_fires(self) -> None:
        code, out = self.lint_text(CLEAN_DOC + "\n\nLet us delve into the details.\n")
        self.assertEqual(code, 1)
        self.assertIn("AIS:L01", out)

    def test_em_dash_density_fires(self) -> None:
        dashes = f" a {EM_DASH} b {EM_DASH} c {EM_DASH} d {EM_DASH} e"
        code, out = self.lint_text("# T\n\n" + "word " * 40 + dashes + "\n")
        self.assertEqual(code, 1)
        self.assertIn("AIS:ST08", out)

    def test_inline_bold_density_fires(self) -> None:
        code, out = self.lint_text("# T\n\n**one** **two** **three** **four** and some words.\n")
        self.assertEqual(code, 1)
        self.assertIn("AIS:F03", out)

    def test_contraction_floor_fires(self) -> None:
        code, out = self.lint_text("# T\n\n" + ("formal prose without any shortened forms " * 20) + "\n")
        self.assertEqual(code, 1)
        self.assertIn("AIS:TN01", out)


if __name__ == "__main__":
    unittest.main()
