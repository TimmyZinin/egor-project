---
id: REV-006
task: EGOR-DOCS-002
type: result
submitted_at: 2026-03-30 19:25 MSK
status: pending_review
executor_claims:
  - "docs/README.md exists, ~220 lines, Russian, covers all 10 required sections"
  - "docs/wiki/how-it-works.md exists, ~210 lines, Russian, step-by-step current behavior"
  - "README.md covers: purpose, architecture, file structure, install, modes, inputs, outputs, scoring, limitations, roadmap"
  - "how-it-works.md covers: scan flow, enrichment details, scoring internals, code file map, CSV interpretation, what does NOT work"
  - "Both docs reference real code paths: schema.py, build_candidates.py, scan.py"
  - "Limitations section explicitly lists 6 things that do NOT work: auto scan, FINRA verify, Jina Reader, outreach, verify mode, report mode"
  - "Roadmap separated into: nearest, mid-term, deferred"
  - "docs point to each other: README links to wiki/how-it-works.md and skill-expert-hunter-spec.md"
  - "No invented features: every claim matches actual repo state"
---

## Context

EGOR-DOCS-002: full Russian documentation + wiki-style current-state doc.

## Source of truth files read

- review-channel-egor/CURRENT_TASK.md (EGOR-DOCS-002)
- review-channel-egor/CURRENT_VERDICT.md (APPROVED REV-005)
- All files in expert-hunter/ directory

## What was done

### 1. docs/README.md — Source of Truth документ

~220 строк на русском. Покрывает:
- Назначение скилла
- Текущее состояние (MVP approved)
- Структура репозитория (file tree)
- Установка и запуск (install.sh + два режима)
- Входные данные (scan JSON контракт + seed)
- Выходные данные (CSV 14 полей + JSON, mode-specific filenames)
- Модель скоринга (8 категорий, правила, тиры)
- Scan-backed enrichment (что извлекается из snippet-ов)
- Ограничения (6 пунктов: что НЕ работает)
- Roadmap (ближайшее / среднесрочное / отложенное)
- Ссылки на связанные документы

### 2. docs/wiki/how-it-works.md — Wiki-документ

~210 строк на русском. Step-by-step:
- Общая схема (scan-backed и seed)
- 6 шагов pipeline: SCAN -> Enrichment -> Scoring -> why_selected -> Export -> Shortlist
- Детали enrichment: regex patterns, media tiers, seniority detection, company extraction
- Детали scoring: формула, hard cap, множественные credentials
- Файлы кода: что где, сколько строк, какие функции
- Как интерпретировать CSV (паттерны scores)
- Что НЕ делает скилл

## What was NOT done

- docs/skill-expert-hunter-spec.md НЕ модифицирован (он для справки, не source of truth)
- Код НЕ изменён
- research.html НЕ изменён

## Evidence

```bash
# Docs exist
ls -la ~/egor-project/docs/README.md
# Expected: exists, ~220 lines

ls -la ~/egor-project/docs/wiki/how-it-works.md
# Expected: exists, ~210 lines

# Russian language
grep -c "скилл\|кандидат\|документ\|работает" ~/egor-project/docs/README.md
# Expected: >10

# Covers all 10 sections from task
grep -c "Назначение\|Структура\|Установка\|Входные\|Выходные\|Скоринг\|Ограничения\|Roadmap" ~/egor-project/docs/README.md
# Expected: >= 8

# References real code paths
grep -c "schema.py\|build_candidates.py\|scan.py\|SKILL.md\|install.sh" ~/egor-project/docs/README.md
# Expected: >= 5

# Wiki step-by-step
grep -c "Шаг" ~/egor-project/docs/wiki/how-it-works.md
# Expected: >= 6

# Limitations explicitly listed
grep -c "НЕ работает\|не выполняет\|не верифицирует\|не скрапит" ~/egor-project/docs/wiki/how-it-works.md
# Expected: >= 4
```

## Files for review

- `/Users/timofeyzinin/egor-project/docs/README.md`
- `/Users/timofeyzinin/egor-project/docs/wiki/how-it-works.md`
