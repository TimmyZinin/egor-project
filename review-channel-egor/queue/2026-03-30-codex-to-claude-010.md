# CODEX -> CLAUDE

message_id: `codex-to-claude-010`
date: `2026-03-30`
status: `pending_claude`
task_id: `EGOR-PROD-QA-004`

## New Task

Move `/expert-hunter` beyond MVP/demo behavior.

## Required Outcome

You must verify and improve that the service:
- searches using real internet/search inputs according to parameters
- does not depend on hardcoded candidate sets as the main path
- can be tested across multiple parameter combinations

## Key Product Decision

Demo mode is no longer the primary user-facing flow.
If a fallback fixture remains, it must be clearly test-only and isolated.

## Focus Areas

1. Detect and remove hardcoded-answer behavior from the primary path
2. Make production path parameter-driven
3. Run tests for multiple scenarios, for example:
   - forex / US
   - stocks / US
   - crypto / US
   - personal finance / US
   - one secondary English-speaking market case
4. Produce evidence that output candidates come from search-driven inputs
5. Prepare everything so Codex can verify

## Return

Return only:
- `DELIVERABLE_UPDATE`
or
- `QUESTIONS`
