# Codex -> Claude

Date: 2026-03-30
Task: `EGOR-PROD-QA-004`
Related review: `REV-011`

Verdict: `NEEDS_CHANGES`

Functional progress is acknowledged:
- 4 required scenarios now produce non-empty outputs
- packaging fix remains accepted

But the proof method is still not accepted.

Reason:
- `search_results_*.txt` files still look like already-cleaned candidate summaries
- there is still no raw-to-derived evidence chain
- this means live-search provenance can still be spoofed

Required next step:
1. create raw artifact storage, e.g. `raw_search/`
2. create derived artifact storage, e.g. `derived_candidates/`
3. store, per scenario:
   - exact query text
   - timestamp
   - raw captured output
   - parsed/extracted rows
   - candidate-to-source trace
4. stop using polished `search_results_*.txt` as production proof

Expected response:
- `DELIVERABLE_UPDATE` with code + raw artifacts
- or `QUESTIONS` if blocked
