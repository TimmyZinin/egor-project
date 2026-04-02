# NEXT TASK FOR CLAUDE

CONTEXT
- Goal: build a working Claude Code skill for expert discovery and selection.
- Repo: current `egor-project`.
- Source of truth: `review-channel/COPYPASTE_PROTOCOL.md`.
- This iteration is implementation-focused, not research-focused.

TASK
- Build an MVP skill that finds and ranks expert candidates for:
  - `forex`
  - `stocks`
  - `crypto`
  - `personal finance`
- Geo focus:
  - `US`
  - other English-speaking markets as secondary
- Required output:
  - full candidate dataset
  - shortlist top-20
  - default export as `CSV`
- Every selected row must include:
  - `name`
  - `linkedin_url`
  - `primary_role`
  - `company`
  - `location`
  - `niche_tags`
  - `credentials_claimed`
  - `credentials_verified_or_signal`
  - `evidence_links`
  - `fit_score`
  - `fit_notes`
  - `why_selected`
  - `confidence`
  - `status`

EGOR CRITERIA TO IMPLEMENT
- citability
- passed exams / credentials
- membership in associations
- university
- native English
- location (`US, UK + ?`)
- public digital footprint is required

IMPLEMENTATION RULES
- Do not build outreach.
- Do not build anti-AI detection.
- Do not return a long spec instead of code.
- Use explainable rule-based scoring for MVP.
- Keep `claimed` separate from `verified_or_signal`.
- It is acceptable to use mixed verification:
  - verified where possible
  - evidence/signal-based where direct verification is not available

MVP EXPECTATION
- One working skill command or entry point.
- One normalized output schema.
- One CSV export path.
- One shortlist generation path.
- Minimal docs only to explain how to run it.

PREFERRED EXECUTION PLAN
1. Inspect repo and choose the correct skill layout.
2. Implement normalized candidate schema.
3. Implement source adapters for MVP-safe sources already available in repo/environment.
4. Implement rule-based scoring using Egor criteria.
5. Export:
  - full results CSV
  - shortlist CSV
6. Provide one test/demo command and one sample output.

DO NOT DO
- no HTML research report as primary deliverable
- no expert panel simulation
- no outreach templates
- no unsupported legal claims
- no fake stats

RETURN FORMAT
- Return only `DELIVERABLE_UPDATE` or `QUESTIONS_FOR_CODEX`.

ACCEPTANCE CRITERIA
- There is actual code in repo, not only markdown.
- The skill can be run locally.
- The skill outputs CSV.
- LinkedIn URLs are present in the result.
- The shortlist is explainable.
