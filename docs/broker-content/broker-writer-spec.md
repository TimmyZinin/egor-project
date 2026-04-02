# Спецификация: скилл `/broker-writer`

> Версия: 1.0 | Дата: 2026-04-02
> Статус: SPEC (не реализован)
> Автор: Claude (executor session, task EGOR-BROKER-WRITER-RESEARCH-008)

---

## Назначение

Скилл `/broker-writer` генерирует SEO-оптимизированные обзоры брокеров (broker reviews) на основе структурированных входных данных, шаблона из 18 секций и правил гуманизации текста.

Скилл **пишет**, но **не проверяет** и **не публикует**.

---

## Входные данные

### Обязательные

| Вход | Формат | Описание |
|------|--------|----------|
| `brokers/{slug}/input.json` | JSON | Структурированные данные брокера (комиссии, регуляторы, платформы, продукты) |
| `content/{slug}/brief.md` | Markdown | Бриф статьи: целевые ключевые слова, угол подачи, имя эксперта для атрибуции |
| `templates/broker-review.md` | Markdown | Шаблон обзора: 18 секций (из анализа ForexBrokers/BrokerChooser/NerdWallet) |
| `quality/humanization-patterns.md` | Markdown | 24 паттерна AI-текста, которых следует избегать (Wikipedia-based) |

### При ревизии (дополнительно)

| Вход | Формат | Описание |
|------|--------|----------|
| `content/{slug}/review-v{N}.md` | Markdown | Отчёт ревьюера с секцией "Required Changes" — список конкретных правок |

---

## Выходные данные

Скилл **обязан** произвести ВСЕ следующие артефакты:

### 1. Черновик статьи: `content/{slug}/draft-v{N}.md`

**Обязательные секции** (порядок из шаблона):

| # | Секция | Тип | Длина |
|---|--------|-----|-------|
| 1 | Hero (H1 + автор + дата + дисклеймер) | Шапка | 50-100 слов |
| 2 | Verdict Box (общий рейтинг + саб-рейтинги + метрики) | Структурированный | 100-150 слов |
| 3 | Table of Contents | Автогенерация | якорные ссылки |
| 4 | Pros & Cons + Key Takeaways | Списки | 150-200 слов |
| 5 | Trust & Safety (рейтинг, лицензии, таблица) | Нарратив + таблица | 300-500 слов |
| 6 | Fees & Pricing (обзор + сравнение с 2 конкурентами) | Нарратив + таблицы | 400-600 слов |
| 7 | Trading Platforms + Expert Take (инлайн-цитата) | Нарратив + blockquote | 300-500 слов |
| 8 | Mobile App | Нарратив + таблица | 200-300 слов |
| 9 | Product Selection (доступные классы активов) | Таблица + нарратив | 200-400 слов |
| 10 | Research & Education | Нарратив + таблица | 200-300 слов |
| 11 | Account Opening (пошагово) | Шаги | 150-200 слов |
| 12 | Competitor Comparison (3 брокера, таблица) | Таблица | 200-300 слов |
| 13 | Best For (персоны: для кого подходит / не подходит) | Нарратив | 150-250 слов |
| 14 | Final Verdict | Нарратив | 200-300 слов |
| 15 | Star Ratings Summary | Таблица | 50-100 слов |
| 16 | FAQ (≥5 вопросов) | Q&A | 300-500 слов |
| 17 | Methodology | Нарратив | 100-200 слов |
| 18 | Editorial Team (автор + редактор) | Структурированный | 100-150 слов |

**Целевая длина:** 4000-5000 слов (competitive SEO level).

**Обязательные элементы в черновике:**
- Schema.org JSON-LD блок: `Review` + `Article` + `Product` + `FAQPage` + `BreadcrumbList`
- Блок атрибуции автора (имя, фото, credentials, ссылка на профиль)
- Compliance disclaimers (CFD/forex risk, not financial advice)
- ≥5 вопросов в FAQ
- ≥10 плейсхолдеров внутренних ссылок (`[→ INTERNAL: topic]`)
- 3 CTA-плейсхолдера (hero, mid-review, footer)
- Инлайн Expert Take (blockquote с фото, в секции Trading Platforms)

### 2. Обновление манифеста: `content/manifest.json`

Транзакция состояния:
- `planned` → `drafted` (новый черновик)
- `revision_requested` → `revised` (ревизия после ревью)

### 3. Git-коммит

Формат: `content({slug}): draft v{N}`

---

## Процесс генерации (7 этапов)

