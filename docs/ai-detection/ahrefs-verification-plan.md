# План проверки текстов через Ahrefs AI Detection

## Контекст

Этот план описывает как проверять сгенерированные broker review тексты на AI detection через Ahrefs. Используется для Варианта 1 (собственный `/broker-writer` skill).

## Доступные инструменты Ahrefs для AI detection

### 1. Free AI Content Detector (без подписки)
- **URL:** https://ahrefs.com/writing-tools/ai-content-detector
- **Что делает:** вставляешь текст → получаешь probability score + highlighted passages
- **Ограничения:** несколько сот слов за раз, не bulk, web-only
- **Когда использовать:** проверка отдельных текстов до публикации

### 2. Page Inspect в Site Explorer (нужна подписка)
- **URL:** Site Explorer → вводишь URL → Page Inspect → вкладка AI Detector
- **Что делает:** анализирует опубликованную страницу, показывает AI probability, highlighted sections, предполагаемые модели
- **Ограничения:** страница должна быть опубликована и проиндексирована, по одной странице за раз
- **Когда использовать:** проверка после публикации

### 3. Top Pages → AI Content Level (нужна подписка)
- **URL:** Site Explorer → Top Pages → колонка "AI Content Level"
- **Что делает:** показывает AI score для каждой страницы в списке Top Pages сайта
- **Ограничения:** доступно для страниц в индексе Ahrefs. Export этой колонки запрошен пользователями но статус не подтверждён
- **Когда использовать:** мониторинг AI levels всего сайта

### 4. Site Audit → Page Explorer с AI фильтром (нужна подписка)
- **URL:** Site Audit → добавить проект → Page Explorer → фильтр по AI Content Level
- **Что делает:** при crawl каждой страницы проекта вычисляет AI content level. Можно фильтровать и сортировать все страницы по AI level
- **Ограничения:** нужно добавить сайт как проект, crawl занимает время, количество страниц зависит от плана
- **Когда использовать:** bulk audit всего сайта после публикации batch контента
- **Источник:** [Ahrefs Twitter announcement](https://x.com/ahrefs/status/1990464967691153805)

## Чего НЕТ

- **Public API endpoint для AI detection** — не найден в документации Ahrefs API v3 (проверено апрель 2026)
- **Программный batch check** — нельзя автоматически проверить 1000 текстов через API
- **Export AI Content Level** из Top Pages — запрошен пользователями, статус не подтверждён

## Workflow проверки для Варианта 1

### Этап A: Pre-publish check (до публикации)

```
1. Генерируем текст через /broker-writer skill
2. Копируем текст в Ahrefs Free AI Detector (https://ahrefs.com/writing-tools/ai-content-detector)
3. Получаем score:
   - High AI probability → возвращаем в humanization pass, правим highlighted секции
   - Low AI probability → готов к публикации
4. Repeat до acceptable score
```

**Ограничения этого этапа:**
- Ручной, по одному тексту за раз
- Free detector принимает несколько сот слов — для статьи 4000+ слов нужно проверять по частям
- Это screening tool, не absolute judge

### Этап B: Post-publish monitoring (после публикации)

```
1. Публикуем batch текстов на сайт
2. Добавляем сайт в Ahrefs Site Audit как проект (если ещё не добавлен)
3. Запускаем crawl
4. Идём в Page Explorer → фильтруем по AI Content Level
5. Страницы с высоким AI level → помечаем для human editing
6. В Site Explorer → Top Pages → смотрим AI Content Level колонку для каждой страницы
```

**Ограничения этого этапа:**
- Crawl занимает время (зависит от размера сайта и плана)
- AI Content Level появляется после того как Ahrefs проиндексирует страницу
- Нет программного способа автоматизировать этот мониторинг

### Этап C: Competitor benchmarking

```
1. Вводим URL конкурента (ForexBrokers.com, BrokerChooser.com) в Site Explorer
2. Top Pages → смотрим их AI Content Level
3. Устанавливаем benchmark: "наши страницы должны иметь AI level не выше чем у конкурентов"
```

## Acceptance criteria для текстов

Предлагаемые пороги (нужно калибровать после первых 10 текстов):

| AI Content Level | Действие |
|-----------------|---------|
| 0-20% | Публикуем без изменений |
| 20-50% | Дополнительный humanization pass, правка highlighted секций |
| 50-80% | Серьёзная переработка: human editing, добавление personal insights, перестройка абзацев |
| 80-100% | Не публикуем. Переписываем существенно или пишем заново с другим подходом |

**Важно:** эти пороги — стартовые. Нужно откалибровать по:
- AI levels конкурентов (benchmark)
- Корреляции AI level с ranking performance
- False positive rate на нашем типе контента

## Что нельзя сделать через Ahrefs

1. **Автоматическую pre-publish проверку через API** — нет такого endpoint
2. **Bulk text check до публикации** — только по одному тексту через web tool
3. **Real-time feedback loop** — skill не может автоматически получить Ahrefs score и решить publish/rewrite
4. **Guarantee прохождения** — Ahrefs detector ~80-85% accuracy (industry estimate), false positives/negatives неизбежны

## Альтернативные AI detection tools (для pre-publish automation)

Если нужен программный pre-publish check (чего Ahrefs не даёт):

| Tool | API? | Pricing | Accuracy (claimed) |
|------|------|---------|-------------------|
| Originality.ai | Да | $15-25/мес | 96%+ (claimed) |
| GPTZero | Да | $10-30/мес | 99%+ (claimed) |
| Copyleaks | Да | Custom | High (claimed) |
| Winston AI | Да | $12-18/мес | 99%+ (claimed) |

**Если нужна автоматизация:** Originality.ai или GPTZero API как pre-publish gate, Ahrefs как post-publish monitoring.

## Рекомендуемый итоговый workflow

```
/broker-writer генерирует текст
  ↓
[Pre-publish] Проверяем через Ahrefs Free AI Detector (manual, web)
  ↓ если AI score высокий
Humanization pass → повторная проверка
  ↓ если AI score приемлемый
Публикуем
  ↓
[Post-publish] Ahrefs Site Audit / Top Pages monitoring (bulk)
  ↓ если проблемы
Human editing опубликованных страниц
```
