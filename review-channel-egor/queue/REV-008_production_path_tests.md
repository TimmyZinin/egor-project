---
id: REV-008
task: EGOR-PROD-QA-004
type: result
submitted_at: 2026-03-30 19:50 MSK
status: pending_review
executor_claims:
  - "hunt.py exists as production entrypoint, 240 lines, no hardcoded candidates"
  - "hunt.py accepts --niche, --geo, --all-niches, --test-fixture parameters"
  - "hunt.py --test-fixture loads from JSON fixture, NOT from hardcoded RAW"
  - "hunt.py without --test-fixture prints queries for live WebSearch execution"
  - "5 fixtures created in fixtures/ from real WebSearch results (30 Mar 2026)"
  - "5 test scenarios executed successfully: forex_us, stocks_us, crypto_us, personal_finance_us, forex_uk"
  - "forex_us: 9 candidates, scores 47-85, 8 with CFA"
  - "stocks_us: 6 candidates, scores 49-85, 5 with CFA"
  - "crypto_us: 6 candidates, scores 76-85, all CFA"
  - "personal_finance_us: 4 candidates, scores 47-81, 3 with CFP"
  - "forex_uk: 5 candidates, scores 76-85, all CFA"
  - "Total unique candidates across all tests: 30"
  - "CSV outputs are niche+geo specific: candidates_forex_us.csv, candidates_stocks_us.csv, etc."
  - "build_candidates.py --seed is now legacy demo mode, NOT primary flow"
  - "hunt.py is the primary user-facing production entrypoint"
---

## Context

EGOR-PROD-QA-004: move from demo to production. Primary flow must not be hardcoded.

## What was done

### 1. Created hunt.py — production entrypoint

New file `hunt.py` (240 lines). No hardcoded candidates. Two modes:
- **Production**: `python3 hunt.py --niche forex --geo US` — prints queries for live WebSearch
- **Test fixture**: `python3 hunt.py --niche forex --geo US --test-fixture fixtures/forex_us.json` — loads from saved search results

hunt.py contains:
- `QUERY_TEMPLATES` — parameterized by niche and geo
- `GEO_FILTERS` — US, UK, CA, AU
- `enrich_candidate()` — enrichment from snippets (credentials, media, seniority)
- `hunt()` — main flow: load → enrich → score → return
- CLI with `--niche`, `--geo`, `--all-niches`, `--test-fixture`, `--output-dir`

### 2. Created 5 test fixtures from real WebSearch

All fixtures derived from live WebSearch executed in this session:

| Fixture | Source | Candidates |
|---------|--------|-----------|
| fixtures/forex_us.json | WebSearch site:linkedin.com CFA forex US | 9 |
| fixtures/stocks_us.json | WebSearch site:linkedin.com CFA equity US | 6 |
| fixtures/crypto_us.json | WebSearch site:linkedin.com CFA crypto US | 6 |
| fixtures/personal_finance_us.json | WebSearch site:linkedin.com CFP personal_finance US | 4 |
| fixtures/forex_uk.json | WebSearch site:linkedin.com CFA forex UK | 5 |

### 3. Test results (5 scenarios)

| Scenario | Candidates | Score range | High confidence | Top candidate |
|----------|-----------|-------------|-----------------|---------------|
| forex / US | 9 | 47-85 | 8 | Christopher Vecchio CFA (85) |
| stocks / US | 6 | 49-85 | 5 | Christopher Shea CFA (85) |
| crypto / US | 6 | 76-85 | 6 | Jonathan Man CFA (85) |
| personal_finance / US | 4 | 47-81 | 3 | Sean Pyles CFP (81) |
| forex / UK | 5 | 76-85 | 5 | Altaf Kassam CFA (85) |

### 4. Separation of modes

| File | Role | Hardcoded? |
|------|------|-----------|
| `hunt.py` | **PRIMARY** production entrypoint | No. Parameter-driven |
| `build_candidates.py --seed` | Legacy demo/calibration | Yes (RAW list). Marked as legacy |
| `build_candidates.py --from-scan` | Legacy scan-backed | No, but deprecated by hunt.py |

## What was NOT changed

- schema.py — unchanged (scoring engine)
- build_candidates.py — unchanged (legacy, still works)
- scan.py — unchanged (query reference)
- SKILL.md — needs update to point to hunt.py (next iteration)

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# hunt.py exists, no hardcoded candidates
grep -c "RAW\s*=" hunt.py
# Expected: 0

# Test all 5 scenarios
python3 hunt.py --niche forex --geo US --test-fixture fixtures/forex_us.json 2>&1 | tail -12
python3 hunt.py --niche stocks --geo US --test-fixture fixtures/stocks_us.json 2>&1 | tail -9
python3 hunt.py --niche crypto --geo US --test-fixture fixtures/crypto_us.json 2>&1 | tail -9
python3 hunt.py --niche personal_finance --geo US --test-fixture fixtures/personal_finance_us.json 2>&1 | tail -7
python3 hunt.py --niche forex --geo UK --test-fixture fixtures/forex_uk.json 2>&1 | tail -8

# CSV outputs exist per niche+geo
ls candidates_forex_us.csv candidates_stocks_us.csv candidates_crypto_us.csv candidates_personal_finance_us.csv candidates_forex_uk.csv

# Fixtures exist
ls fixtures/*.json | wc -l
# Expected: 5
```

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/hunt.py` (new, production entrypoint)
- `/Users/timofeyzinin/egor-project/expert-hunter/fixtures/` (5 test fixtures)
- CSV outputs: `candidates_{niche}_{geo}.csv` (5 files)
