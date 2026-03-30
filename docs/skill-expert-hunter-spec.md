# Skill: /expert-hunter — Спецификация v1.0

## Назначение

Скилл Claude Code для поиска, верификации и рекрутинга финансовых экспертов с LinkedIn для контент-проекта. Автоматизирует полный цикл: от определения критериев до генерации персонализированного outreach.

## Триггеры

- `/expert-hunter` — полный цикл поиска
- `/expert-hunter scan <niche>` — поиск экспертов в конкретной нише
- `/expert-hunter verify <linkedin_url>` — верификация одного эксперта
- `/expert-hunter outreach <linkedin_url>` — генерация outreach для конкретного эксперта
- `/expert-hunter batch <csv_path>` — пакетная обработка списка LinkedIn URL
- `/expert-hunter report` — отчёт по текущему пулу экспертов

## Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    /expert-hunter                            │
├─────────┬──────────┬───────────┬───────────┬───────────────┤
│  SCAN   │  ENRICH  │  VERIFY   │  SCORE    │   OUTREACH    │
│LinkedIn │ Profile  │ Credentials│ Weighted  │ Personalized  │
│ Search  │ Scraping │ Check     │ Ranking   │ Message Gen   │
└────┬────┴────┬─────┴─────┬─────┴─────┬─────┴──────┬────────┘
     │         │           │           │            │
     v         v           v           v            v
  Jina/API  LinkedIn   FINRA/CFA/   Scoring     Claude
  Reader    Profile    CFP/NFA      Algorithm   Outreach
            Parser     Databases                Generator
```

### Хранение данных

```
~/egor-project/
├── data/
│   ├── experts.json          # Основная БД экспертов
│   ├── outreach_log.json     # Лог отправленных outreach
│   ├── scoring_weights.json  # Веса скоринга (настраиваемые)
│   └── niches.json           # Определения ниш и ключевых слов
├── templates/
│   ├── outreach_initial.md   # Шаблон первого контакта
│   ├── outreach_followup.md  # Шаблон follow-up
│   └── outreach_offer.md     # Шаблон оффера
└── docs/
    └── skill-expert-hunter-spec.md  # Эта спецификация
```

## Модули

### 1. SCAN — Поиск кандидатов

#### 1.1 Источники поиска

| Источник | Метод | Приоритет |
|----------|-------|-----------|
| **LinkedIn** (основной) | Jina Reader (`curl -s "https://r.jina.ai/https://linkedin.com/in/{handle}"`) -> fallback: Google cache (`cache:linkedin.com/in/{handle}`) -> fallback: Bing cache -> fallback: Proxycurl API ($0.01/profile, для Tier A кандидатов) | P0 |
| **Google Search** | WebSearch: `site:linkedin.com/in "CFA" "forex" "financial advisor"` | P1 |
| **FINRA BrokerCheck** | `curl` к brokercheck.finra.org API | P2 |
| **CFA Institute Directory** | `curl` к directory.cfainstitute.org | P2 |
| **CFP Board** | `curl` к cfp.net/verify-a-cfp-professional | P2 |
| **Conference speakers** | Scraping speaker lists (FinovateFall, Money 20/20, T3) | P3 |
| **Medium и Substack** | WebSearch + Jina Reader для финансовых авторов | P3 |

#### 1.2 Boolean-запросы для LinkedIn

```
# Основные запросы (через Google site:linkedin.com)
"CFA charterholder" AND ("writer" OR "contributor" OR "columnist" OR "content")
"Certified Financial Planner" AND ("author" OR "speaker" OR "blogger")
"Series 7" AND ("freelance" OR "content creator" OR "financial writer")
"financial advisor" AND ("published" OR "Forbes" OR "Bloomberg" OR "CNBC")

