# /expert-hunter — Поиск и ранжирование финансовых экспертов

Скилл для поиска финансовых экспертов с LinkedIn по критериям Егора. На выходе — CSV с кандидатами, scores и LinkedIn URL.

## Триггеры

`/expert-hunter`, `найди экспертов`, `expert search`, `поиск экспертов`

## Текущий рабочий path (production)

### Основной pipeline: `hunt.py`

```bash
cd ~/egor-project/expert-hunter
python3 hunt.py --niche forex --geo US
```

Параметры:
- `--niche`: forex, stocks, crypto, personal_finance
- `--geo`: US, UK, CA, AU
- `--all-niches`: все ниши за один запуск
- `--test-fixture <path>`: тест с fixture JSON (без интернета)

### Как работает

1. Оператор выполняет WebSearch в Claude Code, сохраняет raw JSON в `raw_search/`
2. `hunt.py` загружает raw artifact → извлекает LinkedIn URLs → enrichment из snippet → scoring → CSV
3. Если raw artifact не найден — генерирует запросы для оператора

### Citability enrichment (отдельный второй проход)

```bash
# Сгенерировать запросы
python3 enrich_citability.py --generate derived_candidates/forex_us.json

# Оператор выполняет WebSearch по каждому кандидату

# Применить результаты
python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json
```

## Выходные файлы

- `candidates_{niche}_{geo}.csv` — все кандидаты (14 полей)
- `shortlist_{niche}_{geo}.csv` — top 20
- `derived_candidates/{niche}_{geo}.json` — JSON с trace до raw
- `candidates_{niche}_{geo}_enriched.csv` — после citability enrichment

## Scoring (8 категорий, max 100)

| Категория | Max | Что измеряет |
|-----------|-----|-------------|
| Citability | 25 | Media mentions (Bloomberg=25, CNBC=20, нишевые=15) |
| Credentials | 20 | CFA=20, CFP=18, CPA=16 (regex из snippet) |
| Google Entity | 15 | SERP presence |
| Associations | 10 | CFA Institute=10, FPA=8 (inference из credentials) |
| LinkedIn Activity | 10 | Не реализовано (snippet не содержит) |
| Experience | 10 | Seniority из snippet (Chief/Head=15+ лет) |
| Location | 5 | Из --geo параметра (не из snippet) |
| Native English | 5 | Proxy: credentials=likely native |

## Ограничения (честно)

- Поиск полуавтоматический: оператор запускает WebSearch, скрипт обрабатывает
- Credentials не верифицированы через FINRA/CFA (regex из snippet)
- LinkedIn профили не скрапятся (блокировка)
- University, LinkedIn Activity — не реализованы (0 баллов)
- Location hardcoded из --geo
- Citability enrichment — отдельный второй проход, не в hunt.py
- Режимы verify и report — не реализованы

## Структура данных

```
expert-hunter/
├── hunt.py                  # Production entrypoint
├── enrich_citability.py     # Sprint 1: citability enrichment
├── schema.py                # Scoring + export
├── raw_search/              # Raw WebSearch artifacts (JSON)
├── derived_candidates/      # Parsed candidates с trace
├── citability_raw/          # Citability WebSearch results
├── fixtures/                # Test fixtures
├── SKILL.md                 # Этот файл
└── install.sh               # Установка в ~/.claude/skills/
```
