# Спецификация: скилл `/broker-checker`

> Версия: 1.0 | Дата: 2026-04-02
> Статус: SPEC (не реализован)
> Автор: Claude (executor session, task EGOR-BROKER-WRITER-RESEARCH-008)

---

## Назначение

Скилл `/broker-checker` — **независимый ревьюер** черновиков broker review. Проверяет структуру, факты, SEO, compliance и гуманизацию. Выносит вердикт: `APPROVED`, `NEEDS_CHANGES` или `REJECTED`.

Скилл **проверяет**, но **не пишет** и **не публикует**.

Название `/broker-checker` (не `/broker-reviewer`) выбрано намеренно: этот скилл — проверяющий/чекер, а не рецензент в редакционном смысле. Он автоматизирует quality gate, не даёт субъективную оценку.

---

## Почему отдельный скилл, а не часть writer

1. **Независимость оценки.** Скилл, проверяющий собственный output — не проверка. Доказано на `review-channel-egor/`: Codex (независимый ревьюер) ловит ошибки, которые Claude (writer) пропускает.
2. **Разные prompt-контексты.** Writer оптимизирован на генерацию. Checker — на критический анализ. Совмещение ухудшает оба.
3. **Разные входные данные.** Checker сверяет черновик с input.json (fact-check), а не генерирует из него.
4. **Audit trail.** Отдельные review-файлы = прозрачная история проверок.

---

## Входные данные

| Вход | Формат | Описание |
|------|--------|----------|
| `content/{slug}/draft-v{N}.md` | Markdown | Черновик для проверки |
| `quality/criteria.json` | JSON | Чеклист критериев проверки (с severity) |
| `brokers/{slug}/input.json` | JSON | Данные брокера для fact-checking |
| `templates/broker-review.md` | Markdown | Шаблон для проверки структурной полноты |
| `quality/humanization-patterns.md` | Markdown | Паттерны AI-текста для детекции |

---

## Выходные данные

### 1. Отчёт проверки: `content/{slug}/review-v{N}.md`

Структура отчёта:

```markdown
# Review: {broker_name} — Draft v{N}

**Verdict:** APPROVED | NEEDS_CHANGES | REJECTED
**Reviewed at:** {ISO datetime}
**Word count:** {N}

## Structural Check

| # | Секция | Присутствует | Замечание |
|---|--------|:---:|-----------|
| 1 | Hero | ✅ | — |
| 2 | Verdict Box | ✅ | — |
| ... | ... | ❌ | Отсутствует |

Missing sections: {N} of 18

## Factual Check

| Claim in draft | Source value (input.json) | Match? |
|---------------|-------------------------|:------:|
| "spread from 0.6 pips" | spreads.eurusd_avg: 0.6 | ✅ |
| "regulated by 3 bodies" | regulators: 4 items | ❌ MISMATCH |

Mismatches: {N}

## SEO Check

- [ ] H1 содержит broker_name + year
- [ ] ≥3 H2 содержат target keywords
- [ ] Meta description placeholder присутствует
- [ ] Internal link плейсхолдеры: {count} (min: 10)
- [ ] FAQ ≥5 вопросов
- [ ] Schema.org JSON-LD присутствует и валиден

SEO issues: {N}

## Compliance Check

- [ ] CFD/forex risk disclaimer
- [ ] "Not financial advice" disclaimer
- [ ] Author attribution block
- [ ] Methodology section

Compliance issues: {N}

## Humanization Check

| Паттерн | Найден? | Где |
|---------|:-------:|-----|
| Generic transition words | ✅ | paragraph 3, 7 |
| Adjective lists | ❌ | — |
| ... | ... | ... |

AI patterns detected: {N}

## Schema.org Check

- [ ] Review type present + valid
- [ ] Article type present
- [ ] Product type present
- [ ] FAQPage type present + ≥5 questions
- [ ] BreadcrumbList present

Schema issues: {N}

## Summary

| Категория | Критических | Высоких | Средних |
|-----------|:-----------:|:-------:|:-------:|
| Structure | 0 | 1 | 0 |
| Facts | 1 | 0 | 0 |
| SEO | 0 | 0 | 2 |
| Compliance | 0 | 0 | 0 |
| Humanization | 0 | 2 | 1 |
| Schema | 0 | 0 | 1 |

## Required Changes (если NEEDS_CHANGES)

1. [P0/CRITICAL] Исправить количество регуляторов: в тексте "3", в input.json "4"
2. [P1/HIGH] Убрать AI pattern "Furthermore" в параграфе 3
3. ...
```