# Нишевые запросы
"forex" AND "CFA" AND "analyst" site:linkedin.com/in
"investment" AND "CFP" AND ("writer" OR "contributor") site:linkedin.com/in
"personal finance" AND "CPA" AND "author" site:linkedin.com/in
```

#### 1.3 Параметры поиска

```json
{
  "max_candidates_per_scan": 50,
  "niches": [
    "forex_trading",
    "personal_finance",
    "investment_management",
    "retirement_planning",
    "tax_planning",
    "insurance",
    "real_estate_finance",
    "crypto_finance",
    "estate_planning",
    "credit_cards_banking"
  ],
  "locations": {
    "primary": ["United States", "United Kingdom"],
    "secondary": ["Canada", "Australia"],
    "weight": { "primary": 1.0, "secondary": 0.7 }
  }
}
```

#### 1.4 Minimum Viable Profile (MVP fields)

LinkedIn auth-wall может ограничить доступ к полному профилю. Определяем обязательные vs nice-to-have поля:

| Поле | Статус | Источник если LinkedIn заблокирован |
|------|--------|-------------------------------------|
| Name | **Обязательное** | Google snippet, FINRA BrokerCheck |
| Headline/Title | **Обязательное** | Google snippet |
| Location (country) | **Обязательное** | Google snippet, FINRA |
| Current company | Желательное | FINRA, CFA Directory |
| Certifications | **Обязательное** | FINRA, CFA, CFP databases напрямую |
| Education | Желательное | Google Scholar, конференции |
| About text | Желательное | Cached versions, personal website |
| Activity/posts | Nice-to-have | Google `site:linkedin.com/pulse "{name}"` |

Если обязательные поля не получены ни одним методом -> кандидат помечается `INCOMPLETE` и не проходит в SCORE.

#### 1.5 Deduplication

Перед ENRICH — обязательная дедупликация:
1. Exact match по `linkedin_url`
2. Fuzzy match по `name + current_company` (Levenshtein distance < 3)
3. При merge: сохранять данные из наиболее полного источника

#### 1.6 Выходные данные SCAN

Для каждого кандидата собирается raw profile:

```json
{
  "linkedin_url": "https://linkedin.com/in/expert-name",
  "name": "John Smith",
  "headline": "CFA | Senior Financial Analyst | Forbes Contributor",
  "location": "New York, NY",
  "connections": "500+",
  "about_text": "...",
  "experience": [...],
  "education": [...],
  "certifications_mentioned": ["CFA", "Series 7"],
  "publications_mentioned": ["Forbes", "Bloomberg"],
  "recent_posts_count": 12,
  "recent_articles_count": 3,
  "scan_timestamp": "2026-03-30T14:00:00Z",
  "scan_source": "google_search"
}
```

### 2. ENRICH — Обогащение профиля

#### 2.1 Данные для извлечения

Из LinkedIn-профиля (через Jina Reader):

| Поле | Источник | Обязательное |
|------|----------|-------------|
| Full name | LinkedIn headline | Да |
| Current position + company | Experience section | Да |
| Years of experience | Experience dates calculation | Да |
| Education (university, degree) | Education section | Да |
| Certifications listed | Certifications section | Да |
| Languages | Skills and Languages section | Нет |
| Publications and articles | Activity section, Articles tab | Нет |
| Media mentions | About section parsing | Нет |
| Contact info (email, website) | Contact section (если публичный) | Нет |
| Recent activity (posts, articles) | Activity feed | Нет |

#### 2.2 Дополнительное обогащение

После LinkedIn — проверить через WebSearch:

```
"{expert_name}" AND ("Forbes" OR "Bloomberg" OR "CNBC" OR "WSJ" OR "Reuters")
"{expert_name}" AND ("CFA" OR "CFP" OR "financial advisor")
"{expert_name}" site:scholar.google.com
```

Результат: список media mentions, citations, external publications.

#### 2.3 Структура обогащённого профиля

```json
{
  "id": "exp_001",
  "linkedin_url": "...",
  "name": "John Smith",
  "location": { "city": "New York", "state": "NY", "country": "US" },
  "native_english": true,
  "current_role": "Senior Financial Analyst",
  "current_company": "Goldman Sachs",
  "years_experience": 15,
  "education": [
    { "institution": "Columbia University", "degree": "MBA Finance", "year": 2011 }
  ],
  "certifications": {
    "claimed": ["CFA", "Series 7", "Series 66"],
    "verified": {},
    "verification_pending": ["CFA", "Series 7", "Series 66"]
  },
  "associations": [],
  "media_mentions": [
    { "outlet": "Forbes", "url": "...", "date": "2025-11-15" }
  ],
  "google_scholar": { "h_index": null, "citations": null, "profile_url": null },
  "linkedin_activity": {
    "posts_last_30d": 12,
    "articles_published": 3,
    "followers": "5,200+"
  },
  "writing_samples": [],
  "enrichment_timestamp": "2026-03-30T14:05:00Z"
}
```

### 3. VERIFY — Верификация credentials

#### 3.1 Автоматическая верификация

Для каждой заявленной сертификации — проверка по официальной базе:

| Сертификация | Метод верификации | Автоматизируемо? |
|-------------|-------------------|-----------------|
| **CFA** | `curl` к directory.cfainstitute.org + парсинг | Частично (поиск по имени, парсинг результата) |
| **CFP** | `curl` к cfp.net/verify-a-cfp-professional | Частично |
| **Series 3/7/65** | FINRA BrokerCheck API (`curl` к brokercheck.finra.org) | Да (есть API/форма) |
| **CPA** | CPAverify.org | Частично (поиск по имени + штат) |
| **CAIA** | Email member@caia.org | Нет (ручная) |
| **FRM** | GARP registry | Нет (ручная) |

#### 3.2 Алгоритм верификации

```python
# Псевдокод
for cert in expert.certifications.claimed:
    if cert in AUTO_VERIFIABLE:
        result = verify_via_database(cert, expert.name, expert.location)
        if result.found:
            expert.certifications.verified[cert] = {
                "status": "CONFIRMED",
                "source": result.database_url,
                "verified_at": now()
            }
        else:
            expert.certifications.verified[cert] = {
                "status": "NOT_FOUND",
                "note": "Name not found in registry. May be inactive or name mismatch."
            }
    else:
        expert.certifications.verified[cert] = {
            "status": "MANUAL_CHECK_REQUIRED",
            "instruction": f"Email {MANUAL_CONTACTS[cert]} to verify"
        }
