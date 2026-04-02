---
id: REV-001
task: TASK-001
type: result
submitted_at: 2026-03-30 18:32 MSK
status: pending_review
executor_claims:
  - "schema.py exists at egor-project/expert-hunter/schema.py, 157 lines"
  - "build_candidates.py exists at egor-project/expert-hunter/build_candidates.py, runnable with python3"
  - "candidates_full.csv has 21 lines (header + 20 candidates)"
  - "candidates_shortlist.csv has 21 lines (header + 20 candidates sorted by fit_score)"
  - "candidates_full.json has 20 entries"
  - "Top candidate: Nik Bhatia CFA CMT, score 96"
  - "12 out of 20 candidates have formal credentials (CFA/CFP/CPA/FRM)"
  - "All 20 candidates have LinkedIn URLs"
  - "Scoring is rule-based with 8 categories totaling max 100"
  - "CSV schema matches PROTOCOL.md Output Schema (14 fields)"
---

## Context

CURRENT_TASK.md requested MVP of /expert-hunter: runnable code, CSV export, shortlist top-20, LinkedIn URLs, explainable scoring.

## Source of truth files read

- review-channel-egor/PROTOCOL.md
- review-channel-egor/CURRENT_TASK.md
- review-channel-egor/CURRENT_VERDICT.md

## What was done

### 1. Code created

```
egor-project/expert-hunter/
  schema.py           -- ExpertCandidate dataclass, scoring logic, CSV/JSON export, shortlist function
  scan.py             -- SCAN module with WebSearch queries per niche, LinkedIn URL parser
  build_candidates.py -- Builds dataset from real WebSearch results, scores, exports CSV + JSON
```

### 2. Real search executed

4 parallel WebSearch queries across 4 niches (forex, stocks, crypto, personal_finance) + 3 supplementary queries. Total: 7 searches, ~45 raw results, 20 unique quality candidates after dedup.

### 3. Scoring model implemented

8 categories, raw points, max 100:

| Category | Max | What it measures |
|----------|-----|------------------|
| citability | 25 | Media mentions (Bloomberg/Forbes = 25, none = 0) |
| credentials | 20 | CFA=20, CFP=18, CPA=16, multiple = bonus capped at 20 |
| google_entity | 15 | Knowledge Panel=15, Scholar=12, SERP presence=7 |
| associations | 10 | CFA Institute=10, FPA=8, NAPFA=9 |
| linkedin_activity | 10 | Posts/month + articles bonus |
| experience_years | 10 | 20+=10, 15-19=8, etc |
| location | 5 | US/UK=5, CA/AU=3, other=0 |
| native_english | 5 | Confirmed=5, likely=4, fluent=3 |

### 4. Output files generated

| File | Lines | Content |
|------|-------|---------|
| candidates_full.csv | 21 | All 20 candidates, sorted by score |
| candidates_full.json | 20 entries | Same data, JSON format |
| candidates_shortlist.csv | 21 | Top 20 (= all in this batch) |
| candidates_shortlist.json | 20 entries | Same |

### 5. Shortlist (top 12 with score >= 60)

| # | Score | Name | Credentials | Company | Niche |
|---|-------|------|-------------|---------|-------|
| 1 | 96 | Nik Bhatia, CFA, CMT | CFA, CMT | The Bitcoin Layer | crypto |
| 2 | 92 | Liz Weston, CFP | CFP | ex-NerdWallet | personal finance |
| 3 | 88 | Sam Ro, CFA | CFA | TKer (Substack) | stocks, macro |
| 4 | 85 | Ye Xie, CFA | CFA | BMO Capital Markets | forex |
| 5 | 84 | Hal M. Bundrick, CFP | CFP | Yahoo Finance | personal finance |
| 6 | 83 | Marta Norton, CFA | CFA | Empower | investment |
| 7 | 82 | Tom Garretson, CFA | CFA | RBC Wealth Management | fixed income |
| 8 | 81 | Vincent G. Piazza, CFA | CFA | Bloomberg Intelligence | stocks |
| 9 | 74 | Bud Haslett, CFA, FRM | CFA, FRM | FOMO-FUD Digital Assets | crypto |
| 10 | 72 | Kirk David Phillips, CPA | CPA | Crypto Bullseye Zone | crypto tax |
| 11 | 69 | Sofien Kaabar, CFA | CFA | BBSP Research | forex, quant |
| 12 | 64 | Sean Pyles, CFP | CFP | NerdWallet | personal finance |

## What was NOT done

- No outreach (out of scope per PROTOCOL.md)
- No FINRA BrokerCheck verification (planned for next iteration)
- No Jina Reader enrichment of individual profiles (rate limit concern for 20 profiles)
- Skill .md file for ~/.claude/skills/ not yet created (code-first approach)
- scan.py offline mode not tested (needs pre-fetched search results)

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/schema.py`
- `/Users/timofeyzinin/egor-project/expert-hunter/build_candidates.py`
- `/Users/timofeyzinin/egor-project/expert-hunter/scan.py`
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_full.csv`
- `/Users/timofeyzinin/egor-project/expert-hunter/candidates_shortlist.csv`

## Evidence

```bash
# Verify files exist
ls -la /Users/timofeyzinin/egor-project/expert-hunter/*.py
ls -la /Users/timofeyzinin/egor-project/expert-hunter/*.csv

# Verify CSV line counts
wc -l /Users/timofeyzinin/egor-project/expert-hunter/candidates_full.csv
# Expected: 21

# Verify runnable
cd /Users/timofeyzinin/egor-project/expert-hunter && python3 build_candidates.py
# Expected: prints shortlist, generates CSV + JSON

# Verify all candidates have LinkedIn URLs
python3 -c "import json; d=json.load(open('candidates_full.json')); print(all(c['linkedin_url'].startswith('https://www.linkedin.com/in/') for c in d))"
# Expected: True

# Verify schema has 14 fields
head -1 candidates_full.csv | tr ',' '\n' | wc -l
# Expected: 14
```

## Residual risks

- 20 candidates is below the 200+ target for full pipeline — this is MVP seed data
- Scoring based on search snippet signals, not full profile verification
- Some credentials marked "claimed" not yet verified against registries
- Non-US candidates (Sofien Kaabar, Adam Nasli) may have lower data quality
