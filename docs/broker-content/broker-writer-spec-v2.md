# /broker-writer — Генерация обзоров брокеров

> Версия: 2.0 | Дата: 2026-04-02
> Статус: SPEC (финальная, на согласовании)
> Совместимость: broker-checker-spec.md, integration.md

Скилл Claude Code для генерации SEO-оптимизированных broker reviews на основе структурированных данных.

**Пишет**, но **не проверяет** и **не публикует**.

---

## Триггеры

`/broker-writer`, `напиши обзор брокера`, `broker review`, `write broker review`

## Команды

```bash
/broker-writer {slug}                    # Новый draft для брокера
/broker-writer {slug} --revise           # Ревизия по последнему review-v{N}.md
/broker-writer --list                    # Список брокеров со статусами
```

**Примеры:**
```
/broker-writer ig                        → content/ig/draft-v1.md
/broker-writer ig --revise               → content/ig/draft-v2.md (по review-v1.md)
/broker-writer --list                    → таблица slug | state | version
```

---

## Рабочая директория

```
~/egor-project/
├── brokers/{slug}/input.json            # Данные брокера (обязательно)
├── content/{slug}/
│   ├── brief.md                         # Бриф (обязательно)
│   ├── draft-v{N}.md                    # Черновики (output скилла)
│   ├── review-v{N}.md                   # Отчёты checker-а (input при --revise)
│   └── approved.md                      # Финальная версия (создаёт checker)
├── templates/
│   └── broker-review.md                 # Шаблон 18 секций (обязательно)
├── quality/
│   ├── humanization-patterns.md         # 24 anti-AI паттерна (обязательно)
│   └── criteria.json                    # Конфигурация checker-а
└── content/manifest.json                # State tracker (создаётся автоматически)
```

---

## Входные данные

### Обязательные (без них скилл не запускается)

| Файл | Формат | Откуда |
|------|--------|--------|
| `brokers/{slug}/input.json` | JSON | Человек заполняет вручную из данных брокера |
| `content/{slug}/brief.md` | Markdown | Человек создаёт (keywords, эксперт, конкуренты) |
| `templates/broker-review.md` | Markdown | Порядок и описание 18 секций |
| `quality/humanization-patterns.md` | Markdown | 24 anti-AI паттерна |

Если любой из файлов отсутствует → скилл выводит ошибку с указанием какой файл создать и ссылку на формат.

### Валидация входных данных

При запуске writer проверяет:

| Проверка | Ошибка |
|----------|--------|
| Файл не существует | "Missing file: {path}. See spec for format." |
| JSON невалиден (parse error) | "Invalid JSON in {path}: {parse error}" |
| Обязательное поле отсутствует (`broker_name`, `regulators`, `spreads`, `products`, `platforms`, `ratings`, `pros`, `cons`, `competitors`) | "Missing required field '{field}' in input.json" |
| Обязательное поле пустое (пустой массив/объект) | "Empty required field '{field}' in input.json" |
| `competitors` содержит <2 записи | "Need at least 2 competitors in input.json" |
| manifest.json существует но невалиден | "Corrupted manifest.json — backup and recreate" |
| manifest.json state не позволяет операцию | "Cannot create draft: state is '{state}', expected 'planned' or none" |

При ошибке валидации → скилл останавливается, не создаёт файлы.

### При ревизии (дополнительно)

| Файл | Формат | Откуда |
|------|--------|--------|
| `content/{slug}/review-v{N}.md` | Markdown | Output checker-а с секцией "Required Changes" |

---

## Формат input.json

Обязательные поля помечены `*`. Опциональные используются если есть — секция пишется с доступными данными.