```

#### 3.3 Верификация Native English

Автоматическая оценка по нескольким сигналам:

| Сигнал | Вес | Метод |
|--------|-----|-------|
| Локация (US/UK/CA/AU/NZ) | 0.3 | LinkedIn location |
| Образование в англоязычной стране | 0.25 | Парсинг education section |
| Качество LinkedIn постов | 0.35 | Анализ 3-5 последних постов через Claude (грамматика, терминология, естественность) |
| Язык профиля | 0.1 | LinkedIn language setting |

Результат: `native_english_score` от 0.0 до 1.0. Порог: >= 0.7 = "likely native".

#### 3.4 Выходные данные VERIFY

```json
{
  "verification_summary": {
    "credentials_confirmed": 2,
    "credentials_not_found": 0,
    "credentials_manual": 1,
    "native_english_score": 0.85,
    "location_tier": "primary",
    "overall_verification": "STRONG"
  }
}
```

### 4. SCORE — Скоринг кандидатов

#### 4.1 Модель скоринга

Weighted scoring model, 100 баллов максимум:

| Критерий | Вес | Макс. баллов | Как считается |
|----------|-----|-------------|---------------|
| **Сертификации** | 25% | 25 | CFA=25, CFP=22, CPA=20, Series 7=15, CAIA=18, FRM=18. Множественные = max(single) + min(3 * extra_count, 5). Hard cap: 25. |
| **Цитируемость** | 20% | 20 | Bloomberg/WSJ/Forbes=20, CNBC/Reuters=16, нишевые фин.СМИ=12, подкасты/YouTube=8, нет=0 |
| **Членство в ассоциациях** | 10% | 10 | CFA Institute=10, FPA=8, NAPFA=9, AICPA=8, Board member=+2 |
| **Университет** | 10% | 10 | Ivy League/Top-20 MBA=10, Relevant degree=7, Any degree=4, No degree=0 |
| **Native English** | 10% | 10 | native_english_score * 10 |
| **Локация** | 5% | 5 | US=5, UK=5, Canada or Australia=3.5, Other English-speaking=2, Other=0 |
| **LinkedIn активность** | 10% | 10 | >10 posts/мес=8, 5-10=6, 1-4=3, 0=0. Articles published: +2 (cap at 10 total). |
| **Опыт (годы)** | 10% | 10 | 20+=10, 15-19=8, 10-14=6, 5-9=4, <5=2 |

**Scoring formula:** Каждый критерий рассчитывается как raw points (0 до max), затем итоговый score = сумма raw points. Веса встроены в max points (certifications max=25 = 25% веса). Hard cap на каждый критерий: `min(calculated, max_points)`. Итого: max score = 100.

#### 4.2 Настраиваемые веса

Файл `data/scoring_weights.json`:

```json
{
  "certifications": 0.25,
  "citability": 0.20,
  "associations": 0.10,
  "university": 0.10,
  "native_english": 0.10,
  "location": 0.05,
  "linkedin_activity": 0.10,
  "experience_years": 0.10,
  "thresholds": {
    "excellent": 80,
    "good": 60,
    "acceptable": 40,
    "reject": 39
  }
}
```

#### 4.3 Скоринг-тиры

| Тир | Баллы | Действие |
|-----|-------|---------|
| **A (Excellent)** | 80-100 | Приоритетный outreach. Premium оффер. |
| **B (Good)** | 60-79 | Стандартный outreach. |
| **C (Acceptable)** | 40-59 | Outreach только если A+B не хватает до цели (10). |
| **D (Reject)** | 0-39 | Не контактировать. |

### 5. OUTREACH — Генерация outreach

#### 5.1 Персонализация

Для каждого кандидата Claude генерирует персонализированный outreach на основе:

1. **Их конкретных публикаций** — ссылка на конкретную статью/пост
2. **Их expertise areas** — упоминание тем, на которые они пишут
3. **Их credentials** — подчёркивание ценности их квалификации
4. **Value proposition** — что они получают (byline, backlinks, exposure, оплата)

#### 5.2 Шаблоны

**Initial Contact (LinkedIn message, max 300 символов):**
```
Hi {name}, your {specific_work_reference} caught my attention —
particularly {specific_insight}. Building a team of credentialed
experts for an authoritative finance review site. Interested in
a quick chat about contributing? {sender_name}
```

**Follow-up Email (если есть email):**
```
Subject: Expert contributor opportunity — {site_name}

