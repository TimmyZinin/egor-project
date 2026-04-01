# Бэклог улучшения Citability — /expert-hunter

## Проблема

Citability (25 баллов, крупнейшая категория scoring) фактически не работает в production mode. Snippet из LinkedIn title не содержит media mentions. Все кандидаты получают 0 по этой категории.

## Спринты

### Sprint 1: Enrichment WebSearch по имени кандидата
**Статус: DONE (standalone second-pass tool)**
**Цель:** Для каждого кандидата из raw_search запустить дополнительный WebSearch по имени + media keywords. Сохранить найденные media mentions как evidence URLs.

Что делать:
1. Добавить функцию `enrich_citability(name, credentials)` в `hunt.py`
2. Для каждого кандидата выполнить поиск: `"{name}" ("Forbes" OR "Bloomberg" OR "CNBC" OR "WSJ" OR "Reuters")`
3. Сохранить найденные evidence URLs в derived candidate
4. Проставить citability tier на основе найденных mentions
5. Обновить scoring

Входные данные: имя кандидата + credentials из per-result enrichment
Выходные данные: citability tier + evidence URLs в derived_candidates JSON

### Sprint 2: Верификация credentials через FINRA BrokerCheck
**Статус: PLANNED**
Curl к brokercheck.finra.org по имени кандидата. Проверка Series 3/7/65.

### Sprint 3: Верификация CFA через CFA Institute Directory
**Статус: PLANNED**
Curl к directory.cfainstitute.org по имени.

### Sprint 4: University extraction
**Статус: PLANNED**
WebSearch `"{name}" university OR degree OR MBA OR PhD` → извлечение образования.

### Sprint 5: Location extraction из snippet
**Статус: PLANNED**
Regex/WebSearch для определения реальной локации вместо hardcode из --geo.

### Sprint 6: Native English quality check
**Статус: PLANNED**
Анализ LinkedIn постов (если доступны) для оценки уровня языка.
