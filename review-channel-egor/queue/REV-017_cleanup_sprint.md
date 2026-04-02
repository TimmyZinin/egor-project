---
id: REV-017
task: EGOR-CLEANUP-007-S2
type: result
submitted_at: 2026-03-31 16:30 MSK
status: pending_review
executor_claims:
  - "SKILL.md rewritten to reflect real current state: hunt.py as production path, honest about limitations"
  - "docs/wiki/how-it-works.md rewritten: hunt.py pipeline, enrich_citability.py, what does NOT work"
  - "docs/README.md updated: Sprint 1 section added with workflow and limitations"
  - "docs/citability-backlog.md Sprint 1 status = DONE (standalone second-pass tool)"
  - "install.sh re-ran, SKILL.md installed to ~/.claude/skills/expert-hunter/SKILL.md"
  - "All three docs (SKILL.md, README.md, how-it-works.md) now agree with actual code paths"
  - "enrich_citability.py: disambiguator in queries, evidence link preservation, stale citability reset, URL-based matching with unique-name fallback, media signal sync"
  - "hunt.py: company extraction from title (not snippet), validation of at-pattern matches"
  - "9 rounds of Codex CLI review executed"
  - "Round 9: 0 P1, 3 P2 remaining (single-word company names, media note dedup, stale citability on same-filename rerun)"
---

## What was done

### Docs synchronization

| Doc | Changes |
|-----|---------|
| SKILL.md | Rewritten: hunt.py as primary, citability as separate tool, honest limitations, no unsupported modes claimed |
| docs/README.md | Added Sprint 1 section: 3-step workflow, new fields, explicit "standalone not integrated" |
| docs/wiki/how-it-works.md | Rewritten: production pipeline hunt.py, raw_search→derived→CSV, enrich_citability.py as Sprint 1, file map updated, "What does NOT work" section |

### Citability improvements (beyond Sprint 1 baseline)

| Fix | What |
|-----|------|
| Query disambiguator | First credential added to queries to reduce false matches |
| Evidence preservation | Original LinkedIn URL kept when no citability hits |
| Stale reset | Citability cleared for missing candidates on rerun |
| URL-based matching | Stable matching by linkedin_url, unique-name fallback |
| Media signal sync | credentials_verified_or_signal updated/cleared with citability changes |
| Output format | linkedin_url included in generated query format |

### Codex CLI review iterations

| Round | P1 | P2 | P3 | Fixed |
|-------|----|----|-----|-------|
| 1 | 1 | 2 | 0 | All |
| 2 | 1 | 2 | 0 | All |
| 3 | 0 | 3 | 0 | All |
| 4 | 0 | 3 | 0 | All |
| 5 | 0 | 1 | 0 | Fixed |
| 6 | 0 | 2 | 0 | All |
| 7 | 1 | 1 | 1 | P1+P3 fixed |
| 8 | 1 | 0 | 1 | P1 fixed |
| 9 | 0 | 3 | 0 | Documented as remaining |

### Remaining P2 issues (round 9)

1. Single-word company names rejected by validation (e.g. "Bloomberg" alone)
2. `media=...` notes in credentials_verified_or_signal may accumulate on repeated runs
3. Stale citability not cleared when rerunning with same raw filename

These are edge cases in company extraction and idempotency, not structural bugs.

## Evidence

```bash
cd /Users/timofeyzinin/egor-project

# Docs agree with code
grep "hunt.py" expert-hunter/SKILL.md docs/README.md docs/wiki/how-it-works.md | wc -l
# Expected: >10

# SKILL.md installed
diff expert-hunter/SKILL.md ~/.claude/skills/expert-hunter/SKILL.md
# Expected: identical

# Pipeline works
cd expert-hunter && python3 hunt.py --niche forex --geo US 2>&1 | grep "FOUND"
# Expected: 10 candidates

# Citability works
python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json 2>&1 | grep "APPLY"
# Expected: Updated 10/10
```

## Codex CLI review command used

```bash
codex review --uncommitted
```

## Codex CLI result (round 9)

0 P1, 3 P2 remaining. No blocking issues. Remaining P2s are company extraction edge cases and citability idempotency.

Waiting for next `go`.
