# CURRENT TASK

This file is the canonical inbox for Claude.
If this file changes, Claude should treat it as the current operative assignment.
`queue/` entries are archive/history only and must not override this file.

status: `active`
owner: `claude`
project: `Egor Project`
task_id: `EGOR-GPTZERO-RESEARCH-010`
updated_at: `2026-04-02`

## Objective

Research `gptzero.me` / GPTZero and determine whether it is suitable for our future text-checking skill.

This is a research/specification task only.
Do not implement the final skill yet.

Main goal:
- verify what GPTZero actually offers for AI-text checking;
- verify official API / automation / limits / pricing / operational constraints;
- determine whether GPTZero is suitable for our broker-content text-check workflow;
- compare GPTZero against the already researched ZeroGPT and Ahrefs roles;
- produce concise source-of-truth docs in repo.

## Important execution rules

- Be a strict auditor, not a marketer.
- Prefer primary sources.
- Separate confirmed facts from assumptions.
- Do not invent API support or pricing details if unconfirmed.
- Keep session burn low:
  - avoid broad speculative exploration,
  - focus on the concrete decision: suitable or not for our checking skill.

## Scope

Claude must answer:

1. Does GPTZero have an official API suitable for our workflow?
2. What inputs/outputs does it support?
3. What are the practical automation constraints?
4. What quality signal would GPTZero add to our future pipeline?
5. Should GPTZero replace ZeroGPT, complement it, or stay out of scope?
6. Is GPTZero suitable for a future skill around broker text checking?

## Required inputs to inspect

- Previous related deliverables:
  - `/Users/timofeyzinin/egor-project/docs/zerogpt-checker-research.md`
  - `/Users/timofeyzinin/egor-project/docs/zerogpt-integration-decision.md`
  - `/Users/timofeyzinin/egor-project/docs/ahrefs-checker-spec.md`
  - `/Users/timofeyzinin/egor-project/docs/broker-writer-ahrefs-integration.md`
- Previous bridge updates:
  - `/Users/timofeyzinin/egor-project/review-channel-egor/queue/2026-04-02-claude-deliverable-008.md`
  - `/Users/timofeyzinin/egor-project/review-channel-egor/queue/2026-04-02-claude-deliverable-009.md`

## Deliverables

Claude must produce actual repo docs.

Minimum expected deliverables:

1. One GPTZero research/spec document
2. One short decision note:
   - suitable / not suitable / optional
   - replace / complement / reject vs ZeroGPT
3. One concise `DELIVERABLE_UPDATE` in the bridge

## Suggested output files

- `docs/gptzero-checker-research.md`
- `docs/gptzero-integration-decision.md`

Claude may choose slightly different names if clearer.

## Done When

This task is done only when:

1. GPTZero capabilities and limits are documented honestly
2. automation feasibility is documented honestly
3. recommendation vs ZeroGPT/Ahrefs is explicit
4. a suitability verdict for our skill is explicit
5. `DELIVERABLE_UPDATE` is written
6. Claude explicitly says he is waiting for next `go`

## Response Contract

If blocked:
- return `QUESTIONS`

If progress exists:
- return `DELIVERABLE_UPDATE`
