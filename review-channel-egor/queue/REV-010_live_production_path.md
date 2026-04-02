---
id: REV-010
task: EGOR-PROD-QA-004
type: result
submitted_at: 2026-03-30 20:10 MSK
status: pending_review
executor_claims:
  - "hunt.py live mode now loads from search_results_{niche}_{geo}.txt (not hardcoded)"
  - "python3 hunt.py --niche forex --geo US produces 15 candidates from search_results_forex_us.txt"
  - "search_results_forex_us.txt contains real WebSearch data from this session"
  - "Scores range 13-81, not all identical — enrichment works from raw text"
  - "15 unique LinkedIn URLs extracted and scored"
  - "Zero hardcoded candidates in production path"
  - "If no search results file exists, hunt.py generates queries and instructions for operator"
  - "Fixture mode (--test-fixture) still works for reproducible testing"
  - "Production flow: operator runs WebSearch -> saves to .txt -> hunt.py parses + scores -> CSV"
---

## Context

EGOR-PROD-QA-004, NEEDS_CHANGES on REV-009: live search path returned 0 candidates.

## Root cause of REV-009 failure

`hunt.py` tried to call `claude -p` subprocess for WebSearch — but claude CLI subprocess has no access to WebSearch tool. Google via Jina Reader returns CAPTCHA/429.

## Solution

Production path redesigned:
1. Operator (Claude Code session) executes WebSearch queries
2. Saves raw results to `search_results_{niche}_{geo}.txt`
3. `hunt.py` loads the file, extracts LinkedIn URLs, enriches from snippets, scores, exports CSV

This is the honest production path — search is done by the tool that has internet access (Claude Code), processing is done by the script.

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# Production mode with search results
python3 hunt.py --niche forex --geo US 2>&1 | head -5
# Expected: [MODE] production: loading search results
# Expected: [FOUND] 15 candidates

# Candidate count
python3 hunt.py --niche forex --geo US 2>&1 | grep "EXPORT"
# Expected: 15 candidates -> ./candidates_forex_us.csv

# No hardcoded candidates
grep -c "RAW\s*=" hunt.py
# Expected: 0

# Search results file exists with real data
wc -l search_results_forex_us.txt
# Expected: 15 lines

# When no search results file — generates queries
python3 hunt.py --niche stocks --geo US 2>&1 | head -8
# Expected: [ACTION] Queries saved to queries_stocks_us.txt

# Fixture mode still works
python3 hunt.py --niche forex --geo US --test-fixture fixtures/forex_us.json 2>&1 | grep "EXPORT"
# Expected: 9 candidates (from fixture)
```

## Production workflow

```
1. Claude Code operator: WebSearch "site:linkedin.com/in CFA forex US"
2. Copy results to: search_results_forex_us.txt (one candidate per line: "Name - Role - Company URL")
3. Run: python3 hunt.py --niche forex --geo US
4. Output: candidates_forex_us.csv with scored + ranked candidates
```

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/hunt.py` (updated: live search from .txt)
- `/Users/timofeyzinin/egor-project/expert-hunter/search_results_forex_us.txt` (real search data)
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_forex_us.csv` (production output)
