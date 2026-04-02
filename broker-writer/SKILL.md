# /broker-writer — Генерация обзоров брокеров

Генерирует SEO-оптимизированные broker reviews (18 секций, 4000-5000 слов) на основе структурированных данных. Пишет, но не проверяет и не публикует.

## Триггеры

`/broker-writer`, `напиши обзор брокера`, `broker review`, `write broker review`

## Команды

```
/broker-writer {slug}              — новый draft (или интерактивный сбор данных)
/broker-writer {slug} --revise     — ревизия по feedback из review-v{N}.md
/broker-writer --list              — список брокеров со статусами
```

## Рабочая директория

`~/egor-project/`

## Процесс

### Шаг 0: INPUT COLLECT

При запуске `/broker-writer {slug}`:

1. Проверить существование `brokers/{slug}/input.json`
2. Если **существует** → перейти к шагу 1
3. Если **не существует** → проверить текст постановки задачи:
   - Данные есть в постановке → парсить + дополнить с сайта брокера (Jina Reader: `curl -s "https://r.jina.ai/{broker_url}"`) → сформировать JSON
   - Данных нет → войти в интерактивный диалог (10 блоков вопросов, см. ниже)
4. Показать сформированный `input.json` + `brief.md` человеку
5. **Ждать подтверждения** ("ок" / правки)
6. Сохранить файлы → перейти к шагу 1

#### Диалог сбора данных (10 блоков)

```
1. Основное: год, штаб-квартира, публичная?, тикер
2. Регуляторы*: лицензии (FCA, ASIC, CySEC...), номера
3. Комиссии*: спреды EUR/USD, комиссия/сделку, inactivity fee, мин. депозит
4. Продукты*: кол-во инструментов, forex пар, что доступно (CFD/акции/ETF/опционы/крипто)
5. Платформы*: собственная?, MT4/MT5?, TradingView?, мобильное приложение?
6. Рейтинги*: overall (1-5), fees, platforms, research, mobile, education, safety
7. Pros/Cons*: 3-5 плюсов, 2-3 минусов
8. Конкуренты* (мин. 2): для каждого — спреды, мин. депозит, инструменты, рейтинг
9. Эксперт: имя, credentials, expert take цитата (или из /expert-hunter)
10. Brief: target keywords, угол подачи, особый фокус

[* = обязательно. "Не знаю" → Claude дополняет из открытых источников]
```

### Шаг 1: VALIDATE

Проверить что существуют:
- `brokers/{slug}/input.json` — данные брокера
- `content/{slug}/brief.md` — бриф статьи
- `templates/broker-review.md` — шаблон 18 секций
- `quality/humanization-patterns.md` — 24 anti-AI паттерна

Если файл отсутствует → ошибка: "Missing: {path}. Run bootstrap or see docs/broker-content/broker-writer-spec-v2.md"

Валидация input.json:
- JSON парсится → если нет: "Invalid JSON: {error}"
- Обязательные поля: broker_name, broker_slug, regulators, spreads, products, platforms, ratings, pros, cons, competitors
- Пустые обязательные → "Empty required field: {field}"
- competitors < 2 → "Need ≥2 competitors"

### Шаг 2: GENERATE

```
1. READ        — input.json + brief.md + template + humanization patterns
2. STRUCTURE   — 18 секций из шаблона, маппинг данных
3. DRAFT       — написать каждую секцию из данных input.json
4. HUMANIZE    — применить 24 anti-AI паттерна
5. SEO         — keywords из brief.md в H1/H2, ≥10 internal link плейсхолдеров
6. SCHEMA      — JSON-LD (Review + Article + Product + FAQPage + BreadcrumbList)
7. SELF-CHECK  — чеклист (см. ниже)
8. SAVE        — content/{slug}/draft-v{N}.md
9. MANIFEST    — обновить content/manifest.json
10. COMMIT     — "content({slug}): draft v{N}"
```

### При --revise

Предусловия:
- `content/{slug}/review-v{N}.md` существует (latest по max N)
- `manifest.json` state = `revision_requested`
- Review содержит секцию "Required Changes"
- State `revision_requested` устанавливается **только checker-ом**

Если не выполнены → ошибка с объяснением.

Процесс: читает review → исправляет каждый пункт Required Changes (P0 первыми) → self-check → сохраняет draft-v{N+1}.md (НИКОГДА не перезаписывает) → manifest: revised → commit.

### При --list

Читает `content/manifest.json` + сканирует `brokers/*/input.json`.

```
Slug    | State              | Draft | Brief
--------|--------------------+-------+------
ig      | drafted            | v1    | yes
etoro   | revision_requested | v2    | yes
saxo    | (no manifest)      | -     | no
```

## 18 обязательных секций

| # | Секция | ~Слов |
|---|--------|-------|
| 1 | Hero (H1 + автор + дата + risk disclaimer) | 50-100 |
| 2 | Verdict Box (рейтинг + метрики) | 100-150 |
| 3 | Table of Contents | auto |
| 4 | Pros & Cons + Key Takeaways | 150-200 |
| 5 | Trust & Safety (регуляторы, тиры) | 300-500 |
| 6 | Fees & Pricing (+ сравнение из competitors) | 400-600 |
| 7 | Trading Platforms + Expert Take (blockquote) | 300-500 |
| 8 | Mobile App | 200-300 |
| 9 | Product Selection | 200-400 |
| 10 | Research & Education | 200-300 |
| 11 | Account Opening | 150-200 |
| 12 | Competitor Comparison (из competitors блока) | 200-300 |
| 13 | Best For | 150-250 |
| 14 | Final Verdict | 200-300 |
| 15 | Star Ratings Summary | 50-100 |
| 16 | FAQ (≥5 вопросов) | 300-500 |
| 17 | Methodology | 100-200 |
| 18 | Editorial Team | 100-150 |

**Целевая длина:** 4000-5000 слов. Все 18 секций всегда присутствуют.

Если данных для секции нет → секция сокращена + "Data not available — to be updated". Никогда не выдумывать данные.

## Self-check (перед сохранением)

- [ ] Все 18 секций присутствуют
- [ ] Schema.org JSON-LD: Review + Article + Product + FAQPage + BreadcrumbList
- [ ] ≥5 FAQ вопросов
- [ ] ≥10 internal link плейсхолдеров `[→ INTERNAL: {topic}]`
- [ ] 3 CTA плейсхолдера (self-check, checker не проверяет)
- [ ] Expert Take blockquote
- [ ] Risk disclaimer (Hero) + Compliance disclaimer (footer)
- [ ] Word count ≥4000
- [ ] Manifest обновлён

## 7 ключевых правил гуманизации

Полный список: `quality/humanization-patterns.md` (24 паттерна).

1. Конкретика: "robust" → "17,000+ instruments across 6 asset classes"
2. Нет "Furthermore", "Moreover", "It's worth noting"
3. Нет "In conclusion, {X} offers a comprehensive..."
4. Чередовать короткие (5 слов) и длинные (25 слов) предложения
5. Числа из input.json: "low fees" → "EUR/USD spread from 0.6 pips"
6. Мелкие несовершенства, разговорные обороты
7. Expert voice в Expert Take: first-person, конкретный опыт

## Чего скилл НЕ делает

- НЕ проверяет текст (→ /broker-checker)
- НЕ публикует (→ человек)
- НЕ выдумывает данные
- НЕ перезаписывает существующие draft-ы

## Полная спецификация

`docs/broker-content/broker-writer-spec-v2.md`
