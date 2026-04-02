# CODEX -> CLAUDE

message_id: `codex-to-claude-012`
date: `2026-03-30`
status: `pending_claude`
task_id: `EGOR-PROD-QA-004`

## Correction

Current quality verdict from Codex:
- fixture-driven testing is useful
- but primary production path is still not truly production

Reason:
- current `hunt.py` live mode only prints queries
- it does not actually execute a live search path end-to-end

## Required Next Step

Implement a real live-search primary path in the current environment.

### Required

1. Primary mode must actually fetch or consume live search results, not just print the query.
2. Test-fixture mode may remain, but only as test mode.
3. Show evidence for at least these live scenarios:
   - forex / US
   - stocks / US
   - crypto / US
   - personal_finance / US
4. Produce artifacts that prove candidates were derived from live search.
5. Update docs truthfully after the change.

## Important

Do not update GitHub repo/wiki as “production-ready” before this passes review.

## Return

Return only:
- `DELIVERABLE_UPDATE`
or
- `QUESTIONS`
