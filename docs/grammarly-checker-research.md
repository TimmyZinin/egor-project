# Исследование: Grammarly как инструмент проверки текстов

> Версия: 1.0 | Дата: 2026-04-02
> Статус: RESEARCH (не реализован)
> Задача: AI Detection Benchmark Research
> Автор: Claude (executor session)

---

## 1. Что такое Grammarly AI Detection

Grammarly (grammarly.com) — writing suite с AI detection как частью экосистемы. AI detection запущен в **августе 2024**. RAID benchmark score: **0.999** (#1, tied с GiantMelon и Veredict Labs).

Дополнительно: **Grammarly Authorship** (авг 2024) — provenance tracking (что напечатано, что скопировано, что AI). **AI Humanizer** (сент 2025) — rewrite для снижения AI score.

---

## 2. API: подтверждённые возможности

### Базовые параметры

| Параметр | Значение | Источник |
|----------|----------|---------|
| Base URL | `https://api.grammarly.com/ecosystem/api/v1/ai-detection` | developer.grammarly.com |
| Auth | OAuth 2.0 (Bearer token). Scopes: `ai-detection-api:read`, `ai-detection-api:write` | docs |
| Доступ | **Enterprise / Education institution-wide ONLY.** Free и Pro — без API | docs |
| Форматы | .doc, .docx, .odt, .txt, .rtf | docs |
| Rate limits | POST: 10 req/sec, GET: 50 req/sec | docs |
| Max file | 4 MB / 100,000 символов | docs |
| Min text | 30 слов | docs |
| Retention | Scores: 30 дней. Documents: max 24 часа | docs |
| SDK | Нет. Только raw REST / cURL | docs |

### Workflow (3 шага)

1. `POST /ai-detection` → получить `score_request_id` + pre-signed S3 URL
2. `PUT` к pre-signed URL → загрузить документ (120 сек timeout)
3. `GET /ai-detection/{score_request_id}` → poll результата (PENDING / COMPLETED / FAILED)

### Output format

```json
{
  "score_request_id": "...",
  "status": "COMPLETED",
  "score": {
    "average_confidence": 0.89,
    "ai_generated_percentage": 0.5
  }
}
```

**Ключевые ограничения output:**
- `ai_generated_percentage` = decimal 0-1 (не 0-100)
- **Нет per-sentence highlighting** — только document-level %
- **Нет 3-class classification** (human/mixed/ai) — только binary %
- **Нет explanation** WHY text was flagged

---

## 3. Ценообразование

| План | Цена | AI Detection | API |
|------|------|-------------|-----|
| Free | $0 | Web tool (paste text) | Нет |
| Pro | $12/мес | In-app detection + Authorship | Нет |
| Enterprise | Custom (sales call) | Full suite + API | Да (Beta) |

**API pricing не публичен.** Минимум ~$15/user/мес при 150+ пользователях [ESTIMATE].

---

## 4. Точность: RAID vs Reality

### RAID Benchmark
- Score: **0.999** (#1, tied)
- 11 моделей: ChatGPT, GPT-4, GPT-3, GPT-2, Mistral, Cohere, LLaMA, MPT
- Perfect 1.000 на GPT-4, GPT-3, GPT-2, LLaMA-chat, MPT

### Independent Tests
- GPTZero test (competitor-sourced, не независимый): 100% AI текст → Grammarly оценил как "50% AI" [COMPETITOR SOURCE]
- Непоследовательность: один текст → 0% → 35% → 90% в разные дни [ANECDOTAL, multiple reviews]
- False positive rate: ~6% [SINGLE SOURCE]
- Raw AI detection: ~94% на straightforward AI content [SINGLE SOURCE]
- Humanized content: пропускает ~22% [SINGLE SOURCE]
- Mixed content: значительно слабее [MULTIPLE SOURCES]

### Вывод
RAID benchmark и real-world тесты расходятся. Grammarly лидирует в контролируемых условиях (RAID). Независимые real-world тесты показывают непредсказуемость, но большинство из них основаны на анекдотических примерах или проведены конкурентами — необходима независимая верификация.

---

## 5. Grammarly Authorship (отдельный продукт)

В отличие от AI detection (анализ паттернов), Authorship = **provenance tracking**:
- Отслеживает в реальном времени: что напечатано, что скопировано, что AI
- Color-coded per-sentence view
- Shareable report link
- **Не использует ML detection** — только tracking origin

Доступен: Pro+ планы.

---

## 6. Ограничения (критичные для нашего use case)

1. **API = Enterprise only (Beta).** Для indie/startup недоступен
2. **Нет per-sentence highlighting** — невозможно понять какие абзацы flagged
3. **Непоследовательность** — тот же текст, разные результаты в разные дни
4. **Собственные AI suggestions trigger собственный detector** — парадокс
5. **Слабость на mixed content** (human + AI editing = основной use case)
6. **Только английский** для AI detection
7. **Beta API** — может измениться, нет SLA, нет SDK

---

## 7. Вердикт для нашего use case

**НЕ подходит** как primary automated pre-publish gate для broker reviews:
- API недоступен без Enterprise соглашения
- Нет per-sentence granularity для точечного исправления
- Непредсказуемые результаты

**Подходит когда:** уже есть Grammarly Enterprise подписка → AI detection = бесплатный бонус как дополнительный сигнал.

---

## Источники

- [Grammarly AI Detector](https://www.grammarly.com/ai-detector)
- [Grammarly AI Detection API (Beta)](https://developer.grammarly.com/ai-detection-api.html)
- [Grammarly OAuth Credentials](https://developer.grammarly.com/oauth-credentials.html)
- [Grammarly Plans & Pricing](https://www.grammarly.com/plans)
- [RAID Benchmark Leaderboard](https://raid-bench.xyz/leaderboard)
- [GPTZero: Grammarly AI Review](https://gptzero.me/news/grammarly-ai-review/)
- [Originality.ai: Grammarly Review](https://originality.ai/blog/grammarly-ai-detector-review)
