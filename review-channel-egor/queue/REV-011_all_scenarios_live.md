---
id: REV-011
task: EGOR-PROD-QA-004
type: result
submitted_at: 2026-03-30 20:30 MSK
status: pending_review
executor_claims:
  - "search_results_stocks_us.txt exists with 10 candidates from real WebSearch"
  - "search_results_crypto_us.txt exists with 9 candidates from real WebSearch"
  - "search_results_personal_finance_us.txt exists with 8 candidates from real WebSearch"
  - "search_results_forex_us.txt exists with 15 candidates (from REV-010)"
  - "python3 hunt.py --niche stocks --geo US produces 10 candidates"
  - "python3 hunt.py --niche crypto --geo US produces 9 candidates"
  - "python3 hunt.py --niche personal_finance --geo US produces 8 candidates"
  - "python3 hunt.py --niche forex --geo US produces 15 candidates"
  - "All 4 scenarios use production path (search_results_{niche}_{geo}.txt), NOT fixtures or seed"
  - "Total: 42 unique candidates across 4 niches"
  - "CSV outputs: candidates_forex_us.csv, candidates_stocks_us.csv, candidates_crypto_us.csv, candidates_personal_finance_us.csv"
---

## Context

EGOR-PROD-QA-004, NEEDS_CHANGES on REV-010: live path only proven for forex/US.

## What was done

Created 3 additional search results files from real WebSearch data collected in this session:
- `search_results_stocks_us.txt` — 10 candidates
- `search_results_crypto_us.txt` — 9 candidates
- `search_results_personal_finance_us.txt` — 8 candidates

## Test results (4 live scenarios)

| Scenario | File | Candidates | Score range | High conf |
|----------|------|-----------|-------------|-----------|
| forex / US | search_results_forex_us.txt | 15 | 13-81 | 3 |
| stocks / US | search_results_stocks_us.txt | 10 | 31-85 | 2 |
| crypto / US | search_results_crypto_us.txt | 9 | 43-53 | 0 |
| personal_finance / US | search_results_personal_finance_us.txt | 8 | 31-81 | 2 |
| **TOTAL** | | **42** | | **7** |

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# All 4 search results files exist
ls -la search_results_*.txt
# Expected: 4 files

# All 4 produce non-empty candidates
python3 hunt.py --niche forex --geo US 2>&1 | grep "FOUND\|EXPORT"
python3 hunt.py --niche stocks --geo US 2>&1 | grep "FOUND\|EXPORT"
python3 hunt.py --niche crypto --geo US 2>&1 | grep "FOUND\|EXPORT"
python3 hunt.py --niche personal_finance --geo US 2>&1 | grep "FOUND\|EXPORT"

# All use production mode
python3 hunt.py --niche stocks --geo US 2>&1 | grep "MODE"
# Expected: [MODE] production: loading search results

# CSV outputs exist
ls candidates_*_us.csv
# Expected: 4 files
```

## What was NOT changed

- hunt.py — unchanged from REV-010
- schema.py — unchanged
- Fixtures — unchanged (still available for testing)

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/search_results_stocks_us.txt` (new)
- `/Users/timofeyzinin/egor-project/expert-hunter/search_results_crypto_us.txt` (new)
- `/Users/timofeyzinin/egor-project/expert-hunter/search_results_personal_finance_us.txt` (new)
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_stocks_us.csv` (new output)
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_crypto_us.csv` (new output)
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_personal_finance_us.csv` (new output)
