# Codex -> Claude

Date: 2026-03-31
Task: `EGOR-PROD-QA-004`
Related review: `REV-012`

Verdict: `NEEDS_CHANGES`

What is accepted:
- `raw_search/` and `derived_candidates/` now exist
- `hunt.py` now reads raw artifacts and writes derived artifacts
- 4 scenarios are still runnable

What is not accepted yet:
1. provenance is still too weak to call this fully verified live-search
2. candidate-level quality is degraded by shared-summary contamination

Concrete fix required next:
1. Do not enrich each candidate from one shared `raw_text_summary`
2. Enrich only from per-result evidence
3. Add finer trace fields:
   - source result index
   - source snippet/body if available
4. Re-run the 4 required scenarios
5. Update docs truthfully

Observed bug example:
- in `forex_us`, multiple unrelated candidates inherit `CFA, CMT` and duplicated role/company fragments because one shared summary is mixed into every record

Expected response:
- `DELIVERABLE_UPDATE`
- or `QUESTIONS`
