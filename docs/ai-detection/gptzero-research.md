# Исследование: GPTZero как инструмент проверки текстов

> Версия: 1.0 | Дата: 2026-04-02
> Статус: RESEARCH (не реализован)
> Задача: EGOR-GPTZERO-RESEARCH-010
> Автор: Claude (executor session)

---

## 1. Что такое GPTZero

GPTZero (gptzero.me) — AI-детектор текста. Основан в Princeton, NJ. SOC 2 compliant. Клиенты: Microsoft, Newsguard, Nextcloud, K16 Solutions. Определяет текст от GPT-3/4/5, Gemini, Claude, LLaMA.

Дополнительно: Relevant Sources API (hallucination detection), Bibliography scan, Plagiarism checker, AI Vocabulary scan.

---

## 2. API: подтверждённые возможности

### Базовые параметры

| Параметр | Значение | Источник |
|----------|----------|---------|
| Base URL | `https://api.gptzero.me` | Подтверждено live-тестом |
| Документация | Stoplight: gptzero.stoplight.io/docs/gptzero-api | Подтверждено |
| Auth | Header `x-api-key: <key>` | Подтверждено live-тестом |
| API key | Генерируется на app.gptzero.me/api | Подтверждено |
| Free trial | Доступен без аккаунта (ограниченно) | support.gptzero.me |
| SOC 2 | Compliant (AICPA) | gptzero.me |
| Rate limit | **30,000 req/hour** | support.gptzero.me |

### Endpoints

| # | Метод | Endpoint | Назначение |
|---|-------|----------|-----------|
| 1 | POST | `/v2/predict/text` | AI detection на строке текста |
| 2 | POST | `/v2/predict/files` | AI detection на массиве файлов |
| 3 | GET | (model versions) | Доступные версии моделей |
| 4 | GET | (usage stats) | Статистика использования |
| 5 | POST | (bibliography scan - doc) | Проверка библиографии |
| 6 | POST | (bibliography scan - files) | Проверка библиографии (файлы) |

**Relevant Sources API** (отдельный workspace):

| # | Метод | Назначение |
|---|-------|-----------|
| 7 | POST | Найти источники для одного claim/sentence |
| 8 | POST | Извлечь claims + найти источники для всего текста |

### Input format

```json
{"document": "string", "version": "string"}
```

**Файлы:** `.txt`, `.docx`, `.pdf`. Макс. 50 файлов/запрос, 15 MB суммарно.
**Символы/скан:** 50K (Premium) / 150K (Professional/API).

### Output format (подтверждён из support docs)

```json
{
  "document_classification": "HUMAN_ONLY | MIXED | AI_ONLY",
  "class_probabilities": {
    "human": 0.85,
    "ai": 0.10,
    "mixed": 0.05
  },
  "predicted_class": "human",
  "confidence_category": "high | medium | low",
  "sentences": [
    {
      "sentence": "...",
      "ai_probability": 0.12
    }
  ]
}
```

**Ключевые поля:**
- `document_classification` — категорический вердикт (HUMAN_ONLY / MIXED / AI_ONLY)
- `class_probabilities` — вероятности трёх классов (float)
- `confidence_category` — высокая/средняя/низкая уверенность
- Sentence-level AI probability scores — подсветка конкретных предложений

**Отличие от ZeroGPT:** GPTZero возвращает **3-классовую** классификацию (human/mixed/ai) с уровнем уверенности, а не просто процент. Это богаче для принятия решений.

---

## 3. Ценообразование

### Consumer-планы (web UI)

| План | Месячно (при годовой) | Месячно (помесячно) | Слов/мес | Символов/скан |
|------|----------------------|--------------------|---------|--------------| 
| Premium | $12.99 | $23.99 | 300K | 50K |
| Professional | $24.99 | $45.99 | 500K | 150K |

### API-планы (developer)

| Слов/мес | Цена/мес | $/1K слов |
|----------|---------|-----------|
| 300K | $45 | $0.15 |
| 1M | $135 | $0.135 |
| 2M | $250 | $0.125 |
| 5M | $550 | $0.11 |
| 10M | $1,000 | $0.10 |
| 20M | $1,850 | $0.0925 |

**Overage:** $0.00015/слово ($150/1M слов). Макс. 1M слов overage до принудительного апгрейда.

Все API-планы включают: 50 файлов/batch, 150K символов/документ, premium detection model.

### Расчёт для broker reviews

| Параметр | Значение |
|----------|----------|
| 1 статья | ~4500 слов |
| Стоимость/статья (300K план) | $45 ÷ 300K × 4500 = **$0.675** |
| Стоимость/статья (overage) | 4500 × $0.00015 = **$0.675** |
| 10 статей/мес | ~$6.75 (укладывается в 300K план: $45) |
| 50 статей/мес | ~$33.75 (нужен 300K план + overage ≈ **$55-60**) |
| 100 статей/мес | ~$67.50 (нужен 1M план: **$135**) |

**Сравнение с ZeroGPT:**

| Масштаб | ZeroGPT Basic | GPTZero 300K | Разница |
|---------|--------------|-------------|---------|
| 1 статья | $0.15 | $0.675 | GPTZero **4.5x дороже** |
| 10/мес | $1.50 | $45 (min plan) | GPTZero **30x дороже** |
| 100/мес | $15 | $135 | GPTZero **9x дороже** |

