# PROTOCOL

## Channel Identity

- Channel: `review-channel-egor/`
- Project: `Egor Project`
- Purpose: isolated bridge between Codex session and Claude session for expert discovery skill work
- Isolation rule:
  - `review-channel/` belongs to Content Factory and must not be used here
  - `review-channel-egor/` belongs only to Egor Project

## Canonical Shared Files

For Claude, the canonical operational files are:
- `CURRENT_TASK.md`
- `CURRENT_VERDICT.md`

For Codex review history:
- `verdicts/`

For archive only:
- `queue/`

Important:
- `queue/` is not the canonical inbox for Claude
- if Codex wants Claude to act, the operative instruction must be reflected in `CURRENT_TASK.md`
- queue messages may exist as audit trail, but they must not be the only place where a new task lives

## Goal

Build a working Claude Code skill `/expert-hunter` for finding and selecting finance experts.

## Core Deliverable

A working skill that outputs:
- full candidate table
- shortlist top-20
- LinkedIn URLs for candidates
- explainable selection rationale

## Out Of Scope

- outreach
- email / DM flows
- anti-AI detection
- decorative research reports
- role-played expert panels as if they were real experts

## Required Behavior For Claude

If blocked by missing requirements:
- return `QUESTIONS`

If there is implementation progress:
- return `DELIVERABLE_UPDATE`

Do not return long speculative strategy docs instead of code.

## MVP Scope

- Niches:
  - `forex`
  - `stocks`
  - `crypto`
  - `personal finance`
- Geo:
  - `US`
  - secondary: other English-speaking markets
- Expert type:
  - public author / expert with visible digital footprint
- Output default:
  - `CSV`
- Optional secondary output:
  - HTML viewer built from CSV

## Egor Criteria

- citability
- passed exams / credentials
- membership in associations
- university
- native English
- location (`US`, `UK+`)
- public digital footprint required

## Output Schema

Each row must include:

- `name`
- `linkedin_url`
- `primary_role`
- `company`
- `location`
- `niche_tags`
- `credentials_claimed`
- `credentials_verified_or_signal`
- `evidence_links`
- `fit_score`
- `fit_notes`
- `why_selected`
- `confidence`
- `status`

## Working Rules

- claimed and verified signals must be separate
- scoring must be explainable and rule-based for MVP
- output must contain all found candidates plus shortlist top-20
- prioritize working code over specification text

## Codex Review Loop

When the human writes `go`, Codex must follow this order:

1. read the newest Claude message in `review-channel-egor/queue/` matching `REV-*`
2. inspect actual repo artifacts if the message claims code/output changes
3. write/update:
   - `CURRENT_VERDICT.md`
   - `verdicts/...`
   - next `queue/codex-to-claude-...`
4. only after that report back to the human

Codex must not reply with a placeholder like “the handoff is already written” before checking for a newer Claude artifact.

## Codex Task Assignment Rule

When Codex assigns a new task to Claude:

1. Codex must update `CURRENT_TASK.md` with the active task.
2. Codex may additionally write an archive handoff in `queue/`, but that is optional.
3. Codex must not assume Claude has read `queue/` unless the same task is also reflected in `CURRENT_TASK.md`.

## Claude Polling Rule

Claude should treat:
- `CURRENT_TASK.md` as the canonical current assignment
- `CURRENT_VERDICT.md` as the canonical review state

`queue/` may be used as archive/history, but not as the sole source of current instructions.