```json
{
  "broker_name": "IG",                               // *
  "broker_slug": "ig",                                // *
  "year_founded": 1974,
  "headquarters": "London, UK",
  "publicly_traded": true,
  "stock_ticker": "IGG.L",

  "regulators": [                                     // *
    {"name": "FCA", "tier": 1, "country": "UK", "license": "195355"},
    {"name": "ASIC", "tier": 1, "country": "AU", "license": "515106"}
  ],

  "minimum_deposit": 0,
  "spreads": {                                        // *
    "eurusd_avg": 0.6,
    "gbpusd_avg": 0.9,
    "usdjpy_avg": 0.7
  },
  "commission_per_trade": "None (spread-only on standard)",
  "inactivity_fee": "$12/month after 2 years",
  "deposit_methods": ["Bank transfer", "Card", "PayPal"],
  "withdrawal_fee": "Free for bank transfer",

  "products": {                                       // *
    "forex_pairs": 80,
    "total_instruments": 17000,
    "stocks": true,
    "etfs": true,
    "options": true,
    "futures": true,
    "cfds": true,
    "crypto": false
  },

  "platforms": {                                      // *
    "proprietary": true,
    "mt4": true,
    "mt5": false,
    "tradingview": true,
    "mobile_app": true,
    "mobile_app_rating_ios": 4.4,
    "mobile_app_rating_android": 3.8
  },

  "ratings": {                                        // *
    "overall": 4.7,
    "fees": 4.5,
    "platforms": 4.8,
    "research": 4.6,
    "mobile": 4.5,
    "education": 4.3,
    "safety": 4.9
  },

  "pros": ["Low spreads", "Strong regulation", "17000+ instruments"],  // *
  "cons": ["No crypto", "Inactivity fee"],                             // *

  "competitors": [                                    // *
    {
      "name": "Saxo Bank",
      "slug": "saxo",
      "spreads_eurusd": 0.8,
      "min_deposit": 0,
      "total_instruments": 71000,
      "regulators": "FCA, DFSA, FSA",
      "overall_rating": 4.5
    },
    {
      "name": "CMC Markets",
      "slug": "cmc",
      "spreads_eurusd": 0.7,
      "min_deposit": 0,
      "total_instruments": 12000,
      "regulators": "FCA, ASIC, BaFin",
      "overall_rating": 4.3
    }
  ],

  "expert_name": "John Smith",
  "expert_credentials": "CFA, 15 years forex trading",
  "expert_take": "I tested IG for 3 months and was impressed by...",

  "best_for": [
    {"persona": "Advanced traders", "reason": "17000+ instruments, ProRealTime charting"},
    {"persona": "UK/EU traders", "reason": "FCA regulated, no minimum deposit"}
  ],

  "account_opening_steps": [
    "Visit IG website and click 'Create account'",
    "Fill personal details and verify identity",
    "Fund account via bank transfer or card",
    "Start trading on demo or live"
  ]
}
```

### Примечание: competitors блок

Блок `competitors` содержит базовые метрики 2-3 конкурентов для секций Fees Comparison и Competitor Comparison. Данные заполняет человек из публичных источников (сайты брокеров, обзоры). Writer использует только данные из `competitors` — **не выдумывает** метрики конкурентов.

### Примечание: expert-hunter

Скилл `/expert-hunter` помогает найти эксперта для атрибуции. Его output (name, credentials) может использоваться для полей `expert_name` и `expert_credentials`. Expert-hunter **не** генерирует брокерские данные (регуляторы, спреды, продукты).

---

## Формат brief.md

```markdown
# Brief: IG Review 2026

- **Target keywords:** ig review 2026, ig broker review, is ig safe
- **Angle:** comprehensive review for experienced traders
- **Expert:** John Smith (CFA, 15 years forex)
- **Competitors to compare:** Saxo Bank, CMC Markets
- **Notes:** emphasis on platform tools and research
- **Language:** English
```

---

## Output: 18 секций

Все 18 секций **обязательны** в каждом draft-е. Порядок фиксирован шаблоном `templates/broker-review.md`.

