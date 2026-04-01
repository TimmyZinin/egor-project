# /expert-hunter — Документация (Source of Truth)

Скилл Claude Code для поиска и ранжирования финансовых экспертов с LinkedIn.

## Назначение

Автоматизирует discovery финансовых экспертов для контент-проекта Егора. На выходе — CSV-таблица кандидатов с LinkedIn URL, credentials, scoring и объяснением выбора. Outreach НЕ входит в scope.

## Текущее состояние (MVP, одобрен 30 марта 2026)

Работающий прототип с двумя режимами запуска:
- **seed** — встроенный набор из 20 enriched кандидатов (для демо и калибровки)
- **scan-backed** — загрузка из JSON-файла с результатами реального поиска

## Структура репозитория

```
egor-project/
├── expert-hunter/               # Рабочая директория скилла
│   ├── SKILL.md                 # Определение скилла (source of truth)
│   ├── install.sh               # Установка в ~/.claude/skills/
│   ├── schema.py                # Модель данных, scoring, экспорт CSV/JSON
│   ├── build_candidates.py      # Основной pipeline (--from-scan | --seed)
│   ├── scan.py                  # Определения WebSearch запросов + парсер
│   └── scan_results_20260330.json  # Сохранённые результаты поиска (20 записей)
├── docs/
│   ├── README.md                # Этот файл (source of truth)
│   ├── wiki/
│   │   └── how-it-works.md      # Как скилл работает сейчас (step-by-step)
│   └── skill-expert-hunter-spec.md  # Расширенная спецификация (v1.0, для справки)
├── research.html                # Исследование + экспертная панель + кандидаты (GitHub Pages)
└── review-channel-egor/         # Bridge-канал Codex <-> Claude
```

## Установка и запуск

### Установка скилла

```bash
cd ~/egor-project/expert-hunter
./install.sh
# Копирует SKILL.md -> ~/.claude/skills/expert-hunter.md
```

### Режим 1: Seed (демо)

```bash
cd ~/egor-project/expert-hunter
python3 build_candidates.py --seed
```

Использует встроенный набор из 20 кандидатов с полным enrichment. Scores от 33 до 96. Выходные файлы: `candidates_full.seed.csv`, `candidates_shortlist.seed.csv` (+ JSON аналоги).

### Режим 2: Scan-backed (рабочий)

```bash
cd ~/egor-project/expert-hunter
python3 build_candidates.py --from-scan scan_results_20260330.json
```

Загружает кандидатов из JSON-файла с результатами WebSearch. Автоматически извлекает из snippet-ов: credentials (CFA, CFP, CPA, CMT, FRM через regex), media tier, seniority, company. Выходные файлы: `candidates_full.scan.csv`, `candidates_shortlist.scan.csv` (+ JSON аналоги).

### Как получить новый scan_results JSON

В Claude Code сессии:
1. Запустить WebSearch запросы из `scan.py` (по нишам: forex, stocks, crypto, personal_finance)
2. Собрать результаты в JSON по контракту (см. раздел "Входные данные")
3. Сохранить в `scan_results_YYYYMMDD.json`
4. Запустить `build_candidates.py --from-scan scan_results_YYYYMMDD.json`

## Входные данные

### Контракт scan JSON

Каждая запись ДОЛЖНА содержать:
- `linkedin_url` (str) — URL профиля LinkedIn
- `name` (str) — имя кандидата

Каждая запись МОЖЕТ содержать:
- `raw_snippet` (str) — используется для enrichment-эвристик (credentials, media, seniority)
- `niche` (str) — forex, stocks, crypto, personal_finance
- `scan_source` (str) — google_search, finra, cfa_directory
- `scan_timestamp` (str, ISO 8601)

### Seed данные

Встроенный массив `RAW` в `build_candidates.py`. 20 записей с полным enrichment (credentials, scoring details, company, location). Собраны из реального WebSearch 30 марта 2026.

## Выходные данные

### CSV (14 полей)