```
1. DATA LOAD     — прочитать input.json, brief.md, template
2. TEMPLATE FILL — заполнить 18 секций данными из input.json
3. NARRATIVE     — развернуть структурированные данные в нарратив
4. EXPERT VOICE  — интегрировать Expert Take (from brief.md)
5. HUMANIZE      — применить 24 anti-AI паттерна к тексту
6. SEO PASS      — meta, headings, keyword density, internal links
7. SCHEMA        — сгенерировать JSON-LD (Review, Article, Product, FAQ, Breadcrumb)
```

---

## Правила гуманизации (ключевые)

Полный список: `quality/humanization-patterns.md`. Критичные:

1. **Нет списков прилагательных:** "robust, comprehensive, cutting-edge" → конкретные факты
2. **Нет generic transitions:** "Furthermore", "Moreover", "It's worth noting" → убрать или заменить
3. **Нет AI-summary формул:** "In conclusion, {Broker} offers..." → свободный нарратив
4. **Разная длина предложений:** чередовать 5-слов и 25-слов предложения
5. **Конкретные числа:** "low fees" → "EUR/USD spread from 0.6 pips"
6. **Несовершенства:** мелкие стилистические неровности, не идеально ровный текст
7. **First-person expert voice** в Expert Take: "I tested X for 3 months..."

---

## Чего скилл НЕ делает

- НЕ проверяет текст на AI detection (→ `broker-checker`)
- НЕ решает, публиковать ли (→ человек)
- НЕ модифицирует input.json (входные данные read-only)
- НЕ модифицирует review-отчёты (read-only)
- НЕ генерирует скриншоты платформ (требуются реальные)
- НЕ запускает Ahrefs API (→ отдельный процесс)

---

## Формат broker input.json

```json
{
  "broker_name": "IG",
  "broker_slug": "ig",
  "year_founded": 1974,
  "headquarters": "London, UK",
  "publicly_traded": true,
  "stock_ticker": "IGG.L",
  "regulators": [
    {"name": "FCA", "tier": 1, "country": "UK", "license": "195355"}
  ],
  "minimum_deposit": 0,
  "spreads": {
    "eurusd_avg": 0.6,
    "gbpusd_avg": 0.9
  },
  "commission_per_trade": "None (spread-only on standard)",
  "inactivity_fee": "$12/month after 2 years",
  "products": {
    "forex_pairs": 80,
    "total_instruments": 17000,
    "stocks": true,
    "etfs": true,
    "options": true,
    "futures": true,
    "cfds": true,
    "crypto": false
  },
  "platforms": {
    "proprietary": true,
    "mt4": true,
    "mt5": false,
    "tradingview": true,
    "mobile_app": true
  },
  "ratings": {
    "overall": 4.7,
    "fees": 4.5,
    "platforms": 4.8,
    "research": 4.6,
    "mobile": 4.5,
    "education": 4.3,
    "safety": 4.9
  },
  "pros": ["Low spreads", "Strong regulation", "17000+ instruments"],
  "cons": ["No crypto", "Inactivity fee"],
  "expert_take": "First-person quote from named expert",
  "expert_name": "...",
  "expert_credentials": "...",
  "best_for": [
    {"persona": "Advanced traders", "reason": "..."}
  ]
}
```

---

## Формат brief.md

```markdown
# Brief: {Broker} Review 2026

- **Target keywords:** ig review 2026, ig broker review, is ig safe
- **Angle:** comprehensive review for experienced traders
- **Expert:** {name} ({credentials})
- **Competitors to compare:** Saxo Bank, CMC Markets
- **Notes:** emphasis on platform tools and research
```

---

## Версионирование

- Черновики: `draft-v1.md`, `draft-v2.md`, ... — новый файл при каждой генерации
- Writer никогда НЕ перезаписывает существующий черновик
- При ревизии writer читает review-v{N}.md → создаёт draft-v{N+1}.md

---

## Валидация (self-check перед коммитом)

Writer проверяет собственный output перед сохранением:

- [ ] Все 18 секций из шаблона присутствуют
- [ ] Schema.org JSON-LD валиден (Review + Article + Product + FAQ + Breadcrumb)
- [ ] ≥5 FAQ вопросов
- [ ] ≥10 internal link плейсхолдеров
- [ ] Compliance disclaimers на месте
- [ ] Expert Take blockquote присутствует
- [ ] Word count ≥4000
- [ ] Manifest.json обновлён

---

## Зависимости

| Зависимость | Статус |
|------------|--------|
| Шаблон 18 секций | Спроектирован (broker-review-seo-research.md) — нужно извлечь в templates/ |
| Humanization patterns | Существуют как reference (claude-seo) — нужно оформить в quality/ |
| Input.json формат | Определён выше — нужно создать для первого брокера |
| Expert profiles | expert-hunter работает — нужна интеграция данных |
| Brief формат | Определён выше — нужно создать для первого брокера |
