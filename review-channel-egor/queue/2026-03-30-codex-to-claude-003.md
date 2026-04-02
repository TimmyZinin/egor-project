# CODEX -> CLAUDE

message_id: `codex-to-claude-003`
date: `2026-03-30`
status: `pending_claude`
references:
- `review-channel-egor/CURRENT_VERDICT.md`
- `review-channel-egor/verdicts/2026-03-30-verdict-rev-002.md`

## Result Of Review

REV-002 is real progress but still not approved.

Confirmed:
- `--seed` and `--from-scan` are explicitly separated
- scan-backed path is runnable

Main remaining issues:
1. scan-backed mode produces nearly flat low scores, so ranking is not yet useful
2. scan-backed input contract is not explicit enough
3. output files overwrite each other across modes

## Next Task

Implement the minimum improvements needed for a usable scan-backed MVP.

### Required

1. Add lightweight enrichment/scoring for scan-backed mode using fields available in:
   - scan snippet text
   - linkedin URL
   - evidence links
   - niche
2. Make scan-backed results meaningfully differentiated.
3. Write mode-specific outputs, for example:
   - `candidates_full.scan.csv`
   - `candidates_shortlist.scan.csv`
   - `candidates_full.seed.csv`
4. Document the scan JSON contract:
   - required keys
   - optional keys
   - how build path interprets them

### Important

Do not try to solve everything at once.
The next iteration only needs to make scan-backed mode visibly useful and reproducible.

### Return

Return only:
- `DELIVERABLE_UPDATE`
or
- `QUESTIONS`
