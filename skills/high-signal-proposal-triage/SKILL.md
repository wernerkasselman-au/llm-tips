---
name: high-signal-proposal-triage
description: >
  Apply High-Signal writing standards and structural proposal checks before any
  design doc, RFC, ADR, or architecture recommendation is shortlisted for senior
  review: short synopsis, ownership attestation, ADR/Design-Doc sections, ranked
  evidence packs. Mostly agent-performed discipline, not automated enforcement.
  Only the High-Signal text scans execute today; see "What is actually enforced".
---

# High-Signal Proposal Triage

## When to activate

- Any internal proposal, design doc, RFC, ADR, SAD packet, or architecture
  recommendation that other people will read.
- Before a document joins an Architecture Review Board queue or a senior-architect
  shortlist.
- When an agent is asked to draft, review, or improve a proposal.

## Core artefacts

This skill owns no copies. Every artefact below lives once, in the repo, and is
referenced by relative path. If you find a second copy of any of them inside this
directory, delete it: two copies drift, and the one people read is whichever they
found first.

| Artefact | Path from here | Role |
| --- | --- | --- |
| Triage DAG | `../../tools/proposal_triage_dag.toml` | Executable 12-unit triage workflow. Holds the thresholds. |
| Writing guide | `../../high_signal_writing_guide.md` | Writing standards (ownership, specificity, anti-padding). |
| Style policy | `../../tools/style_policy.toml` | ~50 machine-readable contracts the linter executes. |
| Linter | `../../tools/lint_writing_style.py` | The only executable content gate today. Run it from the repo root, not from here. |
| This contract | `contract-declaration.toml` | Requirement IDs, severities, promotion rules. Declarative, see below. |

## Single source of truth for thresholds

The synopsis trigger and the synopsis cap live in the DAG, in units `U01` and
`U02`. Don't restate either number in this file, in `contract-declaration.toml`,
or in any prompt. Read them from the DAG. A number copied into a second file
won't stay in sync with the first.

## What is actually enforced today

Be precise about this, because an unexecuted gate is indistinguishable from no gate.

| Gate | Status |
| --- | --- |
| High-Signal vocabulary, structure, voice, formatting scans | Executable, per file. `lint_writing_style.py` against `style_policy.toml`, run from the repo root. One caveat: `AIS:TN02` has no implementation and returns clean silently while still counting toward the reported "applied N contracts". |
| Synopsis 1.5x weighting and U07 scoring/routing | Not executable. The linter reports violations per file; it scores nothing and routes nothing. |
| Synopsis presence and word cap | Not executable. No runner exists. Checkable in principle: it is a word count. |
| Structural minimums (Goals, Non-goals, Alternatives, Consequences) | Not executable. No runner exists. Checkable in principle: heading presence. |
| Ownership attestation | Presence is checkable. The truth of the attestation is not, by anyone. See below. |
| Ranked shortlist and evidence pack assembly | Not executable. Agent-performed. |

Producing the missing checker is the next artefact, not a footnote. Until it
exists, this skill is a disciplined operating manual, not an enforcement layer,
and it should be described that way to anyone who asks.

## Required behaviour

1. Load `contract-declaration.toml` and the DAG before producing or accepting any
   proposal body. Read the thresholds from the DAG at load time.
2. Treat the short synopsis as the primary triage surface. Senior reviewers read
   the shortlist, not the document set.
3. Require an ownership attestation to be **present and signed** by a named
   author. What you can verify is that it exists and who signed it. You can't
   verify that the thinking behind it is theirs, and no gate in this repo claims
   to. Don't let the attestation's presence be reported as proof of authorship.
4. Enforce the structural minimums from DAG unit `U03`: Goals plus Non-goals,
   Alternatives considered with at least one rejected alternative and its reason,
   and Consequences or impacted systems.
5. Run the High-Signal scans (`U04`, `U05`) in parallel. Weighted hits at or above
   the DAG's rewrite threshold mean rewrite from the notes, not sentence edits.
6. Emit a ranked shortlist plus a self-contained evidence pack whose first element
   is the synopsis (`U10`).
7. Never auto-promote a document that failed the synopsis or ownership hard gates
   (`U02`).
8. Report which gates ran and which were skipped. A triage run that silently
   skipped the unexecutable gates must not read as a clean pass.

## Unit map

| Layer | Units |
| --- | --- |
| 0 intake | `U01` proposal-inventory, `U02` synopsis-and-ownership-gate |
| 1 parallel scans | `U03` structural-section-check, `U04` vocabulary-scan, `U05` structure-voice-scan, `U06` reader-time-signal |
| 2 triage | `U07` triage-scoring-and-classification |
| 3 remediation | `U08` writing-quality-remediation, `U09` impact-and-blast-radius-enrichment, `U10` evidence-pack-and-shortlist-assembly |
| 4 validation | `U11` post-remediation-regression |
| 5 sign-off | `U12` sign-off-and-attestation |

## Relationship to other packs

- Complements agent-assurance contribution governance (no self-approval, closure
  roots, multi-LLM review).
- Composable later with an architecture-inventory adapter so that "Impacted
  systems" and "Alternatives" become claims checked against real state instead of
  free text. That adapter doesn't exist yet.

## Scope

This skill owns writing quality, structural completeness, ownership attestation,
and shortlisting. It isn't an architecture review board and doesn't judge whether
a proposal is technically right.
