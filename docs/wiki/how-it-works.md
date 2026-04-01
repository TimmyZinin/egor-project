# Как /expert-hunter работает сейчас

Актуальное описание на 31 марта 2026. Основано на реальном состоянии кода.

## Общая схема

```
WebSearch (оператор) → raw_search/*.json → hunt.py → derived_candidates/*.json → CSV
                                                         ↓ (опционально)
                                            enrich_citability.py → enriched CSV
```

## Production pipeline: hunt.py

### Запуск

```bash
cd ~/egor-project/expert-hunter
python3 hunt.py --niche forex --geo US
```

### Что происходит внутри

1. **Поиск raw artifact**: `raw_search/{niche}_{geo}_*.json` (берёт latest по дате)
2. **Если найден**: загружает `raw_results` массив (title + url + snippet для каждого результата)
3. **Для каждого результата**:
   - Извлекает LinkedIn URL из url поля
   - Извлекает имя из title (regex: до " - " или до credentials)
   - Вызывает `enrich_candidate(name, url, snippet, niche, geo)`
4. **Enrichment из snippet**:
   - Credentials: regex `\bCFA\b`, `\bCFP\b`, `\bCPA\b`, `\bCMT\b`, `\bFRM\b`, `\bCAIA\b`, Series 3/7/65
   - Media tier: ищет Bloomberg/Forbes/WSJ (Tier 1), CNBC/Reuters (Tier 2), NerdWallet/Investopedia (Tier 3)
   - Seniority: Chief/Head/Director/Senior → experience 15+
   - Company: regex "at Company" из snippet
   - Location: из --geo параметра (hardcoded, не из snippet)
   - Native English: proxy — если есть credentials → likely_native
   - Google Entity: inferred из snippet length + credentials
   - Associations: inference из credentials (CFA → CFA Institute)
5. **Scoring**: `score_candidate()` из `schema.py` — 8 категорий, hard cap на каждую, max 100
6. **Trace**: каждый candidate получает `raw_source_file`, `raw_source_index`, `raw_source_title`, `raw_source_url`
7. **Export**: `derived_candidates/{niche}_{geo}.json` + `candidates_{niche}_{geo}.csv`
8. **Shortlist**: top 20 по score → `shortlist_{niche}_{geo}.csv`

### Если raw artifact НЕ найден

hunt.py генерирует запросы и инструкции для оператора:
```
[ACTION] Run these queries via WebSearch in Claude Code:
[QUERY 1] site:linkedin.com/in "CFA" ("forex" OR "FX") ...
[ACTION] Save ALL results as ONE JSON to: raw_search/{niche}_{geo}_YYYYMMDD.json
```

## Citability enrichment: enrich_citability.py (Sprint 1)

Standalone second-pass tool. НЕ интегрирован в hunt.py.

### Шаг 1: Генерация запросов

```bash
python3 enrich_citability.py --generate derived_candidates/forex_us.json
```

Создаёт `citability_queries_forex_us.txt` — по одному запросу на кандидата:
```
# Christopher Vecchio
"Christopher Vecchio" ("Forbes" OR "Bloomberg" OR "CNBC" OR ...)
```

### Шаг 2: Оператор выполняет WebSearch

Сохраняет результаты в `citability_raw/forex_us.json`:
```json
[{"name": "...", "results": [{"title": "...", "url": "...", "snippet": "..."}]}]
```

### Шаг 3: Применение

```bash
python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json
```

Обновляет derived_candidates JSON, добавляя:
- `citability_tier`: bloomberg_wsj_forbes / cnbc_reuters / niche_finance_media / none
- `citability_outlets`: ["FXStreet", "InvestorPlace"]
- `citability_evidence_urls`: до 5 URL-ов
- `citability_raw_source`: файл-источник

Пересчитывает scores и генерирует `candidates_forex_us_enriched.csv`.

## Файлы кода

| Файл | Что делает |
|------|-----------|
| `hunt.py` | Production entrypoint. Raw artifact → enrichment → scoring → CSV |
| `enrich_citability.py` | Sprint 1 citability. Generate queries → apply results |
| `schema.py` | ExpertCandidate dataclass, SCORING dict, score_candidate(), CSV/JSON export, shortlist() |
| `scan.py` | Query definitions (4 ниши), LinkedIn URL regex, snippet parser. Legacy, superseded by hunt.py |
| `build_candidates.py` | Legacy pipeline (--seed / --from-scan). Superseded by hunt.py |
| `SKILL.md` | Определение скилла для Claude Code |
| `install.sh` | Установка скилла в ~/.claude/skills/ |

## Что НЕ работает

1. **Автоматический WebSearch** — оператор запускает вручную
2. **FINRA/CFA верификация** — credentials из regex, не из баз
3. **LinkedIn scraping** — заблокирован (999/429)
4. **University extraction** — не реализовано, 0 баллов
5. **LinkedIn Activity** — не реализовано, 0 баллов (snippet не содержит)
6. **Location** — hardcoded из --geo, не из snippet
7. **Citability в hunt.py** — не интегрирован, отдельный `enrich_citability.py`
8. **Режимы verify, report** — не реализованы