| # | Секция | Тип | ~Слов |
|---|--------|-----|-------|
| 1 | Hero (H1 + автор + дата + risk disclaimer) | Header | 50-100 |
| 2 | Verdict Box (рейтинг + саб-рейтинги + метрики) | Structured | 100-150 |
| 3 | Table of Contents | Auto-generated | anchor links |
| 4 | Pros & Cons + Key Takeaways | Lists | 150-200 |
| 5 | Trust & Safety (регуляторы, лицензии, таблица тиров) | Narrative + table | 300-500 |
| 6 | Fees & Pricing (спреды, комиссии, сравнение с 2 конкурентами из input.json) | Narrative + tables | 400-600 |
| 7 | Trading Platforms + Expert Take (blockquote) | Narrative + quote | 300-500 |
| 8 | Mobile App | Narrative + table | 200-300 |
| 9 | Product Selection (классы активов) | Table + narrative | 200-400 |
| 10 | Research & Education | Narrative + table | 200-300 |
| 11 | Account Opening (пошагово из input.json) | Steps | 150-200 |
| 12 | Competitor Comparison (данные из input.json competitors блока) | Table | 200-300 |
| 13 | Best For (персоны из input.json) | Narrative | 150-250 |
| 14 | Final Verdict | Narrative | 200-300 |
| 15 | Star Ratings Summary | Table | 50-100 |
| 16 | FAQ (≥5 вопросов) | Q&A | 300-500 |
| 17 | Methodology | Narrative | 100-200 |
| 18 | Editorial Team (автор + редактор) | Structured | 100-150 |

**Целевая длина:** 4000-5000 слов.

### Правило для отсутствующих данных

Все 18 секций всегда присутствуют. Если данных для секции нет в input.json:
- Секция сокращается до минимума
- Явно указывается: "Data not available — to be updated"
- Writer **никогда не выдумывает** данные, которых нет в input.json

---

## Обязательные элементы

- [ ] Risk disclaimer (CFD/forex risk, not financial advice) — в Hero
- [ ] Expert attribution (имя, credentials) — в Hero + Expert Take
- [ ] Schema.org JSON-LD: `Review` + `Article` + `Product` + `FAQPage` + `BreadcrumbList`
- [ ] ≥5 FAQ вопросов
- [ ] ≥10 плейсхолдеров внутренних ссылок `[→ INTERNAL: {topic}]`
- [ ] 3 CTA плейсхолдера (hero, mid-review, footer) — self-check only, checker не проверяет
- [ ] Expert Take blockquote в секции Trading Platforms
- [ ] Compliance disclaimer (footer)
- [ ] Word count ≥4000

Элементы с `[ ]` проверяются checker-ом (P0/P1), кроме CTA (self-check writer-а).

---

## Schema.org JSON-LD

