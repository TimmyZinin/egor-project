---
id: REV-015
task: EGOR-CITABILITY-006-S1
type: result
submitted_at: 2026-03-31 15:05 MSK
status: pending_review
executor_claims:
  - "docs/citability-backlog.md created: 6 sprints defined, Russian"
  - "enrich_citability.py created: 160 lines, --generate and --apply modes"
  - "citability_raw/ directory created with forex_us.json (real WebSearch data)"
  - "Sprint 1 tested: Mohammad Ali 53->68 (FXStreet found), John Jagerson 46->61 (InvestorPlace found)"
  - "Citability now actually affects scoring in production"
  - "candidates_forex_us_enriched.csv generated with updated scores"
  - "derived_candidates/forex_us.json updated with citability_tier, citability_outlets, citability_evidence_urls, citability_raw_source"
  - "MEDIA_TIER3 expanded: added FXStreet, DailyFX, InvestorPlace"
  - "Sprint 2-6 remain PLANNED, not implemented"
---

## What was done

### 1. Backlog (docs/citability-backlog.md)
6 sprints defined:
- Sprint 1: Citability enrichment WebSearch (THIS SPRINT)
- Sprint 2: FINRA BrokerCheck verification
- Sprint 3: CFA Directory verification
- Sprint 4: University extraction
- Sprint 5: Location extraction
- Sprint 6: Native English check

### 2. Sprint 1 implementation (enrich_citability.py)

Two-phase workflow:
1. `--generate derived.json` → query file for operator
2. `--apply derived.json citability_raw.json` → enriched candidates

Tested on forex/US:
- Before: all 10 candidates citability=0, max score=53
- After: Mohammad Ali=68 (FXStreet), John Jagerson=61 (InvestorPlace)
- 8 candidates remain citability=none (honest: they're not cited in media)

New fields in derived_candidates:
- `citability_tier`: bloomberg_wsj_forbes / cnbc_reuters / niche_finance_media / none
- `citability_outlets`: ["FXStreet"] etc.
- `citability_evidence_urls`: up to 5 URLs
- `citability_raw_source`: filename for trace

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# Backlog exists
ls docs/citability-backlog.md

# Sprint 1 tool exists
python3 enrich_citability.py --help

# Generate queries
python3 enrich_citability.py --generate derived_candidates/forex_us.json
# Expected: citability_queries_forex_us.txt

# Apply citability
python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json
# Expected: Mohammad Ali score 68, John Jagerson score 61

# Enriched CSV
head -3 candidates_forex_us_enriched.csv
```

## Files for review

- `/Users/timofeyzinin/egor-project/docs/citability-backlog.md`
- `/Users/timofeyzinin/egor-project/expert-hunter/enrich_citability.py`
- `/Users/timofeyzinin/egor-project/expert-hunter/citability_raw/forex_us.json`
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_forex_us_enriched.csv`