| Поле | Описание |
|------|----------|
| `name` | Полное имя кандидата |
| `linkedin_url` | URL профиля LinkedIn |
| `primary_role` | Текущая должность |
| `company` | Текущая компания |
| `location` | Страна (US, UK, Canada, Australia, Other) |
| `niche_tags` | Ниши через запятую (forex, stocks, crypto, personal_finance) |
| `credentials_claimed` | Заявленные сертификации (CFA, CFP, CPA, CMT, FRM) |
| `credentials_verified_or_signal` | Источник подтверждения (LinkedIn title, FINRA, media mention) |
| `evidence_links` | URL-ы подтверждений |
| `fit_score` | Итоговый score (0-100) |
| `fit_notes` | Разбивка score по категориям |
| `why_selected` | Объяснение почему кандидат подходит |
| `confidence` | high (70+), medium (50-69), low (<50) |
| `status` | candidate, shortlisted |

### Имена файлов

- `candidates_full.seed.csv` / `.json` — seed режим
- `candidates_full.scan.csv` / `.json` — scan-backed режим
- `candidates_shortlist.seed.csv` / `.json` — shortlist (top 20) seed
- `candidates_shortlist.scan.csv` / `.json` — shortlist (top 20) scan-backed

Режимы НЕ перезаписывают файлы друг друга.

## Модель скоринга

8 категорий, максимум 100 баллов. Hard cap на каждую категорию: `min(calculated, max)`.

| Категория | Max | Что измеряет |
|-----------|-----|-------------|
| **Citability** | 25 | Bloomberg/Forbes/WSJ = 25, CNBC/Reuters = 20, нишевые СМИ = 15, подкасты = 10, нет = 0 |
| **Credentials** | 20 | CFA = 20, CFP = 18, CPA = 16, CAIA/FRM = 15, Series 7 = 12. Множественные: max + min(3*extra, 5) |
| **Google Entity** | 15 | Knowledge Panel = 15, Google Scholar = 12, Rich SERP = 7, Basic SERP = 3, нет = 0 |
| **Associations** | 10 | CFA Institute = 10, NAPFA = 9, FPA = 8, AICPA = 8, Board member бонус = +2 |
| **LinkedIn Activity** | 10 | >10 posts/мес = 8, 5-10 = 6, 1-4 = 3, 0 = 0. Articles published = +2 (cap 10) |
| **Experience** | 10 | 20+ лет = 10, 15-19 = 8, 10-14 = 6, 5-9 = 4, <5 = 2 |
| **Location** | 5 | US = 5, UK = 5, Canada/Australia = 3, Other English-speaking = 2, Other = 0 |
| **Native English** | 5 | Confirmed = 5, Likely = 4, Fluent = 3, Unclear = 1 |

### Тиры

| Тир | Баллы | Рекомендация |
|-----|-------|-------------|
| A (Excellent) | 80-100 | Приоритетный кандидат |
| B (Good) | 60-79 | Хороший кандидат |
| C (Acceptable) | 40-59 | Запасной |
| D (Reject) | 0-39 | Не подходит |

### Scan-backed enrichment

При загрузке из scan JSON, функция `enrich_from_snippet()` автоматически извлекает:
- Credentials: regex по CFA, CFP, CPA, CMT, FRM, CAIA, Series 3/7/65
- Media tier: Tier 1 (Bloomberg/Forbes/WSJ), Tier 2 (CNBC/Reuters), Tier 3 (NerdWallet/Investopedia)
- Seniority: Chief/Head/Director/Senior/Lead/Managing/Partner/Professor -> experience 15+
- Company: regex из snippet (после " - " или " at ")
- Google Entity: inferred из длины snippet + credentials + media tier

## Ограничения (текущее состояние)

### Что НЕ работает сейчас

