# DELIVERABLE_UPDATE — EGOR-BROKER-WRITER-RESEARCH-008

**From:** claude
**Date:** 2026-04-02
**Status:** COMPLETE — waiting for review

---

## Deliverables Produced

4 spec documents in `egor-project/docs/`:

1. **`broker-writer-spec.md`** — полная спецификация writer skill
2. **`ahrefs-checker-spec.md`** — полная спецификация checker skill
3. **`broker-writer-ahrefs-integration.md`** — как writer + checker + Ahrefs работают вместе
4. **`source-of-truth-decision.md`** — решение по repos + именованию + timeline

---

## Confirmed Ahrefs Capabilities (from primary sources, April 2026)

### API v3 — ЧТО ЕСТЬ:
- Site Explorer (26 endpoints): backlinks, organic keywords, top pages, domain rating
- Keywords Explorer: keyword metrics, volume, ideas
- SERP Overview: top 100 results per keyword
- Site Audit: health scores, crawled pages
- Brand Radar (9 endpoints): **AI Responses** (мониторинг AI-цитирования), Cited Pages, Impressions
- Batch Analysis: до 100 targets per request
- MCP server: hosted api.ahrefs.com/mcp/mcp (Lite+ plan, same API units)
- Pricing: Lite 25K units/mo → Enterprise 2M units/mo

### API v3 — ЧЕГО НЕТ:
- **AI content detection endpoint — НЕ СУЩЕСТВУЕТ** (подтверждено)
- Programmatic AI text check — НЕТ (ни API, ни SDK, ни CLI)
- Bulk pre-publish text analysis — НЕТ

### Web tools (ручные, не автоматизируемые):
- Free AI Content Detector (web paste, несколько сот слов)
- Page Inspect → AI Detector tab (post-publish only)
- Top Pages → AI Content Level column (подписка)
- Site Audit → AI Content Level filter (подписка, после crawl)

---

## Proposed Architecture

### 3-слойная система:

```
Layer 1: /broker-writer  → генерация draft (18 секций, 4-5K слов, Schema.org)
Layer 2: /broker-checker → автопроверка (structure, facts, SEO, compliance, humanization)
Layer 3: Human + Ahrefs  → ручная AI detection + publish decision
```

### Ключевые решения:
- **2 скилла, не 1.** Writer пишет, checker проверяет. Независимые prompt contexts.
- **Checker НЕ использует Ahrefs API** (endpoint не существует). Проверяет structure/facts/SEO/compliance/humanization.
- **Ahrefs AI detection = ручной слой.** Human paste в web tool после APPROVED.
- **Manifest.json** как state tracker (git-native, LLM-friendly).
- **Severity system:** P0 (blocks publish), P1 (requires fix), P2 (advisory).

---

## Source of Truth Recommendation

**Оставить в `egor-project/` на данном этапе.** Причины:
- `content-pipeline` repo уже занят (Tim's SMM system)
- Нет ни одного real content artifact
- Target publishing platform не определена
- Выделять в отдельный repo → когда ≥10 артефактов + определена платформа + git history мешает

При выделении → `TimmyZinin/broker-content` (не rated-brokers, не content-pipeline).

### Naming:
- `/broker-writer` (не /rb-content-gen)
- `/broker-checker` (не /broker-reviewer)
- `/expert-hunter` — без изменений

---

## Open Questions (before implementation)

1. **Publishing platform?** WordPress, static site, custom CMS? Влияет на output format.
2. **Ahrefs API key?** У Егора есть? Какой план? Нужен для keyword research.
3. **Expert review step?** Будет ли эксперт из expert-hunter реально ревьюить текст?
4. **Scale?** 5-10 reviews/mo → manual OK. 50+ → need n8n automation.
5. **AI detection budget?** Ручной Ahrefs = $0. Автоматический (Originality.ai/GPTZero) = $15-30/mo.

---

Claude is waiting for the next `go`.
