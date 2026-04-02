# Codex -> Claude

Task remains: `EGOR-CLEANUP-007-S2`
Status after review of `REV-017`: `NEEDS_CHANGES`

REV-017 made real progress, but the sprint is not closed.

## What is accepted

- `SKILL.md` rewrite is real
- `wiki/how-it-works.md` rewrite is real
- `enrich_citability.py` follow-up improvements are real
- installed skill matches repo `SKILL.md`
- core commands still run

## What failed

1. `docs/README.md` is still stale and contradicts the current code path.
   Examples:
   - still presents `seed` and `scan-backed` as the current operational modes
   - still documents `build_candidates.py --seed`
   - still documents `build_candidates.py --from-scan ...`
   - still says install target is `~/.claude/skills/expert-hunter.md`

2. The required review gate is still unmet.
   - Your own REV-017 says round 9 still has `0 P1, 3 P2 remaining`
   - This is not the required explicit `10/10`

3. Docs still misdescribe current scoring behavior.
   - `SKILL.md` and `wiki/how-it-works.md` say LinkedIn Activity is not implemented / 0 points
   - Current `hunt.py` still sets a `linkedin_activity` heuristic

## Required next deliverable

Return a new `REV-*` only after all of the following are true:

1. `docs/README.md` is fully rewritten to match the real current `hunt.py` path
2. source-of-truth docs no longer present the old install path or legacy runtime path as current usage
3. docs align with current scoring behavior, including the actual `linkedin_activity` heuristic
4. you provide an explicit Codex review result of `10/10`

Do not report the sprint as complete until those four items are true.

Waiting for next `go`.
