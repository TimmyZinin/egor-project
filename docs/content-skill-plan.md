# План: Скилл генерации контента для проекта Егора

> Пересмотрен после internal adversarial review.
> Основные изменения: отказ от external dependency как base, first-party skill, реалистичные сроки.

## Вердикт: First-party skill + заимствования

НЕ использовать `ivankuznetsov/claude-seo` как base (4 stars, 16 commits, supplier risk).
Написать собственный `/broker-writer` skill, заимствуя humanization patterns из claude-seo как reference.

## Найденные готовые решения (reference, не base)

### ivankuznetsov/claude-seo
- **URL:** https://github.com/ivankuznetsov/claude-seo
- **Статус:** 4 stars, 1 fork, 16 commits, v1.0.0 (11 Mar 2026) — новый solo project
- **Полезно заимствовать:** 24 AI humanization паттерна (из Wikipedia guidelines), workflow structure
- **НЕ использовать как base:** supplier risk, fragile cross-skill chaining

### ahrefs/ahrefs-api-skills (official)
- **URL:** https://github.com/ahrefs/ahrefs-api-skills
- **Полезно:** Keyword research, SERP analysis, Site Audit data
- **AI detection:** No confirmed public API endpoint for AI content detection found in docs (as of Apr 2026)
- **Есть:** Brand Radar API `GET /v3/brand-radar/ai-responses` для мониторинга AI citations
- **API v3 доступ:** на paid plans starting from Lite (не только Enterprise, как было в первой версии)

### Другие (reference only)
- `arturseo-geo/content-creation-skill` — шаблоны контента
- `seomachine` — workspace для long-form SEO
- `seo-geo-claude-skills` — 20 SEO/GEO скиллов
- Ahrefs AI Content Helper — web tool для SEO-оптимизации текста

## Рекомендуемая стратегия (editorial recommendation, pending verification)

### Архитектура: first-party `/broker-writer` skill

```
/broker-writer
  ├── 1. Broker Data Ingestion    — загрузка данных брокера (fees, regulation, platforms)
  ├── 2. Template-Driven Draft    — генерация по broker review template (10 секций)
  ├── 3. Humanization Pass        — удаление AI patterns (заимствованы из claude-seo, 24 паттерна)
  ├── 4. Fact/Citation Validator   — проверка claims через WebSearch
  ├── 5. SEO Optimization         — meta, headings, internal links, keyword density
  ├── 6. Schema.org Generator     — Review + Article + FAQPage + Person (author)
  └── 7. Publish Gate Checklist   — compliance, disclosure, expert byline, final QA
```

### Что НЕ зависит от external repos
- Broker data ingestion — собственный формат
- Template enforcement — 10 секций из анализа ForexBrokers/BrokerChooser
- Schema.org generation — JSON-LD template
- Compliance/disclosure language — finance-specific
- Expert voice integration — system prompt с style examples

### Что заимствуем (reference, не dependency)
- 24 AI humanization паттерна из `claude-seo` (Wikipedia-based)
- SEO optimization checklist structure
- Brand context file concept

### Ahrefs интеграция
- **Keyword research:** через `ahrefs-api-skills` SDK (когда Егор даст API key)
- **Post-publish optimization:** Ahrefs AI Content Helper (web UI)
- **AI detection check:** Ahrefs AI detection available via web tools (Page Inspect in Site Explorer). No confirmed public detection API endpoint
- **AI citations monitoring:** Brand Radar API `GET /v3/brand-radar/ai-responses`

## Планируемые сроки (planning estimates, not engineering commitments)

| Этап | Время | Что делаем |
|------|-------|-----------|
| PoC | 0.5 дня | Prompt template + 1 broker review |
| Usable workflow | 2-4 дня | Template enforcement, humanization, schema, fact-check |
| Production-ready | 1-2 недели | Broker data normalization, regression testing, QA gates |

### PoC (сегодня)
1. Создать prompt template для broker review (10 секций)
2. Сгенерировать 1 review через Claude Code
3. Вручную проверить через Ahrefs AI detector (web UI)
4. Оценить quality и iteration needs

## Следующие шаги

1. **Сегодня:** написать PoC prompt template + сгенерировать 1 broker review
2. **Эта неделя:** создать `/broker-writer` skill file с humanization patterns
3. **Когда Егор даст API key:** установить `ahrefs-api-skills` для keyword research
4. **После первых 10 reviews:** итерировать template по Ahrefs AI detection результатам
5. **Production:** QA gates, Schema.org auto-generation, publish checklist