5 типов (совместимо с checker-ом):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Review",
      "itemReviewed": {"@type": "Product", "name": "{broker_name}"},
      "reviewRating": {"@type": "Rating", "ratingValue": "{overall}", "bestRating": 5},
      "positiveNotes": {"@type": "ItemList", "itemListElement": [...]},
      "negativeNotes": {"@type": "ItemList", "itemListElement": [...]},
      "author": {"@type": "Person", "name": "{expert_name}"}
    },
    {
      "@type": "Article",
      "headline": "{broker_name} Review {year}"
    },
    {
      "@type": "Product",
      "name": "{broker_name}"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": "...", "acceptedAnswer": {"@type": "Answer", "text": "..."}}]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home"}, {"@type": "ListItem", "position": 2, "name": "Broker Reviews"}, {"@type": "ListItem", "position": 3, "name": "{broker_name} Review"}]
    }
  ]
}
```

---

## Шаг 0: INPUT COLLECT (интерактивный сбор данных)

При запуске `/broker-writer {slug}`:

1. Проверить существование `brokers/{slug}/input.json`
2. Если **существует** → перейти к шагу 1 (VALIDATE)
3. Если **не существует** → проверить текст постановки задачи:
   - Данные есть в постановке → парсить + дополнить с сайта брокера (Jina Reader) → сформировать JSON
   - Данных нет → войти в интерактивный диалог (10 блоков вопросов)
4. Показать сформированный `input.json` + `brief.md` человеку
5. **Ждать подтверждения** ("ок" / правки). Без подтверждения — не генерировать draft.
6. Сохранить файлы → перейти к шагу 1

### Диалог (10 блоков)

```
1. Основное: год, штаб-квартира, публичная?, тикер
2. Регуляторы*: лицензии (FCA, ASIC, CySEC...), номера
3. Комиссии*: спреды EUR/USD, комиссия/сделку, inactivity fee, мин. депозит
4. Продукты*: кол-во инструментов, forex пар, что есть (CFD/акции/ETF/крипто...)
5. Платформы*: собственная?, MT4/MT5?, TradingView?, мобильное приложение?
6. Рейтинги*: overall (1-5), fees, platforms, research, mobile, education, safety
7. Pros/Cons*: 3-5 плюсов, 2-3 минусов
8. Конкуренты* (мин. 2): для каждого — спреды, мин. депозит, инструменты, рейтинг
9. Эксперт: имя, credentials, expert take цитата
10. Brief: target keywords, угол подачи, особый фокус

