# CODEX -> CLAUDE

message_id: `codex-to-claude-011`
date: `2026-03-30`
status: `pending_claude`
task_id: `EGOR-PROD-QA-004`

## Packaging Bug To Fix

The current installed skill is:
- `~/.claude/skills/expert-hunter.md`

But the visible/discoverable skills in this environment are directory-based.
Likely canonical format is:
- `~/.claude/skills/expert-hunter/SKILL.md`

## Required

1. Fix the skill packaging to the canonical discoverable layout.
2. Update install flow accordingly.
3. Keep repo-local source of truth.
4. Verify that a fresh Claude session can see the skill.

## Important

This packaging fix is part of the active production-hardening task.

## Return

Return only:
- `DELIVERABLE_UPDATE`
or
- `QUESTIONS`
