# /broker-checker-gptzero — Проверка текстов через GPTZero AI Detection

Проверяет broker review drafts на AI-сигнатуру через GPTZero API. Экономный режим: проверка по секциям, не целиком. Результат — advisory (P2), не блокирует публикацию.

## Триггеры

`/broker-checker-gptzero`, `проверь на AI`, `gptzero check`, `ai detection`

## Команды

```
/broker-checker-gptzero {slug}              — проверить latest draft (по секциям, economy mode)
/broker-checker-gptzero {slug} --full       — проверить весь текст целиком (4000-5000 слов)
/broker-checker-gptzero {slug} --section N  — проверить одну секцию (N = номер 1-18)
/broker-checker-gptzero --budget            — показать расход слов за месяц
/broker-checker-gptzero --list              — список проверенных брокеров с результатами
```

## Рабочая директория

`~/egor-project/`

## Prerequisites

- Env var `GPTZERO_API_KEY` должен быть установлен
- Если ключа нет → скилл выводит ошибку: "Set GPTZERO_API_KEY env var. Key from Egor's account (300K words/month limit)."
- Draft должен существовать: `content/{slug}/draft-v{N}.md`

## Процесс

### Основной flow (default = economy mode по секциям)

```
1. VALIDATE     — проверить GPTZERO_API_KEY, draft существует, manifest state ∈ {drafted, revised}
2. EXTRACT      — вытащить plain text из markdown (убрать заголовки #, таблицы, code blocks, JSON-LD)
3. SPLIT        — разбить текст на 18 секций по шаблону templates/broker-review.md
4. SELECT       — выбрать 4 ключевые секции для проверки:
                   - Секция 5 (Trust & Safety) — нарративная, типична для AI
                   - Секция 7 (Trading Platforms + Expert Take) — expert voice
                   - Секция 13 (Best For) — выводы
                   - Секция 14 (Final Verdict) — заключение
5. BUDGET CHECK — подсчитать слова в выбранных секциях, проверить лимит:
                   прочитать quality/gptzero-budget.json
                   если (used + new_words) > monthly_limit * 0.9 → WARN
                   если (used + new_words) > monthly_limit → STOP с ошибкой
6. API CALLS    — для каждой секции:
                   curl -s -X POST https://api.gptzero.me/v2/predict/text \
                     -H "x-api-key: $GPTZERO_API_KEY" \
                     -H "Content-Type: application/json" \
                     -H "Accept: application/json" \
                     -d '{"document": "<section_text>"}'
                   Timeout: 10 секунд. При ошибке → skip секцию, записать в отчёт.
7. PARSE        — из каждого ответа извлечь:
                   - documents[0].completely_generated_prob → AI Prob (0-1)
                   - documents[0].average_generated_prob → средний AI score
                   - documents[0].sentences[].generated_prob → per-sentence AI scores
                   Маппинг в Classification:
                     completely_generated_prob > 0.7  → AI_ONLY
                     completely_generated_prob > 0.3  → MIXED
                     completely_generated_prob <= 0.3 → HUMAN_ONLY
                   Confidence = high если |completely_generated_prob - 0.5| > 0.2,
                     medium если > 0.1, иначе low
8. REPORT       — сгенерировать отчёт (формат ниже)
9. SAVE         — сохранить:
                   - quality/gptzero-checks/{slug}-v{N}.json (raw API responses)
                   - обновить quality/gptzero-budget.json (добавить расход)
10. COMMIT      — git commit: "gptzero({slug}): check v{N} — {summary}"
```

### При --full

Шаги 3-4 пропускаются. Весь текст отправляется одним запросом (до 150K символов на API плане).
**ВНИМАНИЕ:** расходует ~4500 слов из бюджета за один запрос.

### При --section N

Шаги 3-4 заменяются: извлекается только секция N (1-18).

### При --budget

Читает `quality/gptzero-budget.json` и выводит:
```
GPTZero Budget (April 2026)
Used:      1,234 / 300,000 words (0.4%)
Remaining: 298,766 words
Checks:    3 (ig-v1 sections 5,7,14)
```

### При --list

Сканирует `quality/gptzero-checks/*.json`:
```
Slug | Version | Mode    | Classification | AI Prob | Date
-----|---------|---------|----------------|---------|-----
ig   | v1      | section | MIXED          | 0.42    | 2026-04-03
```

## Формат отчёта

Выводится в stdout (НЕ записывается в content/{slug}/ — это отдельный инструмент от broker-checker):

