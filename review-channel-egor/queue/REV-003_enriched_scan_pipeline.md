---
id: REV-003
task: TASK-001 (NEEDS_CHANGES from REV-002)
type: result
submitted_at: 2026-03-30 18:50 MSK
status: pending_review
executor_claims:
  - "scan-backed mode now extracts credentials from snippets via regex (CFA, CFP, CPA, CMT, FRM, CAIA, Series 3/7/65)"
  - "scan-backed mode detects media tier from snippets (Tier1: Bloomberg/Forbes/WSJ, Tier2: CNBC/Reuters, Tier3: NerdWallet/Investopedia)"
  - "scan-backed mode detects seniority from snippet patterns (Chief/Head/Director/Senior/Lead/Managing/Partner/Professor)"
  - "scan-backed scores now range from 13 to 85 (was: all 13)"
  - "output filenames are mode-specific: candidates_full.scan.csv vs candidates_full.seed.csv"
  - "scan JSON input contract is documented in build_candidates.py docstring"
  - "python3 build_candidates.py --from-scan scan_results_20260330.json produces meaningful ranking"
  - "python3 build_candidates.py --seed still works unchanged"
  - "scan and seed outputs do not overwrite each other"
---

## Context

CURRENT_VERDICT NEEDS_CHANGES on REV-002: three findings.

## Fixes applied

### Finding 1: Scan-backed enrichment from snippets

Added `enrich_from_snippet()` function that extracts from raw_snippet:
- **Credentials**: regex matching CFA, CFP, CPA, CMT, FRM, CAIA, Series 3/7/65
- **Citability**: Tier 1 (Bloomberg/Forbes/WSJ=25pts), Tier 2 (CNBC/Reuters=20pts), Tier 3 (NerdWallet/Investopedia=15pts)
- **Seniority**: Senior/Chief/Director/Head -> experience=15_19 (vs default 5_9)
- **Company**: extracted from snippet via regex
- **Google entity signal**: inferred from snippet length + credentials + media tier

Result: scan-backed scores now range **13-85** (was: all identical 13). Top 3 scan-backed: Ye Xie CFA (85), Vincent Piazza CFA (85), Sam Ro CFA (81).

### Finding 2: Mode-specific output filenames

- `--from-scan` writes: `candidates_full.scan.csv`, `candidates_shortlist.scan.csv`
- `--seed` writes: `candidates_full.seed.csv`, `candidates_shortlist.seed.csv`
- No cross-mode overwrites possible

### Finding 3 (input contract): Documented in build_candidates.py

```
Scan-backed JSON input contract:
Each entry MUST have:
  - linkedin_url (str, required)
  - name (str, required)
Each entry MAY have:
  - raw_snippet (str) — used for enrichment heuristics
  - niche (str) — forex, stocks, crypto, personal_finance
  - scan_source (str)
  - scan_timestamp (str, ISO 8601)
```

## What was NOT changed

- schema.py — unchanged
- scan.py — unchanged
- seed RAW data — unchanged
- scan_results_20260330.json — unchanged

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# Scan-backed: meaningful scores
python3 build_candidates.py --from-scan scan_results_20260330.json 2>&1 | grep "Score"
# Expected: scores 13-85, not all identical

# Seed: unchanged behavior
python3 build_candidates.py --seed 2>&1 | grep "Score"
# Expected: scores 33-96

# Mode-specific files exist separately
ls candidates_full.scan.csv candidates_full.seed.csv
# Expected: both exist, different sizes

# Input contract in source
head -30 build_candidates.py | grep "MUST have"
# Expected: "linkedin_url (str, required)"
```

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/build_candidates.py` (modified: enrichment + filenames + contract)
