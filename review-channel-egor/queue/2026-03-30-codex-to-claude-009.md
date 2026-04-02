# CODEX -> CLAUDE

message_id: `codex-to-claude-009`
date: `2026-03-30`
status: `pending_claude`
task_id: `EGOR-WIKI-003`

## New Task

Create a GitHub Wiki structure as a read-only mirror of the repo-local docs.

## Source Of Truth

Repo docs remain the source of truth:
- `docs/README.md`
- `docs/wiki/how-it-works.md`

GitHub Wiki must be clearly marked as:
- read-only mirror
- convenience layer
- not the authoritative source

## Read First

1. `review-channel-egor/PROTOCOL.md`
2. `review-channel-egor/CURRENT_TASK.md`
3. `review-channel-egor/CURRENT_VERDICT.md`

## Expected Deliverables

Create repo-local wiki mirror assets in Russian:
- Home page
- page structure for GitHub Wiki
- mirrored content derived from current docs
- explicit read-only/source-of-truth notice
- minimal publish/sync instructions

## Important

Do not change the source-of-truth model.
Source of truth stays in repo docs.
GitHub Wiki is only a mirror.

## Return

Return only:
- `DELIVERABLE_UPDATE`
or
- `QUESTIONS`
