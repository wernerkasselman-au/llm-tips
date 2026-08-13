# Route proposal intake through a checked packet

## Context

We receive roughly forty design docs, RFCs, and ADRs a quarter. Two senior
architects read them. Last quarter they spent eleven hours in the reading queue
and shortlisted six documents. Four of the six needed a follow-up conversation
before anyone could tell what was being asked for, because the ask was buried on
page three or absent.

The documents that wasted the most reviewer time weren't the weak proposals. They
were the ones where a reader couldn't find the decision. A weak proposal gets
rejected in four minutes. An unreadable one costs a meeting.

## Goals

- Cut the time a reviewer spends deciding whether a document deserves attention.
- Make the ask, the trade-off, and the blast radius visible before page one ends.
- Give authors a mechanical answer to "is this ready to submit" that doesn't
  require a reviewer's time to obtain.

## Non-goals

- Judging whether a proposal is technically correct. That stays with the review
  board and always will.
- Ranking teams, authors, or documents against each other.
- Replacing the review meeting. This changes what arrives at the meeting, not
  what happens in it.

## Proposal

Every proposal above the triage DAG's length trigger arrives as a packet rather
than a document. A packet holds the proposal, a short synopsis, a signed
ownership attestation, and an evidence pack whose first element is that synopsis.
A checker validates the packet shape in CI, and a document that fails the shape
check never reaches the reading queue.

The checker reads its thresholds from the DAG rather than carrying its own copy,
so the numbers cannot drift between the workflow description and the tool that
enforces it.

## Alternatives considered

**A template repository.** Authors copy a skeleton and fill it in. Rejected: we
tried this in 2024 and adherence decayed to under a third within two quarters,
because nothing checked the result and the skeleton drifted from the guidance it
was meant to encode.

**Reviewer-side triage only.** Ask the architects to bounce anything without a
synopsis. Rejected: it spends the exact resource we are trying to protect, and it
puts a senior reviewer in the position of arguing about formatting with a peer.

**A model-graded quality score.** Have a model rate each document and rank the
queue. Rejected for now: we can't explain a score to an author whose proposal
scored badly, and an unexplainable gate breeds workarounds. The mechanical checks
below are ones an author can reproduce locally in a second.

## Consequences

Authors take on a fixed cost per proposal: writing a synopsis and signing an
attestation. For a document already above the length trigger, that's perhaps
twenty minutes. Authors of short documents are unaffected, since the synopsis
requirement only applies above the trigger.

The checker will reject packets that a human would wave through. A missing
`Non-goals` heading is not a real defect in a proposal that clearly states what
it will not do in prose. We accept that cost deliberately: a gate that fires only
when a human would agree is a gate that needs a human to run it.

## Impacted systems

- The proposals repository, which gains a CI job on the packet paths.
- The architecture review board intake process, whose queue becomes the ranked
  shortlist rather than the raw document set.
- No production system, service, or data domain is touched by this change.

## Risks

The obvious failure is theatre: a packet that satisfies every mechanical check
and still says nothing. The checker cannot detect that, and we shouldn't claim it
can. What it does is remove the excuses, so the remaining failures are visible
ones that a reviewer can name in a sentence.

The second risk is that the gate becomes a queue for exceptions. If more than one
in ten packets needs a manual override, the thresholds are wrong and we should
change them in the DAG rather than grant waivers.

## Ask

Approve the packet format and the CI job for one quarter. We'll report override
rate and reviewer hours at the end of it, and revert if the override rate exceeds
one in ten.
