# Исследование: ZeroGPT как инструмент проверки текстов

> Версия: 1.0 | Дата: 2026-04-02
> Статус: RESEARCH (не реализован)
> Задача: EGOR-ZEROGPT-RESEARCH-009
> Автор: Claude (executor session)

---

## 1. Что такое ZeroGPT

ZeroGPT (zerogpt.com) — AI-детектор текста. Определяет, написан ли текст человеком или сгенерирован LLM (ChatGPT, Claude, Gemini, Grok, DeepSeek, LLaMA).

Помимо детектора: Image Detector, Plagiarism Checker, AI Humanizer, Paraphraser, Summarizer.

---

## 2. Возможности (подтверждённые)

### Что возвращает

| Поле | Тип | Описание |
|------|-----|----------|
| `is_human_written` | int (0-100) | Процент "человеческого" текста |
| `is_gpt_generated` | int (0-100) | Процент AI-текста |
| `gpt_generated_sentences` | array | Список предложений, помеченных как AI |
| `h` | array | AI-flagged sentences (сокращённое поле) |
| `aiWords` | int | Количество слов, определённых как AI |
| `textWords` | int | Общее количество слов |
| `fakePercentage` | int | AI процент (дубликат is_gpt_generated) |
| `feedback_message` | string | Текстовый вердикт |

**Источник:** GitHub repo zerogpt-net/zerogpt-api + Swagger docs api.zerogpt.com/docs

### Ограничения по длине текста

| План | Макс. символов на проверку |
|------|--------------------------|
| Free (web) | 15,000 |
| Basic API | 50,000 |
| PRO API | 150,000 |
| VIP API | 500,000 |

Оптимальная точность: ≥150-200 слов. Рекомендуется: 500-1000+ слов.

Для broker review (4000-5000 слов ≈ 25,000-30,000 символов) — помещается в Basic API tier.

### Языки

"All available languages" — без конкретного списка. [UNVERIFIED: нет подтверждения на каких языках реально обучен]

---

## 3. API: подтверждённые возможности

### Доступность

**API существует и официально поддерживается.**

| Параметр | Значение |
|----------|----------|
| Base URL | `api.zerogpt.com` |
| Документация | Swagger: api.zerogpt.com/docs, Theneo: app.theneo.io/olive-works-llc/zerogpt-docs |
| Auth | Два метода: (1) JWT Bearer token через login endpoint, или (2) API key через `/api/auth/generateApiKey`. Документация не уточняет какой метод предпочтителен для production [NEEDS CLARIFICATION at integration time] |
| Postman | Коллекция доступна публично |
| GitHub | github.com/zerogpt-net/zerogpt-api (JS + PHP примеры) |

### Endpoints

| Endpoint | Метод | Назначение |
|----------|-------|-----------|
| `/api/auth/login` | POST | Авторизация, получение JWT |
| `/api/auth/generateApiKey` | GET | Генерация API key |
| `/api/detect/detectText` | POST | Проверка одного текста |
| `/api/detect/detectFile` | POST | Проверка одного файла |
| `/api/detect/detectFiles` | POST | Batch проверка файлов |
| `/api/detect/checkCollection` | POST | Проверка коллекции |
| `/api/dashboard/detectionResults` | GET | Получение истории проверок |
| `/api/dashboard/exportToPdf` | GET | Экспорт в PDF |

### Пример запроса

```bash
curl -X POST https://api.zerogpt.com/api/detect/detectText \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Your text here..."}'
```

### Пример ответа

```json
{
  "success": true,
  "data": {
    "is_human_written": 15,
    "is_gpt_generated": 85,
    "feedback_message": "Your text is likely AI-generated",
    "gpt_generated_sentences": ["sentence 1", "sentence 2"],
    "h": ["sentence 1", "sentence 2"],
    "aiWords": 425,
    "textWords": 500,
    "fakePercentage": 85
  }
}
```

### Rate limits

**Не задокументированы.** Pay-as-you-go модель подразумевает usage-based billing без жёстких rate limits. [UNVERIFIED: конкретные лимиты не найдены]

---

## 4. Ценообразование

### Web-планы (личные)

| План | Цена/мес | AI Detection символов | Batch файлов |
|------|---------|----------------------|-------------|
| Free | $0 | 15,000 | — |
| PRO | $7.99 | 100,000 | 50 |
| PLUS | $14.99 | 100,000 | 60 |
| MAX | $18.99 | 150,000 | 75 |
| Enterprise | Custom | Custom | Custom |

### API Business (pay-as-you-go)

| Tier | Стоимость AI detection | Макс. символов/проверка | Batch файлов | Макс. размер файла |
|------|----------------------|------------------------|-------------|-------------------|
| Basic | $0.034 / 1000 слов | 50,000 | 40 | — |
| PRO | $0.049 / 1000 слов | 150,000 | 75 | 5 MB |
| VIP | $0.069 / 1000 слов | 500,000 | 150 | 15 MB |

**Минимальная плата:** тексты <300 слов — минимум $0.15-0.18 за проверку.

**Расчёт для broker reviews:**
- 1 статья ≈ 4500 слов
- Basic tier: 4.5 × $0.034 = **~$0.15 за статью**
- 100 статей/мес: **~$15/мес**

Источник: zerogpt.com/pricing

---

## 5. Точность: факты vs маркетинг

### Маркетинговые заявления ZeroGPT

- ">98% accuracy on internal evaluations"
- "Highest accuracy in the industry"

### Независимые оценки (подтверждённые)

