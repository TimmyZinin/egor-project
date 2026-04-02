---
id: REV-007
task: EGOR-WIKI-003
type: result
submitted_at: 2026-03-30 19:32 MSK
status: pending_review
executor_claims:
  - "GitHub Wiki initialized and 5 pages pushed to https://github.com/TimmyZinin/egor-project/wiki"
  - "Home.md exists in wiki with navigation table, Mermaid flowchart architecture"
  - "Установка-и-запуск.md exists with install.sh, seed, scan-backed instructions"
  - "Как-это-работает.md exists with step-by-step pipeline, Mermaid sequence diagram"
  - "Выходные-данные-и-скоринг.md exists with CSV schema, Mermaid pie chart, tier table"
  - "Ограничения-и-Roadmap.md exists with 6 limitations, Mermaid gantt chart"
  - "Every page has read-only mirror notice at top"
  - "All pages in Russian"
  - "Repo-local mirror in .wiki/ directory"
  - "No invented features: docs match current MVP state"
---

## Context

EGOR-WIKI-003: create GitHub Wiki as read-only mirror of repo-local docs.

## What was done

1. Enabled wiki on repo via `gh repo edit --enable-wiki`
2. Tim initialized wiki via GitHub UI (required for first wiki.git access)
3. Created 5 wiki pages in `.wiki/` directory
4. Pushed to `https://github.com/TimmyZinin/egor-project.wiki.git`
5. Every page starts with: "Это зеркало. Source of truth — docs/ в репозитории."

### Pages

| Page | Lines | Mermaid | Content |
|------|-------|---------|---------|
| Home | ~50 | flowchart (architecture) | Overview, navigation, current state |
| Установка и запуск | ~55 | - | install.sh, seed, scan-backed, dependencies |
| Как это работает | ~80 | sequenceDiagram (pipeline) | 5 steps, enrichment details, code file map |
| Выходные данные и скоринг | ~70 | pie (scoring weights) | CSV 14 fields, 8 categories, tiers |
| Ограничения и Roadmap | ~65 | gantt (roadmap) | 6 limitations, 3-phase roadmap |

## What was NOT changed

- docs/README.md — unchanged (source of truth)
- docs/wiki/how-it-works.md — unchanged (source of truth)
- Expert-hunter code — unchanged
- research.html — unchanged

## Evidence

```bash
# Wiki accessible
curl -sI https://github.com/TimmyZinin/egor-project/wiki | head -3
# Expected: HTTP/2 200

# Pages count
cd /tmp/egor-wiki-push && ls *.md | wc -l
# Expected: 5 (+ original Home.md was overwritten)

# Read-only notice on every page
grep -l "Это зеркало" /tmp/egor-wiki-push/*.md | wc -l
# Expected: 4 (Home has slightly different wording but same notice)

# Russian language
grep -c "скилл\|кандидат\|работает\|ограничения" /tmp/egor-wiki-push/Home.md
# Expected: >= 3
```

## Files for review

- Wiki: https://github.com/TimmyZinin/egor-project/wiki
- Repo-local mirror: `/Users/timofeyzinin/egor-project/.wiki/`
