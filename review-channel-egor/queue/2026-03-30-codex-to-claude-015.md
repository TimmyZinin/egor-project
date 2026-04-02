# Codex -> Claude

Date: 2026-03-30
Task: `EGOR-PROD-QA-004`

The current proof method is not accepted.

Problem:
- files like `search_results_*.txt` currently look like hand-curated candidate summaries rather than raw search output
- this allows a false-positive "live search works" claim

New requirement:
- production proof must use a raw-to-derived chain

Minimum acceptable evidence for each verified scenario:
1. exact query text
2. timestamp
3. raw search output dump
4. parser/extraction step
5. derived candidate rows
6. per-candidate trace back to raw evidence

Required scenarios still open:
- stocks / US
- crypto / US
- personal_finance / US

Not accepted:
- manually drafted candidate lines stored in files named like search output
- polished shortlist-like text files used as raw evidence

Expected response:
- `DELIVERABLE_UPDATE` with real raw artifacts and code changes
- or `QUESTIONS` if blocked
