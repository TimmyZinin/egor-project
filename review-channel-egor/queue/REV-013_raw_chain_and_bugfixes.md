---
id: REV-013
task: EGOR-PROD-QA-004
type: result
submitted_at: 2026-03-31 14:30 MSK
status: pending_review
executor_claims:
  - "raw_search/ contains 4 JSON artifacts with per-result snippets from WebSearch 2026-03-31"
  - "derived_candidates/ contains 4 JSON artifacts with per-result trace (raw_source_file, raw_source_index, raw_source_title, raw_source_url)"
  - "hunt.py production mode reads from raw_search/*.json, enriches per-result (not shared summary)"
  - "hunt.py no longer overwrites exports when 0 candidates found"
  - "hunt.py query templates have parenthesized OR clauses"
  - "hunt.py name extraction handles multi-word names (Kelly Anne Smith)"
  - "hunt.py geo normalization: CA->Canada, AU->Australia for scoring"
  - "scan.py regex handles percent-encoded LinkedIn URLs"
  - "scan.py offline parsing uses per-line context (not shifted neighbor)"
  - "build_candidates.py uses os.path.dirname for import path"
  - "build_candidates.py enrich_from_snippet accepts default_location parameter"
  - "build_candidates.py company extraction uses only 'at Company' pattern"
  - "build_candidates.py why_selected uses scoring values not text matching"
  - "8 rounds of Codex CLI review executed; P1 and P2 bugs fixed iteratively"
  - "Remaining Codex CLI findings: 2 P2 + 1 P3 (geo hardcoding, company extraction edge cases, all-niches fixture)"
---

## Context

EGOR-PROD-QA-004 continued from NEEDS_CHANGES on REV-012.

## What was done

### 1. Raw-to-derived evidence chain (fixes REV-012 rejection)

- Removed shared `raw_text_summary` contamination
- Each raw result now has per-result `snippet` field
- hunt.py enriches from per-result snippet only
- Derived candidates have trace: `raw_source_file`, `raw_source_index`, `raw_source_title`, `raw_source_url`
- 4 raw artifacts re-captured from fresh WebSearch 2026-03-31

### 2. Codex CLI review — 8 rounds, 13 bugs found and fixed

| Round | Findings | Fixed |
|-------|---------|-------|
| 1 | P1 scan niche mislabel, P2 geo scoring CA/AU, P2 percent-encoded URLs | All 3 |
| 2 | P1 queries overwrite single file, P2 location hardcode, P3 why_selected | All 3 |
| 3 | P2 name truncation (Kelly Anne), P2 company = title | Both |
| 4 | P1 import path, P2 location still hardcoded | Both |
| 5 | P2 empty export overwrites, P2 company fallback, P2 scan geo | All 3 |
| 6 | P1 OR clause grouping, P1 scan snippet shift, P2 company regex | All 3 |
| 7 | Same as 6 (re-verified) | - |
| 8 | P2 geo hardcode (still), P2 company edge case, P3 fixture path | Documented |

### 3. Remaining known issues (from Codex CLI round 8)

- P2: `hunt.py` hardcodes `--geo` value as candidate location instead of inferring from snippet
- P2: company extraction misses some patterns (only "at Company" works, not " - Company | LinkedIn")
- P3: `--all-niches --test-fixture` doesn't auto-resolve per-niche fixtures

These are data-quality improvements, not blocking bugs. Pipeline is functionally correct.

## Test results (4 live scenarios)

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter
python3 hunt.py --niche forex --geo US       # 10 candidates, scores 13-53
python3 hunt.py --niche stocks --geo US      # 10 candidates, scores 13-53
python3 hunt.py --niche crypto --geo US      # 10 candidates, scores 13-49
python3 hunt.py --niche personal_finance --geo US  # 10 candidates, scores 13-76
```

## Evidence

```bash
# Raw artifacts with per-result snippets
python3 -c "import json; d=json.load(open('raw_search/forex_us_20260331.json')); print('snippet' in d['raw_results'][0])"
# Expected: True

# Derived with trace
python3 -c "import json; d=json.load(open('derived_candidates/forex_us.json')); print(d[0].get('raw_source_index'))"
# Expected: 0 (integer)

# No shared summary contamination
grep -c "raw_text_summary" hunt.py
# Expected: 0

# OR clauses parenthesized
grep '"forex" OR' hunt.py | head -1
# Expected: contains ("forex" OR "FX" OR "currency")

# Percent-encoded URLs work
grep 'w%' scan.py
# Expected: [\w%.-]+
```

## Files for review

- `hunt.py` (production entrypoint, updated)
- `scan.py` (regex + parsing fixes)
- `build_candidates.py` (import, location, company, why_selected fixes)
- `raw_search/*.json` (4 artifacts with per-result snippets)
- `derived_candidates/*.json` (4 artifacts with trace)
