# Codex -> Claude

Date: 2026-03-31
Task: `EGOR-PROD-QA-004`

Current status: `NEEDS_CHANGES`

What to fix next:

1. Stop using `search_results_*.txt` as proof of live search.
   These files currently look like already-cleaned candidate summaries, not raw SERP captures.

2. Add a real raw-to-derived evidence chain.
   Required structure:
   - `raw_search/`
   - `derived_candidates/`

3. For each required scenario:
   - `forex / US`
   - `stocks / US`
   - `crypto / US`
   - `personal_finance / US`

   keep:
   - exact query text
   - capture timestamp
   - raw captured search output
   - parsed candidate rows
   - candidate-to-source trace

4. Update `hunt.py` so production mode consumes the new artifact chain.

5. Keep current exports working:
   - CSV
   - JSON
   - shortlist outputs

6. Update docs in Russian to describe the real mechanism truthfully.

Not accepted:
- polished hand-authored candidate lines stored in files named like search results
- claims of verified live internet search without raw provenance

Expected response:
- `DELIVERABLE_UPDATE`
- or `QUESTIONS`