```markdown
# GPTZero Check: {broker_name} — Draft v{N}

**Mode:** economy (4 секции) | full | section {N}
**Date:** {ISO datetime}
**Words checked:** {count}
**Budget impact:** {count} / 300,000 (cumulative {total_used})

## Results

| Секция | Classification | AI Prob | Human Prob | Confidence |
|--------|---------------|---------|------------|------------|
| 5. Trust & Safety | MIXED | 0.42 | 0.35 | high |
| 7. Platforms + Expert Take | HUMAN_ONLY | 0.15 | 0.72 | high |
| 13. Best For | AI_ONLY | 0.78 | 0.12 | medium |
| 14. Final Verdict | MIXED | 0.55 | 0.28 | high |

## High-AI Sentences (ai_probability > 0.7)

| Секция | Sentence | AI Score |
|--------|----------|----------|
| 5 | "The platform provides robust analytical tools..." | 0.89 |
| 13 | "IG is best suited for experienced traders..." | 0.84 |

## Advisory (P2)

- Секции 5 и 14 классифицированы как MIXED — рекомендуется дополнительная гуманизация
- Секция 13 классифицирована как AI_ONLY — высокий приоритет переработки
- Секция 7 (Expert Take) — HUMAN_ONLY, expert voice работает хорошо

**Severity: P2 (advisory).** Результаты НЕ блокируют публикацию. Используйте для точечной доработки humanization.
```

## Классификация GPTZero

| Classification | Confidence | Действие |
|---------------|------------|----------|
| `HUMAN_ONLY` | high/medium | Ничего не делать |
| `MIXED` | high/medium | Рекомендовать humanization целевых предложений |
| `AI_ONLY` | high/medium | Настоятельно рекомендовать humanization всей секции |
| Any | low | Показать с пометкой "(unreliable)", НЕ давать рекомендаций |

**Правило:** рекомендации даются ТОЛЬКО при high/medium confidence. Low confidence = только информация.

## Error handling

| Ситуация | Действие |
|----------|----------|
| Нет GPTZERO_API_KEY | STOP с инструкцией |
| API возвращает non-200 | Skip секцию, записать ошибку |
| API timeout (>10s) | Skip секцию, записать timeout |
| Невалидный JSON ответ | Skip секцию, записать parse error |
| Low confidence результат | Показать но пометить "(unreliable)" |
| Budget limit reached | STOP с текущим расходом |
| Draft не существует | STOP с ошибкой |
| Manifest state ≠ drafted/revised | WARN но разрешить проверку |

## Чего скилл НЕ делает

- НЕ проверяет структуру, факты, SEO, compliance (→ будущий /broker-checker)
- НЕ модифицирует draft (read-only)
- НЕ блокирует публикацию (severity всегда P2)
- НЕ обновляет manifest.json (это не quality gate, а advisory tool)
- НЕ запускает Ahrefs (→ ручной post-publish)

## Экономия бюджета

| Режим | Слов за проверку | % от 300K | Когда использовать |
|-------|-----------------|-----------|-------------------|
| **economy** (default) | ~1200 | 0.4% | Рутинная проверка каждого draft |
| **--section N** | ~300 | 0.1% | Точечная проверка подозрительной секции |
| **--full** | ~4500 | 1.5% | Финальная проверка перед публикацией |

**Рекомендация:** economy mode для всех drafts, --full только перед финальной публикацией.

## Конфигурация

`quality/gptzero-config.json` — пороги, endpoint, лимиты.

## Budget tracking

`quality/gptzero-budget.json` — трекер расхода по месяцам.

### Схема budget entry

```json
{
  "month": "2026-04",
  "monthly_limit": 300000,
  "total_words_used": 1234,
  "checks": [
    {
      "slug": "ig",
      "version": 1,
      "mode": "economy",
      "sections_checked": [5, 7, 13, 14],
      "words": 1234,
      "timestamp": "2026-04-03T15:00:00Z"
    }
  ]
}
```

### Схема check result (`quality/gptzero-checks/{slug}-v{N}.json`)

```json
{
  "slug": "ig",
  "version": 1,
  "mode": "economy",
  "checked_at": "2026-04-03T15:00:00Z",
  "words_checked": 1234,
  "sections": [
    {
      "number": 5,
      "name": "Trust & Safety",
      "classification": "MIXED",
      "completely_generated_prob": 0.42,
      "average_generated_prob": 0.38,
      "confidence": "high",
      "high_ai_sentences": [
        {"text": "The platform provides...", "generated_prob": 0.89}
      ]
    }
  ],
  "api_responses_raw": ["...truncated..."]
}
```

### Month rollover

При первом запуске нового месяца: если `month` в budget.json ≠ текущий месяц → сбросить `total_words_used` в 0, очистить `checks[]`, обновить `month`. Старые данные доступны в git history.

### Failed/skipped секции

Пропущенные секции (API error, timeout) НЕ считаются в `total_words_used`. Учитываются только секции с успешным API response.

## Полная спецификация

`docs/broker-content/broker-checker-spec.md` (базовый checker) + `docs/ai-detection/gptzero-decision.md` (решение по GPTZero)
