# Инструкция по использованию /expert-hunter

## Что это

Скилл для поиска и ранжирования финансовых экспертов с LinkedIn. На выходе — CSV-таблица кандидатов с LinkedIn URL, credentials, scoring и объяснением выбора.

## Репозиторий

https://github.com/TimmyZinin/egor-project

## Быстрый старт

```bash
# 1. Клонировать репо
git clone https://github.com/TimmyZinin/egor-project.git
cd egor-project/expert-hunter

# 2. Запустить поиск по forex/US (из готовых данных)
python3 hunt.py --niche forex --geo US

# Доступные ниши: forex, stocks, crypto, personal_finance
# Доступные geo: US, UK, CA, AU
```

## Что на выходе

- `candidates_{niche}_{geo}.csv` — все кандидаты, 14 полей, sorted by score
- `shortlist_{niche}_{geo}.csv` — top 20
- `derived_candidates/{niche}_{geo}.json` — JSON с trace до raw search

## Scoring (0-100)

- 80+ (Tier A) — приоритетный кандидат
- 60-79 (Tier B) — хороший
- 40-59 (Tier C) — запасной
- <40 (Tier D) — не подходит

8 категорий: Citability (25), Credentials (20), Google Entity (15), Associations (10), LinkedIn Activity (10), Experience (10), Location (5), Native English (5).

## Текущие ограничения (честно)

1. **Поиск — полуавтоматический.** Оператор (Claude Code сессия) выполняет WebSearch, сохраняет raw JSON в `raw_search/`, скрипт обрабатывает. Это не полностью автоматический pipeline.
2. **Credentials не верифицированы** через FINRA/CFA базы — извлечены из snippet-ов regex-ом.
3. **LinkedIn профили не скрапятся** (LinkedIn блокирует) — данные из Google search snippets.
4. **Outreach НЕ входит** в scope скилла.

## Структура данных

```
expert-hunter/
├── raw_search/          # Raw WebSearch артефакты (JSON с query + results)
├── derived_candidates/  # Parsed кандидаты с trace до raw
├── fixtures/            # Test fixtures для воспроизводимых тестов
├── hunt.py              # Production entrypoint
├── schema.py            # Scoring + export
└── SKILL.md             # Определение скилла
```

## Как добавить новые данные

1. В Claude Code выполнить WebSearch по нужной нише
2. Сохранить результаты в `raw_search/{niche}_{geo}_YYYYMMDD.json`
3. Запустить `python3 hunt.py --niche {niche} --geo {geo}`