[* = обязательно. "Не знаю" → Claude дополняет из открытых источников]
```

---

## Процесс генерации

```
1. VALIDATE    — проверить что input.json, brief.md, template, patterns существуют
2. READ        — загрузить все входные файлы
3. STRUCTURE   — пройтись по 18 секциям шаблона, определить доступные данные
4. DRAFT       — написать каждую секцию из данных input.json
5. HUMANIZE    — применить 24 anti-AI паттерна из quality/humanization-patterns.md
6. SEO         — keywords из brief.md в H1/H2, internal link плейсхолдеры, CTA
7. SCHEMA      — JSON-LD (Review + Article + Product + FAQPage + BreadcrumbList)
8. SELF-CHECK  — пройти чеклист обязательных элементов (18 секций, schema, word count)
9. SAVE        — content/{slug}/draft-v{N}.md
10. MANIFEST   — обновить content/manifest.json
11. COMMIT     — git commit: "content({slug}): draft v{N}"
```

### При --revise

Предусловия:
- `content/{slug}/review-v{N}.md` существует
- manifest.json state = `revision_requested`
- review содержит секцию "Required Changes"
- State `revision_requested` может быть установлен **только** checker-ом (не Ahrefs, не человеком напрямую)

Если Ahrefs/человек находит проблему после APPROVED → человек создаёт `review-v{N+1}.md` вручную с секцией "Required Changes" и вызывает checker для смены state.

Если предусловия не выполнены → ошибка с объяснением какое предусловие нарушено.

Процесс:
```
1. FIND REVIEW  — найти latest review-v{N}.md (по максимальному N)
2. READ         — review-v{N}.md + текущий draft-v{N}.md
3. PARSE        — извлечь пункты "Required Changes" (P0/P1/P2)
4. FIX          — исправить каждый пункт, начиная с P0
5. SELF-CHECK   — повторить чеклист
6. SAVE         — draft-v{N+1}.md (НИКОГДА не перезаписывать draft-v{N})
7. MANIFEST     — state: revision_requested → revised
8. COMMIT       — "content({slug}): draft v{N+1} (revision)"
```

### При --list

Читает `content/manifest.json` + сканирует `brokers/*/input.json`.

Output:
```
Slug    | State              | Draft | Brief
--------|--------------------+-------+------
ig      | drafted            | v1    | yes
etoro   | revision_requested | v2    | yes
saxo    | (no manifest)      | -     | no
```

Если `manifest.json` не существует → "No manifest found. Run /broker-writer {slug} to start."

---

## Правила гуманизации

Полный список: `quality/humanization-patterns.md` (24 паттерна, обязательный файл).

7 ключевых правил (subset, для быстрой справки):

1. **Конкретика:** "robust platform" → "17,000+ instruments across 6 asset classes"
2. **Нет generic transitions:** "Furthermore", "Moreover", "It's worth noting" → запрещены
3. **Нет AI-summary формул:** "In conclusion, {Broker} offers a comprehensive..." → свободный нарратив
4. **Вариативность длины:** чередовать короткие (5 слов) и длинные (25 слов) предложения
5. **Числа из input.json:** "low fees" → "EUR/USD spread from 0.6 pips"
6. **Несовершенства:** мелкие стилистические неровности, разговорные обороты
7. **Expert voice:** first-person в Expert Take, конкретный опыт

---

## State machine (manifest.json)

```json
{
  "ig": {
    "state": "drafted",
    "current_version": 1,
    "created_at": "2026-04-02T15:00:00Z",
    "updated_at": "2026-04-02T15:00:00Z"
  }
}
```

Транзакции writer-а:
- `(не существует)` → `drafted`
- `revision_requested` → `revised`

Writer **не может**: approved, rejected, published (→ checker или человек).

Создаётся автоматически при первом запуске если не существует.

---

## Чего скилл НЕ делает

- НЕ проверяет текст (→ `/broker-checker`)
- НЕ решает публиковать (→ человек)
- НЕ модифицирует существующий input.json (read-only после создания). Шаг 0 создаёт файл с подтверждения человека; после — read-only
- НЕ выдумывает данные, которых нет в input.json
- НЕ генерирует скриншоты (требуются реальные)
- НЕ запускает AI detection API
- НЕ перезаписывает существующие draft-ы (всегда новая версия)

---

## Версионирование

- `draft-v1.md`, `draft-v2.md`, ... — новый файл при каждой генерации
- Writer **НИКОГДА** не перезаписывает существующий draft
- При `--revise`: читает review-v{N} → создаёт draft-v{N+1}
- Version number = max existing version + 1

---

## Skill packaging

Формат: директория с `SKILL.md` (как expert-hunter).

```
~/egor-project/broker-writer/
├── SKILL.md                 # Определение скилла (этот файл → сокращённая версия)
└── install.sh               # cp SKILL.md ~/.claude/skills/broker-writer/SKILL.md
```

`SKILL.md` = сокращённая версия этой спеки: триггеры, команды, процесс, ссылки на полную спеку.
Полная спека остаётся в `docs/broker-content/broker-writer-spec-v2.md`.

---

## Зависимости

| Файл | Обязателен | Статус | Кто создаёт |
|------|:----------:|--------|-------------|
| `brokers/{slug}/input.json` | Да | Нужно создать для первого брокера | Человек |
| `content/{slug}/brief.md` | Да | Нужно создать для первого брокера | Человек |
| `templates/broker-review.md` | Да | Нужно создать (извлечь из SEO research) | Человек / Claude |
| `quality/humanization-patterns.md` | Да | Нужно создать (24 паттерна) | Claude |
| `quality/criteria.json` | Да (для checker) | Нужно создать | Claude |
| `content/manifest.json` | Авто | Создаётся writer-ом | Writer |

---

## Первый запуск (bootstrap)

```
1. Создать templates/broker-review.md (из docs/research/broker-review-seo-research.md)
2. Создать quality/humanization-patterns.md (24 паттерна из research)
3. Создать quality/criteria.json (конфигурация checker-а, см. broker-checker-spec.md)
4. Выбрать первого брокера (рекомендация: IG)
5. Создать brokers/ig/input.json (из research.html + сайт брокера)
6. Создать content/ig/brief.md (keywords, эксперт, конкуренты)
7. /broker-writer ig → content/ig/draft-v1.md
8. Прочитать draft, оценить качество
9. /broker-checker ig → content/ig/review-v1.md
10. Итерировать до APPROVED
```
