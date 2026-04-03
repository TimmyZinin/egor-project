# Решение: GPTZero в broker content pipeline

> Версия: 1.1 | Дата: 2026-04-03
> Статус: РЕШЕНИЕ (согласовано — GPTZero выбран как основной инструмент)
> Задача: EGOR-GPTZERO-RESEARCH-010
> Автор: Claude (executor session)

---

## Вопрос

Подходит ли GPTZero для нашего text-checking skill? Должен ли GPTZero заменить ZeroGPT, дополнить его, или остаться вне скоупа?

---

## Вердикт: GPTZero — ОСНОВНОЙ инструмент AI detection

> **Обновлено 3 апреля 2026:** Решение изменено. GPTZero выбран как основной (не upgrade). ZeroGPT отклонён из-за низкого качества (Trustpilot 1.3/5, документированные false negatives). API ключ получен от аккаунта Егора (300K слов/мес).

### Текущая архитектура

| Слой | Инструмент | Статус |
|------|-----------|--------|
| **Pre-publish AI detection** | **GPTZero** (API) | API ключ получен, скилл `/broker-checker-gptzero` в разработке |
| **Post-publish monitoring** | **Ahrefs** (web UI, ручной) | Как и раньше — Site Audit, AI Content Level |

### Почему GPTZero сразу (а не ZeroGPT → GPTZero)

1. **ZeroGPT отклонён.** Trustpilot 1.3/5, задокументированные случаи false negatives (ChatGPT текст = 0% AI). Ненадёжен даже для калибровки.
2. **API ключ уже есть.** Егор оформил план на 300K слов/мес — нет смысла экономить на отдельном инструменте.
3. **Экономный режим.** Проверка по секциям (~300 слов) вместо полных статей (4500 слов) = 15x экономия бюджета.
4. **3-class confidence** (HUMAN_ONLY/MIXED/AI_ONLY + high/medium/low) — даёт более полезный сигнал чем бинарный % от ZeroGPT.

### Почему GPTZero лучше ZeroGPT на масштабе

1. **3-class confidence.** `HUMAN_ONLY / MIXED / AI_ONLY` + `high/medium/low` confidence > простой процент. Можно фильтровать по high-confidence, снижая false positives.
2. **Relevant Sources API.** Уникальная возможность: проверка factual claims в broker reviews. "IG's EUR/USD spread is 0.6 pips" → источник найден/не найден. Ни ZeroGPT, ни Ahrefs это не делают.
3. **Лучшая академическая валидация.** Chicago Booth 2026: 99.3% recall at 0.1% FPR — единственный AI-детектор с credible independent benchmark.
4. **SOC 2.** Для enterprise клиентов может быть requirement.
5. **Задокументированные rate limits.** 30K req/hr — задокументированная квота. ZeroGPT: rate limits не задокументированы. (Примечание: rate limit ≠ SLA; SLA = гарантия uptime/поддержки, отдельно не заявлен ни одним из сервисов.)

### Почему НЕ замена Ahrefs

GPTZero и Ahrefs решают разные задачи (без изменений от task 009):
- GPTZero = pre-publish AI detection + fact-checking claims
- Ahrefs = SEO (keywords, backlinks, SERP) + post-publish AI content level monitoring

---

## Текущий pipeline (GPTZero как основной инструмент)

### Принятая архитектура

```
Layer 1: /broker-writer   → генерация draft
Layer 2: /broker-checker  → quality gate (structure, facts, SEO, compliance, humanization)
Layer 3a: GPTZero API     → AI detection с 3-class confidence ($0.675/статья)
Layer 3b: GPTZero Sources → fact-check claims в тексте (Relevant Sources API, планируется)
Layer 4: Human + Ahrefs   → ручная верификация + post-publish monitoring
```

**Layer 3b:** GPTZero Relevant Sources API проверяет factual claims в broker review. Это дополняет `/broker-checker` (который сверяет с input.json) — Relevant Sources проверяет claims **против внешних источников**. Интеграция планируется при масштабировании.

### Mermaid: архитектура pipeline

```mermaid
flowchart TD
    subgraph L1["Слой 1: /broker-writer"]
        W[Генерация draft<br/>18 секций, 4-5K слов]
    end

    subgraph L2["Слой 2: /broker-checker"]
        C[Автопроверка<br/>structure + facts + SEO<br/>+ compliance + humanization]
    end

    subgraph L3["Слой 3: GPTZero API (основной)"]
        G1[GPTZero Predict<br/>3-class + confidence<br/>API ключ получен]
        G2[GPTZero Sources<br/>fact-check claims<br/>планируется]
    end

    subgraph L4["Слой 4: Human + Ahrefs"]
        HQ[Human QA<br/>финальная проверка]
        AH[Ahrefs<br/>post-publish monitoring]
    end

    W --> C --> G1 --> G2 --> HQ --> AH
```

---

## Стоимость: сценарии

| Масштаб | ZeroGPT | GPTZero (300K) | GPTZero (1M) | Дельта |
|---------|---------|----------------|-------------|--------|
| 10 статей/мес | $1.50 | $45 (min plan) | — | +$43.50 |
| 50 статей/мес | $7.50 | ~$55-60 | — | +$50 |
| 100 статей/мес | $15 | — | $135 | +$120 |
| 200 статей/мес | $30 | — | $135 | +$105 |

**Breakeven по цене:** GPTZero **не становится дешевле ZeroGPT** ни при каком масштабе. 1M слов / 4500 слов ≈ 222 статьи → $135 / 222 ≈ **$0.61/статья** (vs ZeroGPT $0.15). Переход на GPTZero мотивирован **качеством** (accuracy, 3-class, Sources API), не ценой.

---

## Relevant Sources API — потенциальная интеграция

### Что это даёт для broker reviews

Broker review содержит десятки factual claims:
- "IG is regulated by FCA, ASIC, MAS" → Sources API находит подтверждение
- "EUR/USD spread from 0.6 pips" → Sources API ищет источник
- "IG was founded in 1974" → Sources API проверяет

Это **дополняет** (не заменяет) `/broker-checker`:
- `/broker-checker` сверяет draft vs `input.json` (внутренний fact-check)
- GPTZero Sources сверяет draft vs **внешние источники** (external fact-check)

### Когда интегрировать

Не сейчас. Relevant Sources API — upgrade для масштаба. На старте:
1. `/broker-checker` достаточен для fact-checking (сверка с input.json)
2. Human QA ловит остальное
3. Relevant Sources API = Layer 3b при масштабировании

---

## Итоговая рекомендация

| Вопрос | Ответ |
|--------|-------|
| Подходит ли GPTZero? | **Да — выбран как основной инструмент** |
| ZeroGPT? | **Отклонён** — Trustpilot 1.3/5, задокументированные false negatives |
| Заменить ZeroGPT? | **Да** — GPTZero используется с самого старта (API ключ получен) |
| Дополнить ZeroGPT? | **Нет** — ZeroGPT не используется |
| Дополнить Ahrefs? | **Да** — разные задачи (AI detection vs SEO/post-publish) |
| Budget impact? | $45/мес min (300K слов/мес план Егора) |

---

## Открытые вопросы

1. **Relevant Sources API pricing.** Входит в API-план или отдельная стоимость? [UNVERIFIED]
2. **Python SDK актуальность.** PyPI `gptzero` v0.1.2 (Apr 2023) — может быть устаревшим. Нужно проверить при интеграции.
3. **Finance-specific accuracy.** Ни один AI-детектор не тестировался специфически на финансовом контенте. Нужна собственная калибровка.
