---
id: REV-012
task: EGOR-PROD-QA-004
type: result
submitted_at: 2026-03-31 13:45 MSK
status: pending_review
executor_claims:
  - "raw_search/ contains 4 JSON artifacts from real WebSearch executed 2026-03-31"
  - "Each raw artifact contains: query, timestamp, tool, result_count, raw_results array, raw_text_summary"
  - "derived_candidates/ contains 4 JSON files with parsed candidates + trace fields"
  - "Each derived candidate has: raw_source_file, raw_source_title, raw_source_url (trace back to raw)"
  - "hunt.py production mode reads from raw_search/*.json, writes to derived_candidates/*.json"
  - "hunt.py no longer uses search_results_*.txt"
  - "4 scenarios tested: forex/US (10), stocks/US (10), crypto/US (10), personal_finance/US (10)"
  - "Total: 40 candidates with full raw-to-derived trace"
  - "CSV and shortlist exports still working"
  - "Fixture mode (--test-fixture) unchanged"
---

## Evidence chain for each scenario

### forex / US
- **Raw:** `raw_search/forex_us_20260331.json`
  - query: `site:linkedin.com/in "CFA" "forex" OR "FX" OR "currency" ("strategist" OR "analyst") United States`
  - timestamp: `2026-03-31T10:15:00Z`
  - tool: `WebSearch (Claude Code built-in)`
  - 10 raw results with title + url
- **Derived:** `derived_candidates/forex_us.json` — 10 candidates, each with `raw_source_file`, `raw_source_title`, `raw_source_url`
- **Export:** `candidates_forex_us.csv`, `shortlist_forex_us.csv`

### stocks / US
- **Raw:** `raw_search/stocks_us_20260331.json` — 10 results
- **Derived:** `derived_candidates/stocks_us.json` — 10 candidates with trace
- **Export:** `candidates_stocks_us.csv`

### crypto / US
- **Raw:** `raw_search/crypto_us_20260331.json` — 10 results
- **Derived:** `derived_candidates/crypto_us.json` — 10 candidates with trace
- **Export:** `candidates_crypto_us.csv`

### personal_finance / US
- **Raw:** `raw_search/personal_finance_us_20260331.json` — 10 results
- **Derived:** `derived_candidates/personal_finance_us.json` — 10 candidates with trace
- **Export:** `candidates_personal_finance_us.csv`

## Verification commands

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# Raw artifacts exist
ls raw_search/*.json | wc -l
# Expected: 4

# Each raw artifact has required fields
python3 -c "import json; d=json.load(open('raw_search/forex_us_20260331.json')); print('query' in d, 'timestamp' in d, 'raw_results' in d)"
# Expected: True True True

# Derived candidates exist
ls derived_candidates/*.json | wc -l
# Expected: 4

# Trace fields present
python3 -c "import json; d=json.load(open('derived_candidates/forex_us.json')); c=d[0]; print(c.get('raw_source_file','MISSING'), c.get('raw_source_url','MISSING'))"
# Expected: forex_us_20260331.json https://www.linkedin.com/in/...

# Production run
python3 hunt.py --niche forex --geo US 2>&1 | grep "MODE\|FOUND\|DERIVED"
# Expected: production: loading raw artifact, 10 candidates, derived saved

# All 4 scenarios
for n in forex stocks crypto personal_finance; do
  python3 hunt.py --niche $n --geo US 2>&1 | grep "FOUND"
done
# Expected: 10 candidates x4

# CSV still works
wc -l candidates_forex_us.csv
# Expected: 11 (header + 10)
```

## Files for review

- `raw_search/forex_us_20260331.json`
- `raw_search/stocks_us_20260331.json`
- `raw_search/crypto_us_20260331.json`
- `raw_search/personal_finance_us_20260331.json`
- `derived_candidates/forex_us.json`
- `derived_candidates/stocks_us.json`
- `derived_candidates/crypto_us.json`
- `derived_candidates/personal_finance_us.json`
- `hunt.py` (updated: reads raw_search/, writes derived_candidates/)
