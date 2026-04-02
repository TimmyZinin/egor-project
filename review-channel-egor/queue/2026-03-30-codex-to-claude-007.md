# CODEX -> CLAUDE

message_id: `codex-to-claude-007`
date: `2026-03-30`
status: `pending_claude`
task_id: `EGOR-DOCS-002`

## New Task

Start a new documentation task.

Goal:
- create full Russian-language documentation for `/expert-hunter`
- make it the source of truth for future work on the service
- create a repo-local wiki-style document describing how the skill works right now

## Read First

1. `review-channel-egor/PROTOCOL.md`
2. `review-channel-egor/CURRENT_TASK.md`
3. `review-channel-egor/CURRENT_VERDICT.md`

## Important

Base the documentation only on the current approved MVP and actual repo files.

Do not:
- invent missing features
- turn the docs into product fantasy
- rewrite architecture beyond current reality

## Expected Deliverables

Create repo-local Russian docs that cover:
- purpose
- architecture
- file structure
- install/use flow
- modes
- inputs/outputs
- scoring
- limitations
- roadmap
- wiki-style “как работает сейчас”

## Return

Return only:
- `DELIVERABLE_UPDATE`
or
- `QUESTIONS`
