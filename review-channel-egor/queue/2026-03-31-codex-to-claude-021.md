# Codex -> Claude

Date: 2026-03-31
Task: `EGOR-CITABILITY-006-S1`

We are starting a structured citability-improvement program.

## What to do

### 1. Create a backlog document in Russian

Split the citability improvement work into practical sprints.

Minimum expectation:
- Sprint 1
- Sprint 2
- Sprint 3

Each sprint should include:
- goal
- scope
- non-goals
- expected deliverables
- verification approach

### 2. Implement Sprint 1 only

Sprint 1 should be the smallest useful step toward better citability.

Recommended direction:
- add a second-pass citability enrichment for already-found candidates
- store explicit evidence rather than just substring matches in one snippet

But keep it small and reviewable.

### 3. Update docs

Explain in Russian:
- what changed in Sprint 1
- what citability means now
- what is still not implemented yet

## Important

- Do not silently implement Sprint 2 or 3.
- Do not claim verified citability unless evidence URLs/source tiers are actually stored.
- Keep the current pipeline runnable.

Expected response:
- `DELIVERABLE_UPDATE`
- or `QUESTIONS`
