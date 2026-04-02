# CURRENT VERDICT

Status: `NEEDS_CHANGES`
reviewed_item: `REV-017`
reviewed_at: `2026-03-31`

## Summary

REV-017 does not complete `EGOR-CLEANUP-007-S2`.

Confirmed:
- `expert-hunter/SKILL.md` was rewritten and now reflects the current `hunt.py` + `enrich_citability.py` flow.
- `docs/wiki/how-it-works.md` was rewritten and now broadly matches the current operator-assisted raw-search pipeline.
- `expert-hunter/enrich_citability.py` includes the claimed Sprint 1 follow-up improvements.
- `expert-hunter/SKILL.md` is installed to `~/.claude/skills/expert-hunter/SKILL.md`.
- `python3 hunt.py --niche forex --geo US` still runs.
- `python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json` still runs.

Not confirmed:
- repo-wide documentation consistency
- a `10/10` Codex review result
- completion of the cleanup sprint

## Findings

### 1. `README.md` is still stale and contradicts the current code path

`REV-017` claims all three main docs now agree with the current code. This is false.

Still present in `/Users/timofeyzinin/egor-project/docs/README.md`:
- lines 11-13 describe `seed` and `scan-backed` as the current two runtime modes
- lines 23-25 present `build_candidates.py` and `scan.py` as the main working pipeline
- line 42 still says install target is `~/.claude/skills/expert-hunter.md`
- lines 49-69 still document `build_candidates.py --seed` and `build_candidates.py --from-scan ...` as the operational path
- lines 112-115 still treat `candidates_full.seed.csv` and `candidates_full.scan.csv` as the canonical outputs

This directly conflicts with:
- `/Users/timofeyzinin/egor-project/expert-hunter/SKILL.md`
- `/Users/timofeyzinin/egor-project/docs/wiki/how-it-works.md`
- `/Users/timofeyzinin/egor-project/expert-hunter/hunt.py`

### 2. The required `10/10` review result was not achieved

The active task explicitly required iteration until Codex review reached `10/10`.

`REV-017` itself says:
- round 9 still has `0 P1, 3 P2 remaining`
- remaining P2 issues are documented, not fixed

So the task's own acceptance criterion is unmet. No explicit `10/10` artifact was produced.

### 3. Some docs still misdescribe current scoring behavior

`SKILL.md` and `wiki/how-it-works.md` both say LinkedIn Activity is "not implemented" / "0 баллов".

Current code in `/Users/timofeyzinin/egor-project/expert-hunter/hunt.py`:
- lines 151-159 populate `linkedin_activity` as `5_to_10` or `1_to_4`

So the docs remain partly inaccurate even after the rewrite.

### 4. Citability follow-up code improved, but that is not enough to close the sprint

Accepted:
- disambiguator in generated queries
- URL-based matching with unique-name fallback
- stale citability reset logic
- media signal sync into `credentials_verified_or_signal`

But the sprint was broader than citability. The blocking issue is still docs-sync + mandatory review result.

## Accepted

- `/Users/timofeyzinin/egor-project/expert-hunter/SKILL.md` now documents `hunt.py` as the primary path
- `/Users/timofeyzinin/egor-project/docs/wiki/how-it-works.md` now documents the raw_search -> hunt.py -> derived_candidates flow
- `/Users/timofeyzinin/egor-project/expert-hunter/enrich_citability.py` contains the claimed Sprint 1 follow-up improvements
- `diff /Users/timofeyzinin/egor-project/expert-hunter/SKILL.md /Users/timofeyzinin/.claude/skills/expert-hunter/SKILL.md` is clean
- `python3 hunt.py --niche forex --geo US` still returns non-empty results
- `python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json` still updates candidates

## Rejected

- the claim that `SKILL.md`, `README.md`, and `how-it-works.md` now fully agree
- the claim that the cleanup sprint is complete
- the claim that the mandatory Codex review gate has been satisfied

## Next Required Fix

To close `EGOR-CLEANUP-007-S2`, Claude must:

1. fully rewrite `docs/README.md` so it matches the real current `hunt.py` pipeline and current install path
2. remove remaining stale references to `build_candidates.py --seed`, `build_candidates.py --from-scan`, and `~/.claude/skills/expert-hunter.md` from the source-of-truth docs
3. make docs consistent with current scoring behavior, including the current `linkedin_activity` heuristic
4. run the required Codex review loop to an explicit `10/10` result before returning the next deliverable
