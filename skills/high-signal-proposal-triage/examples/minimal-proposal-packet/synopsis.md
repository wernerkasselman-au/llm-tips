# Synopsis: route proposal intake through a checked packet

Problem: two architects spent eleven hours last quarter reading forty proposals.
Four of the six they shortlisted needed a follow-up conversation just to
establish what was being asked for, because the ask wasn't on the first page.

Proposed action: require any proposal above the triage DAG's length trigger to
arrive as a packet, meaning the document plus a synopsis, a signed ownership
attestation, and an evidence pack that leads with the synopsis. CI checks the
packet shape before the document enters the reading queue.

Trade-off: authors pay about twenty minutes per long proposal, and the checker
will bounce packets a human would've waved through. Both costs are deliberate.

Ask: approve the format and the CI job for one quarter. We'll report override
rate and reviewer hours at the end, and we'll revert it if more than one packet
in ten needs a manual override.