| Источник | Результат |
|----------|----------|
| Независимые обзоры (Skywork, NoteGPT, AcademicHelp) | Реальная точность: **70-85%** в зависимости от типа текста |
| False positive rate на человеческом тексте | **15-25%** |
| Исследование 37,874 эссе | **26.4%** false positives |
| Non-native English speakers | Повышенный false positive rate (~19%) |
| Слегка отредактированный AI-текст | Детекция **резко падает** (синонимы, реструктуризация) |

**Peer-reviewed валидация: НЕ НАЙДЕНА.** Все заявления "98%" — self-reported.

### Вывод по точности

ZeroGPT **не может служить единственным критерием** для publish/reject решения. False positive rate 15-25% означает, что каждый 4-5-й хороший текст будет ошибочно помечен как AI. Приемлемо как **сигнал**, не как **gatekeeper**.

---

## 6. Сравнение с конкурентами

| Критерий | ZeroGPT | Originality.ai | GPTZero | Copyleaks |
|----------|---------|---------------|---------|-----------|
| **API** | ✅ REST | ✅ REST v2 | ✅ REST (17 SDKs) | ✅ REST + SDKs |
| **Free tier** | 15K chars web | Нет (PAYG $30) | Web only | 25K chars web |
| **Мин. цена** | $0.034/1K слов | ~$0.01/100 слов | ~$12.99/мес | Sales-based |
| **Batch** | 40-150 файлов | Dedicated endpoint | До 250 файлов | Enterprise |
| **Per-sentence** | ✅ | ✅ | ✅ | ✅ |
| **Accuracy (independent)** | 70-85% | Не подтверждено независимо | Не подтверждено | Third-party validated |
| **Rate limits** | Не задокументированы | 500 req/min | Не задокументированы | Не задокументированы |
| **YMYL features** | Нет | Fact checker | Hallucination detector | AI Logic (source matching) |
| **Документация** | Средняя (Swagger) | Хорошая | Хорошая (Stoplight) | Enterprise-grade |

### Ranking для программной pre-publish проверки

1. **Originality.ai** — лучшая документация, ясные rate limits, batch endpoint, fact checker
2. **GPTZero** — зрелый API (17 SDKs, Zapier), SOC 2, hallucination detector
3. **Copyleaks** — third-party validated accuracy, но pricing через sales
4. **ZeroGPT** — API есть, но документация тонкая, pricing непрозрачный, accuracy не подтверждена
5. **Winston AI** — базовый API, ограниченная языковая поддержка

**Ни один инструмент не предлагает finance/YMYL-специфичные модели детекции.**

---

## 7. Дизайн будущего использования ZeroGPT в pipeline

### Концепт: ZeroGPT как программный pre-publish AI detection gate

```
/broker-writer → draft-v{N}.md
  ↓
/broker-checker → review-v{N}.md (structure, facts, SEO, compliance, humanization)
  ↓ APPROVED
ZeroGPT API → detectText(draft text)
  ↓
  ├── AI score ≤30%  → готов к ручной проверке
  ├── AI score 30-60% → дополнительный humanization pass
  └── AI score >60%  → переписать highlighted sentences, повторить
  ↓
Human + Ahrefs (ручная верификация)
  ↓
Публикация
```

### Что ZeroGPT skill читает

| Вход | Источник |
|------|---------|
| Текст черновика | `content/{slug}/approved.md` или `draft-v{N}.md` |
| Конфигурация порогов | `quality/zerogpt-config.json` |

### Что ZeroGPT skill возвращает

```json
{
  "broker_slug": "ig",
  "checked_at": "2026-04-02T15:00:00Z",
  "source_file": "content/ig/approved.md",
  "overall_ai_score": 35,
  "overall_human_score": 65,
  "total_words": 4500,
  "ai_words": 1575,
  "flagged_sentences": [
    "Furthermore, IG offers a comprehensive range of trading instruments.",
    "The platform provides robust analytical tools for traders."
  ],
  "verdict": "PASS",
  "action": "none"
}
```

### Логика вердикта

| AI Score | Вердикт | Действие |
|----------|---------|---------|
| 0-30% | PASS | Переходит к Human QA |
| 30-60% | WARN | Дополнительный humanization pass на flagged sentences |
| 60-100% | FAIL | Переписать flagged sentences, повторная проверка |

**Пороги конфигурируемые** через `quality/zerogpt-config.json`. Калибровка после первых 10-20 статей.

### Стоимость при масштабе

| Масштаб | Стоимость ZeroGPT (Basic) | С учётом re-checks |
|---------|--------------------------|-------------------|
| 10 статей/мес | ~$1.50/мес | ~$3/мес (2x re-check) |
| 50 статей/мес | ~$7.50/мес | ~$15/мес |
| 100 статей/мес | ~$15/мес | ~$30/мес |

---

## 8. Terms of Service

- Web scraping/bots **запрещены** на сайте zerogpt.com
- API usage **разрешён и является платной функцией** — программные вызовы через API = intended use case
- Разграничение ясное: web scraping forbidden, API calls permitted

Источник: zerogpt.com/terms-of-use

---

## 9. Риски и ограничения

1. **Accuracy 70-85%**, не 98% как заявляет маркетинг. False positives неизбежны.
2. **Нет peer-reviewed validation.** Ни одного рецензированного исследования точности.
3. **False positive на non-native English** — 19%+. Для финансового контента на английском от non-native команды это проблема.
4. **Легко обходится** — синонимы, реструктуризация абзацев, human editing нарушают паттерны.
5. **Rate limits не задокументированы** — нет гарантии SLA.
6. **Документация тонкая** — Swagger есть, но примеров мало, error codes не описаны.
7. **Не определяет конкретную модель** — возвращает общий score, не "написано Claude" vs "написано GPT".