### 2. Обновление манифеста: `content/manifest.json`

Транзакции:
- `drafted` / `revised` → `approved` (при APPROVED)
- `drafted` / `revised` → `revision_requested` (при NEEDS_CHANGES)
- `drafted` / `revised` → `rejected` (при REJECTED)

При APPROVED: checker копирует draft в `content/{slug}/approved.md`.

### 3. Git-коммит

Формат: `review({slug}): v{N} — {VERDICT}`

---

## Критерии проверки: severity

### P0 (Critical) — блокирует публикацию

- Фактическая ошибка в числах (спреды, комиссии, регуляторы)
- Отсутствует compliance disclaimer
- Schema.org JSON-LD невалиден или отсутствует
- Отсутствуют ≥3 обязательные секции из 18

### P1 (High) — требует исправления

- ≥3 AI паттерна обнаружены
- Нет Expert Take blockquote
- <5 FAQ вопросов
- <10 internal link плейсхолдеров
- Word count <3500

### P2 (Medium) — рекомендация

- 1-2 AI паттерна обнаружены
- Отдельные секции слишком короткие
- Стилистические замечания

### Логика вердикта

```
IF P0 issues > 0: REJECTED
ELIF P1 issues > 0: NEEDS_CHANGES
ELSE: APPROVED
```

---

## Ahrefs-интеграция в checker

### Что checker делает сам (без Ahrefs)

- Структурная проверка (18 секций)
- Factual check (draft vs input.json)
- SEO structure check (headings, keywords, internal links)
- Compliance check (disclaimers, attribution)
- Humanization check (24 AI patterns)
- Schema.org validation

### Что checker НЕ делает (→ человек + Ahrefs)

Checker **не запускает Ahrefs AI detection**. Причины:

1. **Нет API-эндпоинта.** Ahrefs API v3 не имеет endpoint для AI content detection (подтверждено апрель 2026, docs.ahrefs.com/api).
2. **Free detector — web-only.** Только вставка текста через браузер, нет программного доступа.
3. **AI detection ≠ quality gate.** Accuracy ~80-85% (industry estimate). False positives отклонят хороший контент. Используется как сигнал, не как gatekeeper.

### Как Ahrefs-результаты входят в процесс

1. Checker выносит вердикт (APPROVED/NEEDS_CHANGES/REJECTED) **без Ahrefs**.
2. Если APPROVED → человек вручную проверяет через Ahrefs Free AI Detector (web).
3. Результат Ahrefs записывается в `quality/ahrefs-checks/{slug}.json` (ручной ввод).
4. Если AI score выше порога → человек возвращает в writer для дополнительной гуманизации.
5. Ahrefs **не блокирует** state machine автоматически.

---

## Чего скилл НЕ делает

- НЕ модифицирует черновик (read-only доступ к draft-файлам)
- НЕ генерирует контент
- НЕ запускает Ahrefs API / web tools
- НЕ принимает решение о публикации (→ человек)
- НЕ проверяет визуальное отображение / рендеринг

---

## Формат criteria.json

```json
{
  "version": "1.0",
  "criteria": [
    {
      "id": "struct-sections",
      "category": "structure",
      "check": "All 18 template sections present",
      "severity_if_fail": "P0 if ≥3 missing, P1 if 1-2 missing"
    },
    {
      "id": "fact-numbers",
      "category": "facts",
      "check": "All numeric claims match input.json",
      "severity_if_fail": "P0"
    },
    {
      "id": "seo-faq-count",
      "category": "seo",
      "check": "≥5 FAQ questions",
      "severity_if_fail": "P1"
    },
    {
      "id": "compliance-disclaimer",
      "category": "compliance",
      "check": "CFD/forex risk disclaimer present",
      "severity_if_fail": "P0"
    },
    {
      "id": "humanize-patterns",
      "category": "humanization",
      "check": "No AI patterns from humanization-patterns.md detected",
      "severity_if_fail": "P1 if ≥3, P2 if 1-2"
    },
    {
      "id": "schema-valid",
      "category": "schema",
      "check": "JSON-LD contains Review + Article + Product + FAQPage + Breadcrumb",
      "severity_if_fail": "P0"
    }
  ]
}
```

---

## Защита от race conditions

- Checker может работать только если manifest.state ∈ {`drafted`, `revised`}
- При неправильном state → скилл выходит с ошибкой
- Writer и checker НИКОГДА не запускаются одновременно на одном {slug}
- Манифест обновляется атомарно с git-коммитом
