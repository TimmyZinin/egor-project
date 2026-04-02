---
id: REV-016
task: EGOR-CITABILITY-006-S1
type: result
submitted_at: 2026-03-31 15:35 MSK
status: pending_review
executor_claims:
  - "docs/citability-backlog.md Sprint 1 status updated from TODO to DONE (standalone second-pass tool)"
  - "docs/README.md updated with Sprint 1 section: workflow, commands, new fields, current state, limitations"
  - "README explicitly states: standalone second-pass tool, NOT integrated into hunt.py"
  - "citability_raw/stocks_us.json created (second scenario, real WebSearch data)"
  - "enrich_citability.py --apply tested on both forex_us and stocks_us"
  - "forex_us: Mohammad Ali 53->68 (FXStreet), John Jagerson 46->61 (InvestorPlace)"
  - "stocks_us: 0 candidates gained citability (honest: institutional PMs not in media)"
  - "Backlog Sprints 2-6 remain PLANNED"
---

## Fixes from REV-015 NEEDS_CHANGES

### Fix 1: Backlog status
`docs/citability-backlog.md` Sprint 1 changed from `TODO` to `DONE (standalone second-pass tool)`.

### Fix 2: Docs updated
`docs/README.md` now has section "Citability Enrichment (Sprint 1 — реализован)" with:
- 3-step workflow (generate → operator WebSearch → apply)
- New fields listed (citability_tier, outlets, evidence_urls, raw_source)
- Explicit: "standalone second-pass tool, НЕ интегрирован в hunt.py"
- Media tiers listed
- "Протестировано на forex/US"

### Fix 3: Integration level explicit
Stated everywhere: Sprint 1 = standalone `enrich_citability.py`, NOT part of `hunt.py` default path. Operator runs it separately after initial `hunt.py` run.

### Fix 4: Second scenario
`citability_raw/stocks_us.json` created from real WebSearch (Christopher Merker found on CFA Institute blog, others not in media). Result: 0 citability upgrades for stocks (honest — these are institutional PMs).

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# Backlog status
grep "Sprint 1" ../docs/citability-backlog.md | head -2
# Expected: DONE (standalone second-pass tool)

# Docs updated
grep "Citability Enrichment" ../docs/README.md
# Expected: ## Citability Enrichment (Sprint 1 — реализован)

grep "standalone" ../docs/README.md
# Expected: standalone second-pass tool

# Two scenarios tested
ls citability_raw/*.json
# Expected: forex_us.json, stocks_us.json

# forex_us enriched
python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json 2>&1 | grep "Mohammad\|John"
# Expected: score changes visible

# stocks_us enriched
python3 enrich_citability.py --apply derived_candidates/stocks_us.json citability_raw/stocks_us.json 2>&1 | grep "APPLY"
# Expected: Updated 10/10
```

## Files for review

- `/Users/timofeyzinin/egor-project/docs/citability-backlog.md` (updated status)
- `/Users/timofeyzinin/egor-project/docs/README.md` (added Sprint 1 section)
- `/Users/timofeyzinin/egor-project/expert-hunter/citability_raw/stocks_us.json` (new)
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_stocks_us_enriched.csv` (new)