1. **Автоматический scan** — `scan.py` содержит запросы, но не выполняет WebSearch самостоятельно. Поиск запускается вручную в Claude Code сессии
2. **FINRA/CFA верификация** — credentials извлекаются из snippet-ов regex-ом, но не проверяются через официальные базы (brokercheck.finra.org, directory.cfainstitute.org)
3. **Jina Reader enrichment** — LinkedIn блокирует Jina Reader (HTTP 999/429). Профили обогащаются через Google search по имени
4. **Outreach** — вне scope скилла
5. **Режимы verify и report** — описаны в SKILL.md, но не реализованы в коде
6. **scan_results JSON** — собирается вручную из WebSearch результатов, не автоматически из scan.py output

### Что работает

1. Seed mode: полный pipeline с 20 enriched кандидатами -> CSV/JSON
2. Scan-backed mode: загрузка из JSON -> snippet enrichment -> differentiated scoring -> CSV/JSON
3. Scoring: rule-based, 8 категорий, hard cap, объяснимые результаты
4. Export: CSV 14 полей + JSON, mode-specific filenames
5. Install: `install.sh` устанавливает skill в Claude Code

## Citability Enrichment (Sprint 1 — реализован)

Отдельный standalone инструмент для обогащения кандидатов данными о цитируемости в медиа. **Не интегрирован в основной hunt.py pipeline** — запускается как отдельный второй проход.

### Как использовать

```bash
cd ~/egor-project/expert-hunter

# Шаг 1: Сгенерировать запросы для citability check
python3 enrich_citability.py --generate derived_candidates/forex_us.json
# -> citability_queries_forex_us.txt (запросы для оператора)

# Шаг 2: Оператор выполняет WebSearch для каждого запроса
# Сохраняет результаты в citability_raw/forex_us.json

# Шаг 3: Применить citability данные
python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json
# -> Обновляет derived_candidates/forex_us.json (citability_tier, evidence URLs)
# -> Генерирует candidates_forex_us_enriched.csv с пересчитанными scores
```

### Что добавляется к каждому кандидату

- `citability_tier`: bloomberg_wsj_forbes / cnbc_reuters / niche_finance_media / none
- `citability_outlets`: список найденных СМИ (["FXStreet", "InvestorPlace"])
- `citability_evidence_urls`: до 5 URL-ов с подтверждениями
- `citability_raw_source`: файл-источник для trace

### Текущее состояние

- Реализовано как standalone second-pass tool (`enrich_citability.py`)
- Протестировано на forex/US: 2 кандидата получили citability score (Mohammad Ali +15, John Jagerson +15)
- НЕ интегрировано в `hunt.py` — требует отдельного запуска
- Media tiers: Tier 1 (Bloomberg, Forbes, WSJ), Tier 2 (CNBC, Reuters, MarketWatch), Tier 3 (NerdWallet, Investopedia, FXStreet, DailyFX, InvestorPlace)

## Roadmap (что планируется)

### Ближайшее (следующие итерации)

1. **Расширение ниш** — stocks, crypto, personal_finance (сейчас только forex собран live)
2. **FINRA BrokerCheck верификация** — автоматическая проверка Series 3/7/65 через curl
3. **CFA Directory верификация** — проверка CFA charterholders
4. **Больше кандидатов** — цель 200+ через множественные WebSearch раунды

### Среднесрочное

5. **verify режим** — `/expert-hunter verify <linkedin_url>` с полным scorecard
6. **report режим** — `/expert-hunter report` со статистикой pipeline
7. **Automated scan** — scan.py сам выполняет поиск и сохраняет JSON
8. **HTML viewer** — генерация HTML из CSV для визуального просмотра

### Отложенное (не в scope MVP)

9. Outreach генерация
10. Anti-AI detection
11. Content generation pipeline
12. Proxycurl API интеграция ($0.01/profile)

## Связанные документы

- [Как скилл работает сейчас (step-by-step)](wiki/how-it-works.md)
- [Расширенная спецификация v1.0](skill-expert-hunter-spec.md) — для справки, НЕ source of truth
- [Исследование + экспертная панель](https://timzinin.com/egor-project/research.html) — GitHub Pages
