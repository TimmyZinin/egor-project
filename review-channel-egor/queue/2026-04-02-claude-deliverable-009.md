# DELIVERABLE_UPDATE — EGOR-ZEROGPT-RESEARCH-009

**From:** claude
**Date:** 2026-04-02
**Status:** COMPLETE — waiting for review

---

## Deliverables Produced

2 documents in `egor-project/docs/`:

1. **`zerogpt-checker-research.md`** — полное исследование ZeroGPT: API, pricing, accuracy, output format, сравнение с конкурентами
2. **`zerogpt-integration-decision.md`** — решение: ZeroGPT дополняет Ahrefs (Layer 3 в pipeline), не заменяет

---

## ZeroGPT: ключевые факты

### Подтверждённо:
- **API существует:** REST, base url `api.zerogpt.com`, Swagger docs, JWT auth
- **Endpoints:** detectText, detectFile, detectFiles, checkCollection
- **Output:** AI score (0-100), per-sentence highlighting, word counts
- **Pricing:** Business API pay-as-you-go: Basic $0.034/1K слов, PRO $0.049, VIP $0.069
- **Стоимость 1 статьи (4500 слов):** ~$0.15 (Basic tier)
- **Batch:** 40-150 файлов в зависимости от плана
- **TOS:** API usage explicitly permitted (web scraping forbidden)
- **GitHub:** github.com/zerogpt-net/zerogpt-api (JS + PHP examples)

### Проблемы:
- **Accuracy 70-85%** (не 98% как маркетинг). False positive rate 15-25%
- **Нет peer-reviewed validation** — ни одного рецензированного исследования
- **Rate limits не документированы** — нет SLA
- **Не определяет конкретную модель** — общий score, не "Claude" vs "GPT"
- **Документация тонкая** — Swagger есть, но error codes и edge cases не описаны

---

## Рекомендация: COMPLEMENT (дополняет Ahrefs)

### Новая 4-слойная архитектура:

```
Layer 1: /broker-writer   → генерация (без изменений)
Layer 2: /broker-checker  → quality gate (без изменений)
Layer 3: ZeroGPT API      → НОВЫЙ: автоматическая AI detection ($0.15/статья)
Layer 4: Human + Ahrefs   → ручная верификация + post-publish monitoring
```

### Почему не замена:
- ZeroGPT = pre-publish AI score (автоматический, дешёвый)
- Ahrefs = SEO + post-publish monitoring (keywords, backlinks, site audit AI levels, brand radar)
- Они решают РАЗНЫЕ задачи, не конкурируют

### Почему не optional:
- Без ZeroGPT, AI detection = ручная вставка в web tool (Layer 3 → human)
- С ZeroGPT, AI detection = автоматический API call, human проверяет только borderline cases
- $15/мес за 100 статей — окупаемость очевидна

---

## Сравнение с конкурентами (если ZeroGPT не подойдёт)

1. **Originality.ai** — лучше: API docs, 500 req/min, fact checker. Дороже: ~$0.045/статья
2. **GPTZero** — зрелее: 17 SDKs, SOC 2, hallucination detector. Pricing через sales
3. **Copyleaks** — third-party validated accuracy. Enterprise pricing

Рекомендация: начать с ZeroGPT, при false positive >20% → Originality.ai.

---

## Open Questions

1. Кто оплачивает ZeroGPT API — Егор или Tim?
2. Калибровка порогов — после первых 10-20 реальных статей
3. Fallback на Originality.ai — автоматический или ручное решение?

---

Claude is waiting for the next `go`.
