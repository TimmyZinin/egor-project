# Codex -> Claude

Date: 2026-03-31
Task: `EGOR-CLEANUP-007-S2`

We are doing one combined cleanup sprint.

## Required scope

1. Synchronize the main docs with the real current code:
- `docs/README.md`
- `docs/wiki/how-it-works.md`
- `expert-hunter/SKILL.md`

2. Continue the remaining agreed citability work from the previous reviews.

3. Make the skill invocation path clear and correct.

4. Run `/codex review` (or the available Codex review path in your environment) against the completed work.

5. If the Codex review result is below `10/10`, keep iterating until it becomes `10/10`.

## Important

- Do not return early with a partial result.
- Do not claim success without the review result.
- The bridge deliverable must include:
  - what changed
  - what command/path was used for Codex review
  - the explicit `10/10` result
  - a note that you are waiting for the next `go`

Expected response:
- `DELIVERABLE_UPDATE`
- or `QUESTIONS`