Hi {name},

Following up on my LinkedIn message. I'm specifically looking
for {certification} professionals to review {niche_area} content
because readers (and Google) value verified expertise.

What we offer:
- Your byline with full credential bio
- Backlinks to {their_company_or_practice}
- ${compensation} per article
- Full editorial support

Recent example: [link to published expert content]

Worth 15 minutes this week?

{sender_name}
```

**Offer (после положительного ответа):**
```
Subject: Contributor details — {site_name}

Hi {name},

Excited to have you on board. Here's how it works:

1. You pick topics in {their_expertise_areas} (or we suggest)
2. Our team drafts content aligned with your voice and expertise
3. You review, add personal insights, approve
4. Published with your full byline, bio, and LinkedIn link

Compensation: ${amount} per article | {frequency}
First article: pilot (1 piece, no long-term commitment)

Attached: contributor guidelines, sample article, agreement.

{sender_name}
```

#### 5.3 Anti-spam правила

- Максимум 30 outreach в день (LinkedIn daily limit)
- Минимум 3 дня между initial и follow-up
- Максимум 2 follow-ups
- Персонализация обязательна (нет generic массовой рассылки)
- Каждый outreach логируется в `outreach_log.json` со state machine: `drafted → sent → viewed → responded → positive/negative → committed/declined`

## Режимы работы

### Режим 1: Full Pipeline (`/expert-hunter`)

Полный цикл: SCAN -> ENRICH -> VERIFY -> SCORE -> OUTREACH

1. Спрашивает нишу (или использует все 10)
2. Запускает поиск через все источники
3. Обогащает каждый найденный профиль
4. Верифицирует credentials
5. Скорит и ранжирует
6. Генерирует outreach для тиров A и B
7. Показывает отчёт с рекомендациями

**По умолчанию — полностью автономный режим.** Pipeline выполняется от SCAN до OUTREACH без остановок, с финальным отчётом.

При запуске с `--interactive` флагом — checkpoint-ы включены:
- После SCAN: "Найдено X кандидатов. Продолжить обогащение?"
- После SCORE: "Тир A: X, Тир B: Y, Тир C: Z. Генерировать outreach для A+B?"
- После OUTREACH: "Outreach готов для X экспертов. Ревью перед отправкой?"

### Режим 2: Single Expert (`/expert-hunter verify <url>`)

Быстрая проверка одного эксперта:
1. Скрапит LinkedIn профиль
2. Обогащает данными из поиска
3. Верифицирует все заявленные credentials
4. Выдаёт скор и рекомендацию

**Формат вывода:**
```
EXPERT ANALYSIS: John Smith
━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 82/100 (Tier A — Excellent)

