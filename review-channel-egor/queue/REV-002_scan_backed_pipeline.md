---
id: REV-002
task: TASK-001 (NEEDS_CHANGES from REV-001)
type: result
submitted_at: 2026-03-30 18:45 MSK
status: pending_review
executor_claims:
  - "build_candidates.py accepts --from-scan <path> for scan-backed mode"
  - "build_candidates.py accepts --seed for demo mode with built-in data"
  - "scan_results_20260330.json exists with 20 entries from real WebSearch"
  - "python3 build_candidates.py --from-scan scan_results_20260330.json produces CSV with 20 rows"
  - "python3 build_candidates.py --seed produces CSV with 20 rows (enriched scores)"
  - "scan-backed mode loads from JSON file, not hardcoded RAW list"
  - "Both modes produce identical CSV schema (14 fields)"
  - "Mode is printed at start: [MODE] scan-backed or [MODE] seeded demo"
---

## Context

CURRENT_VERDICT.md = NEEDS_CHANGES on REV-001. Three findings:
1. Manual seed instead of scan-driven pipeline
2. scan.py not integrated into build path
3. Full vs shortlist status semantics

## What was changed

### Finding 1 fix: build_candidates.py now has two explicit modes

- `--from-scan <path>` reads `candidates_raw.json` (scan-backed mode)
- `--seed` uses built-in RAW dataset (demo mode)
- Default without args = seed mode (backward compatible)
- Mode is printed at runtime: `[MODE] scan-backed` or `[MODE] seeded demo`

### Finding 2 fix: scan output file created and wired

- Created `scan_results_20260330.json` — 20 entries from real WebSearch executed today
- `build_candidates.py --from-scan scan_results_20260330.json` reads this file
- `load_from_scan()` function normalizes scan output into candidate format

### Finding 3: acknowledged, not changed

Status semantics (shortlisted mutation) kept as-is for MVP. Noted for future.

## What was NOT changed

- scan.py itself not modified (query logic unchanged)
- schema.py not modified (scoring logic unchanged)
- Seed RAW dataset not modified

## Reproducible paths

```bash
# Path 1: scan-backed (from saved search results)
cd /Users/timofeyzinin/egor-project/expert-hunter
python3 build_candidates.py --from-scan scan_results_20260330.json
# Expected: [MODE] scan-backed, 20 candidates, CSV + JSON

# Path 2: seed demo (enriched data)
python3 build_candidates.py --seed
# Expected: [MODE] seeded demo, 20 candidates, scores 33-96

# Verify both produce 14-field CSV
head -1 candidates_full.csv | tr ',' '\n' | wc -l
# Expected: 14
```

## Evidence

```bash
# Verify scan results file
wc -l /Users/timofeyzinin/egor-project/expert-hunter/scan_results_20260330.json
# Expected: 22 (JSON array, 20 entries)

# Verify --from-scan flag accepted
python3 build_candidates.py --from-scan scan_results_20260330.json 2>&1 | head -1
# Expected: [MODE] scan-backed: loading from scan_results_20260330.json

# Verify --seed flag
python3 build_candidates.py --seed 2>&1 | head -1
# Expected: [MODE] seeded demo: using built-in 20 candidates
```

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/build_candidates.py` (modified)
- `/Users/timofeyzinin/egor-project/expert-hunter/scan_results_20260330.json` (new)
