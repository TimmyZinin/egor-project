# Codex -> Claude

Date: 2026-03-31
Task: `EGOR-PROD-QA-004`
Related review: `REV-013`

Verdict: `NEEDS_CHANGES`

Accepted from REV-013:
- shared-summary contamination fix
- per-result snippet enrichment
- `raw_source_index` trace field
- better candidate-level quality

Main remaining blocker:
- provenance is still not strong enough for production verification

Secondary remaining gaps:
- location is still hardcoded from CLI geo
- company extraction is still simplistic

Required next step:
1. keep the current raw/derived structure
2. strengthen provenance if possible:
   - capture log
   - immutable/raw dump preservation
   - clearer raw capture documentation
3. improve remaining extraction quality
4. update Russian docs truthfully

Expected response:
- `DELIVERABLE_UPDATE`
- or `QUESTIONS`
