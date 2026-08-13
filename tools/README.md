# High-Signal writing tooling

Machine-checkable companions to the
[High-Signal Writing Guide](../high_signal_writing_guide.md) and
[`style_guide.md`](../style_guide.md): a ruleset, a linter, and an audit DAG.

## Files

| File | What it is |
|---|---|
| [`style_policy.toml`](style_policy.toml) | Contract-declaration TOML encoding ~50 scannable rules from the style guide (vocab, openers/closers, structural patterns, voice, formatting). Each rule has a stable `AIS:*` id, applicability tags, and a detection mode (`word_boundary`, `phrase`, `regex`, density metric). |
| [`lint_writing_style.py`](lint_writing_style.py) | Stdlib-only Python linter that applies the policy to a prose file and reports violations with line numbers. Exit 0 = clean, 1 = violations, 2 = invocation error. Requires Python 3.11+ (uses `tomllib`). |
| [`audit_dag.toml`](audit_dag.toml) | A 10-unit implementation DAG describing the full audit-and-fix workflow: inventory → parallel scans → triage → rewrite/edit → regression → sign-off. Useful as an orchestration template if you want to fan the audit out across an agent fleet. |
| [`proposal_triage_dag.toml`](proposal_triage_dag.toml) | A 12-unit triage DAG for proposal and design-doc intake at scale: mandatory synopsis (≤ 180 words for documents ≥ 600 words), ownership attestation gate, ADR/Design-Doc structural checks, parallel High-Signal quality scans, and a ranked shortlist plus evidence packs for senior architects. |

## Quick start

```bash
python3 tools/lint_writing_style.py \
  --policy tools/style_policy.toml \
  path/to/article.md
```

If you're checking several files, pass them all in one invocation.

Sample output:

```
file:   path/to/article.md
policy: tools/style_policy.toml
applied 49 contracts (skipped 7 non-applicable)
2 violation(s):
  [AIS:ST02] structural  1 hit(s)
    (document-level): tricolon-fraction too high: 60.00% (3/5 enumerations, limit 30%)
  [AIS:F03] formatting  1 hit(s)
    (document-level): inline-bold rate too high: 1.43 per 200 words (10 bold phrases in 1398 words, limit 1.0)
```

The linter applies only the contracts whose `applies_to` matches the input
file's content type. The default is always `prose` regardless of extension
(`lint_writing_style.py:86`); pass
`--applicability prose|docs|technical_docs|marketing|code_comments|commit_messages`
to select another.

A contract that declares a `density_metric` nothing implements is reported under
`NOT CHECKED` and excluded from the applied count, rather than counted as applied
and passing silently. `AIS:TN02` (`opinionated_claims_per_document_minimum`) is
the one such gap today: "take a position" isn't reliably detectable by pattern,
and a detector that reports "no position taken" about a document that plainly
takes one would be worse than declaring the gap. Pass `--strict-metrics` to turn
any such gap into exit 2, which is how CI catches a policy and linter that have
drifted apart.

## Triage thresholds

The DAG (`audit_dag.toml`, unit `U06`) encodes the recommended hit-weighted
triage from §13 of the style guide:

- Tier-1 vocab, antithesis (`not X, but Y`), balanced-conclusion, §5.14
  second-generation tells: weight `1.0`
- §4.10 filler phrases, restricted-density violations, §6.9 false ranges:
  weight `0.5`
- Voice/format hits: weight `0.25`

Routing:

- Weighted score `≥ 3` → rewrite from scratch (per §12.4: sentence-level
  edits don't fix structural tells).
- Weighted score `1–2` → surgical edit.
- Weighted score `0` → clean, no action.

## Scope of automation

The linter automates roughly the parts of §13's checklist that are
mechanically detectable: vocabulary, opener/closer phrases, em-dash density,
tricolon density, paragraph-uniformity coefficient of variation, copula
avoidance, terminal-participial decoration, ChatGPT-specific markup leaks,
inline-bold density, and the explicit antithesis variants from §5.1.

It doesn't automate:

- "Did the writer take a position?" (§3 P2)
- "Is at least one observational specific present?" (§9.1)
- "Does the piece read aloud as something a human would say?" (§13 voice
  audit)

Those still need a human read; there's no mechanical proxy for any of them. The
§13 checklist calls these out: they're the residue after the linter has done its
job.

## License

MIT (see [`LICENSE`](../LICENSE)). Contributions and bug reports welcome.
