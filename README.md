# llm-tips

Evidence-based writing notes and tooling for high-signal prose, documentation, comments, and commits.

## Core documents

- [High-Signal Writing Guide](high_signal_writing_guide.md): renamed and tightened entry point (formerly Anti-AI-Tell Style Guide). The detailed sections haven't moved yet; they're still in `style_guide.md` pending full migration.
- `style_guide.md`: full evidence-based ruleset (vocabulary, structure, voice, formatting).
- `style_guide_tightened.md`: compressed variant.
- `token_optimization.md`: techniques for higher semantic density in documentation.

## Tooling

See [`tools/README.md`](tools/README.md) for usage.

- `tools/style_policy.toml`: machine-readable contracts (~50 rules).
- `tools/lint_writing_style.py`: stdlib linter, requires Python 3.11+.
- `tools/audit_dag.toml`: original writing audit and fix DAG.
- `tools/proposal_triage_dag.toml`: ServiceNow-scale proposal triage DAG. Adds mandatory short synopsis (≤ 180 words for documents ≥ 600 words), ownership attestation, ADR/Design-Doc structural gates, reader-time signals, and a prioritised shortlist + evidence pack for senior architects.

## License

MIT, see [`LICENSE`](LICENSE).