Credentials:
  CFA .......... CONFIRMED (CFA Institute Directory)
  Series 7 ..... CONFIRMED (FINRA BrokerCheck, CRD# 1234567)

Citability:
  Forbes ........ 3 mentions (2024-2025)
  Bloomberg ..... 1 interview (2025)

Location: New York, US (Tier: Primary)
Native English: 0.92 (Likely native)
LinkedIn Activity: 15 posts/30d, 2 articles
Experience: 18 years

RECOMMENDATION: Priority outreach. Premium offer ($1,500+/article).
```

### Режим 3: Batch Processing (`/expert-hunter batch <csv>`)

Пакетная обработка списка:
1. Читает CSV с LinkedIn URL (одна колонка)
2. Запускает ENRICH -> VERIFY -> SCORE для каждого
3. Выдаёт ranked таблицу
4. Генерирует outreach только для тиров A+B

### Режим 4: Niche Scan (`/expert-hunter scan <niche>`)

Поиск по конкретной нише:
1. Использует предопределённые запросы для ниши
2. SCAN -> ENRICH -> SCORE (без VERIFY и OUTREACH)
3. Выдаёт top-20 кандидатов для дальнейшего review
4. **Score помечается как "UNVERIFIED ESTIMATE"** — credentials не проверены, scoring по заявленным данным

### Режим 5: Report (`/expert-hunter report`)

Отчёт по текущему состоянию рекрутинга:
```
EXPERT HUNTING REPORT — 2026-03-30
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target: 10 experts | Current: 4 committed

Pipeline:
  Scanned:     147 candidates
  Enriched:     89
  Verified:     52
  Tier A:       12 (8 contacted, 3 responded, 2 committed)
  Tier B:       23 (15 contacted, 5 responded, 2 committed)
  Tier C:       17 (not contacted)

Outreach Stats:
  Sent:          23
  Responded:      8 (34.8% response rate)
  Positive:       5 (21.7%)
  Committed:      4 (17.4%)

Gap to target:   6 more experts needed
Recommendation:  Contact remaining 4 Tier A + expand Tier B outreach
```

## Error Handling

| Ошибка | Действие | Retry |
|--------|---------|-------|
| Jina Reader 429/503 | Backoff 5s -> 15s -> 45s, затем fallback к Google cache | 3 retries |
| LinkedIn auth-wall (пустой профиль) | Fallback: Google cache -> Bing -> Proxycurl (для Tier A) -> mark INCOMPLETE | По fallback chain |
| FINRA BrokerCheck HTML change | Log warning, skip VERIFY для этого cert, mark MANUAL_CHECK | Нет retry |
| WebSearch rate limit | Backoff 10s, continue with partial data | 2 retries |
| experts.json locked | Wait 5s, retry 3x, write to session-specific file | 3 retries |
| Scoring input incomplete | Пропустить отсутствующий критерий (0 баллов), пометить в output | - |

## Технические ограничения

### LinkedIn access
- LinkedIn блокирует скрапинг. Основной метод: **Jina Reader** (`curl -s "https://r.jina.ai/https://linkedin.com/in/{handle}"`)
- Fallback: WebSearch для публичных данных
- Не использовать Playwright для LinkedIn (rate limits, blocks)
- Не требовать Sales Navigator API (платный)

### Rate limits
- Jina Reader: без жёстких лимитов, но вежливый crawling (1 req/2 sec)
- WebSearch: стандартные лимиты Claude Code
- FINRA BrokerCheck: публичная форма, без API key

### Хранение
- Все данные в JSON файлах (не БД)
- `experts.json` — append-only с версионированием через git
- Lockfile: `data/.experts.lock` (created before write, removed after). При обнаружении lock — ждать 5 сек, retry 3 раза, затем write to `data/experts_{session_id}.json` и merge при unlock
- Никаких PII в коммитах (LinkedIn URL и имена = публичные данные, OK)

## Зависимости

- **Claude Code** — основная платформа
- **Jina Reader** — `curl -s "https://r.jina.ai/{URL}"` — scraping LinkedIn
- **WebSearch** — поиск media mentions, Google Scholar, conference speakers
- **curl** — HTTP-запросы к верификационным базам
- **jq** — парсинг JSON (установлен через brew)
- **Нет внешних API keys** — всё работает через публичные источники

## Интеграции

### С другими скиллами

| Скилл | Интеграция |
|-------|-----------|
| `/offer` | Генерация персонального лендинга для эксперта (как outreach asset) |
| `/outreach` | Отправка outreach через email и LinkedIn DM |
| `/lead-machine` | Shared scoring model и pipeline архитектура |
| `/bank` | Хранение сгенерированного контента от экспертов |

### С Telegram MCP
- Уведомление Тиму при завершении batch scan
- Уведомление при получении ответа от эксперта (если интегрировано с email)

## Метрики успеха

| Метрика | Цель |
|---------|------|
| Time to first 10 experts | < 8 недель |
| Response rate on outreach | > 5% (industry avg) |
| Tier A/B ratio in pipeline | > 50% |
| Credential verification rate | > 80% автоматически |
| Cost per committed expert | < $200 (outreach effort) |

## Безопасность

- Не хранить пароли или API ключи в репо
- LinkedIn URL — публичные данные, не PII
- Outreach messages — не spam (персонализированные, <30/день, opt-out)
- FINRA/CFA данные — публичные верификационные базы, разрешено использовать
- Не собирать данные, которые человек не сделал публичными

## Версионирование

- v1.0 — MVP: SCAN + ENRICH + SCORE + manual outreach templates
- v1.1 — VERIFY автоматизация (FINRA, CFA, CFP)
- v1.2 — OUTREACH генерация с персонализацией
- v2.0 — Batch processing + pipeline automation + report dashboard