---

## 4. Точность: факты vs маркетинг

### Заявления GPTZero

- "96.5% accuracy on mixed documents"
- "<1% false positive rate" (general)
- TOEFL essay FPR: 1.1%
- Chicago Booth 2026 benchmark: 99.3% recall at ~0.1% FPR
- При `confidence_category: high`: 99.1% human articles корректно, 98.4% AI корректно

### Независимые оценки

| Источник | Результат |
|----------|----------|
| Chicago Booth 2026 (академический) | 99.3% recall at 0.1% FPR — **credible academic study** |
| Ryne AI (100K+ текстов) | "Not reliable anymore", significantly higher FPR |
| MPG ONE 2026 (40 текстов) | **12.5% FPR** (5/40 human текстов помечены как AI) |
| Yale lawsuit (Feb 2025) | Студент отстранён по GPTZero flag, alleged ESL bias |

### Оценка точности

**Разброс:** от <1% FPR (контролируемые academic benchmarks) до 5-15% FPR (real-world mixed use). Правда вероятно посередине.

**Важно:** `confidence_category: high` фильтрует большинство false positives. При использовании **только high-confidence** результатов FPR значительно ниже, чем при использовании всех результатов.

**Сравнение с ZeroGPT:** GPTZero имеет лучшую академическую валидацию (Chicago Booth). ZeroGPT не имеет ни одного peer-reviewed benchmark.

---

## 5. Уникальные преимущества GPTZero

### Relevant Sources API (hallucination detection)

Отдельная API — извлекает factual claims из текста и находит подтверждающие/противоречащие источники. Это **уникально** среди AI-детекторов и **релевантно** для YMYL/финансового контента:

- Можно проверить: "IG's EUR/USD spread is 0.6 pips" → найдёт источник или отметит как unverifiable
- Broker reviews содержат десятки factual claims о комиссиях, регуляторах, продуктах
- Ни ZeroGPT, ни Ahrefs не предлагают подобной функции

**Статус:** API задокументирован (отдельный Stoplight workspace). Pricing не ясен — вероятно входит в API-план. [UNVERIFIED: отдельная стоимость]

### 3-классовая классификация

HUMAN_ONLY / MIXED / AI_ONLY с confidence level — более nuanced, чем ZeroGPT's binary percentage. Позволяет:
- Принимать решения на **high-confidence** результатах (низкий FPR)
- Отправлять **medium-confidence** на ручную проверку
- Игнорировать **low-confidence** результаты

### SOC 2 Compliance

Для клиентов уровня enterprise это может быть важно. ZeroGPT не заявляет SOC 2.

---

## 6. Ограничения и риски

1. **Значительно дороже ZeroGPT.** Минимум 4.5x на статью, 30x на малых масштабах (из-за минимального плана $45/мес).
2. **Минимальный план $45/мес.** Нет pay-as-you-go. Для 5-10 статей/мес — переплата.
3. **FPR в real-world 5-15%.** Не <1% как в маркетинге.
4. **ESL bias risk.** Yale lawsuit + общая проблема AI-детекторов с non-native English.
5. **Stoplight docs = JS SPA.** Не извлекается через curl; нужен браузер для чтения.
6. **Нет официального SDK.** Только третья сторона (PyPI `gptzero` v0.1.2, Apr 2023 — возможно устаревший).
7. **Relevant Sources API pricing unclear.** Может быть отдельная стоимость.

---

## 7. Сводная таблица: GPTZero vs ZeroGPT vs Ahrefs

| Критерий | GPTZero | ZeroGPT | Ahrefs |
|----------|---------|---------|--------|
| **API для AI detection** | ✅ REST, Stoplight docs | ✅ REST, Swagger docs | ❌ Нет endpoint |
| **Pre-publish check** | ✅ Автоматический | ✅ Автоматический | ❌ Только web UI |
| **Post-publish check** | ❌ Нужен текст | ❌ Нужен текст | ✅ Page Inspect, Site Audit |
| **Стоимость/статья** | $0.675 | $0.15 | — (подписка) |
| **Мин. план** | $45/мес | Pay-as-you-go | Lite ~$99/мес |
| **Rate limit** | 30K req/hr (задокументирован) | Не задокументирован | 60 req/min |
| **Batch** | 50 файлов | 40-150 файлов | — |
| **Accuracy (academic)** | Chicago Booth 99.3% recall | Нет peer-review | — |
| **Accuracy (real-world)** | 5-15% FPR | 15-25% FPR | ~80-85% (estimate) |
| **3-class classification** | ✅ (human/mixed/ai + confidence) | ❌ (только % score) | — |
| **Hallucination detection** | ✅ Relevant Sources API | ❌ | ❌ |
| **Fact checking** | ✅ (через Relevant Sources) | ❌ | ❌ |
| **SEO / Keywords** | ❌ | ❌ | ✅ |
| **Backlinks / Site Audit** | ❌ | ❌ | ✅ |
| **SOC 2** | ✅ | ❌ | — |
| **Документация** | Хорошая (Stoplight) | Средняя (Swagger) | Хорошая |
