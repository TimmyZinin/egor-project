# Trustpilot: рейтинги AI-детекторов

> Версия: 1.0 | Дата проверки: 2026-04-02
> Статус: RESEARCH
> Автор: Claude (executor session)

---

## Сводная таблица

| Параметр | GPTZero | ZeroGPT | Grammarly |
|----------|---------|---------|-----------|
| **TrustScore** | 2.5/5 | 1.3/5 | 3.5/5 |
| **Категория Trustpilot** | Poor | Bad | Average |
| **Кол-во отзывов** | 122 | 105 | 10,399 |
| **Профиль заявлен** | Да | Нет | Да (Paid) |
| **Основная функция** | AI Detection | AI Detection | Writing Assistant |
| **URL** | trustpilot.com/review/gptzero.me | trustpilot.com/review/zerogpt.com | trustpilot.com/review/grammarly.com |

---

## GPTZero (2.5/5, 122 отзыва)

### Распределение звёзд (оценка по первой странице)
- 5-star: ~25% (minority positive)
- 4-star: ~0%
- 3-star: ~0%
- 2-star: ~5%
- 1-star: ~65-70%

[APPROXIMATE — Trustpilot не экспортирует точное распределение]

### Негативные темы
1. **False positives (доминирующая жалоба):** Человеческий текст помечается как AI. Примеры:
   - 10-летние работы, написанные задолго до ChatGPT, помечены как 80% AI
   - Главы романов, написанных до AI → flagged as AI
   - WhatsApp сообщения → flagged as AI
   - Typing pattern recorder показывает 100% human input → текст всё равно 100% AI
2. **Академический вред:** Студенты обвинены в плагиате на основе GPTZero; "ruining my writing" — пользователи искажают свой стиль
3. **Непоследовательность:** Результаты меняются между проверками; "always shows ~50% AI regardless"
4. **Подписка:** Сложность отмены, повторяющаяся жалоба
5. **Маркетинг:** Заявляют 99% accuracy, пользователи опровергают

### Позитивные темы
- Полезен для учителей (проверка студенческих работ)
- Хороший free plan с summaries
- Платный план: статистика и сохранение документов
- Описательная информация о AI vs human частях

### Характерная цитата
> "I tested it by pasting a chapter from a novel I wrote before any launch of AI chat bots, and it flagged it as AI! This is ridiculous."
> — Christopher Burton, январь 2026

---

## ZeroGPT (1.3/5, 105 отзывов)

### Распределение звёзд (оценка по первой странице)
- 5-star: ~8%
- 4-star: ~0%
- 3-star: ~0%
- 2-star: ~0%
- 1-star: ~85-90%

[APPROXIMATE]

### Негативные темы
1. **Экстремальные false positives:** Человеческие эссе → 100% AI. При перефразировании flagged текста AI score **увеличивается** (40% → 70%)
2. **False negatives:** Текст из ChatGPT → "0% ChatGPT" (стихотворение целиком скопировано из ChatGPT = "0% AI")
3. **Непоследовательность:** Один документ: 27% AI, затем 75% AI через секунды без изменений
4. **Billing scam:** Годовая подписка вместо месячной; сложность возврата
5. **Массовые ложные обвинения:** "Half the class fell victim to false claims"
6. **Качество сайта:** "poorly put together", нет подробных объяснений

### Позитивные темы (минимум)
- Простой интерфейс
- Подсветка конкретных предложений
- Небольшое количество пользователей находят "reliable and effective"

### Характерные цитаты
> "Please, PLEASE just use any other site if you're a teacher reading this. Half the class fell victim to false claims while every other AI detector proved our work to be original."
> — Jake, август 2025

> "Fake checker. I copy and pasted an entire poem from ChatGPT and it said it was 0% ChatGPT."
> — Kaiya Amin, июнь 2025

### Профиль не заявлен
ZeroGPT **не заявил** свой профиль на Trustpilot — компания не отвечает на отзывы и не управляет своей репутацией. Это дополнительный red flag.

---

## Grammarly (3.5/5, 10,399 отзывов)

### Распределение звёзд (оценка по первой странице)
- 5-star: ~25%
- 4-star: ~15%
- 3-star: ~10%
- 2-star: ~25%
- 1-star: ~25%

[APPROXIMATE — распределение гораздо равномернее, чем у AI-детекторов]

### Важный контекст
Grammarly — это **writing assistant**, не AI-детектор. AI detection — лишь одна из множества функций. Подавляющее большинство отзывов (>95%) касаются проверки грамматики, подписки и UI — **не AI detection**. Очень мало отзывов упоминают AI detection специфически.

### Негативные темы
1. **Billing-проблемы (доминирующая жалоба):** Неожиданные списания после trial, удвоение цены, сложность отмены
2. **Навязчивый UI:** Overlay блокирует редактируемый текст; "green icon always in the way"
3. **Отмена Office plugin:** Миграция на новый формат — "much more difficult and labour-intensive"
4. **Upselling:** Free версия постоянно push-ит Premium

### Позитивные темы
- Отличная проверка грамматики (core function)
- Экономия времени
- Помощь с резюме и документами
- Лучше ProWritingAid (в сравнениях)
- Быстрая поддержка клиентов (в некоторых случаях)
- Универсальность: академия, бизнес, casual

---

## Вывод для проекта

### 1. Ни один AI-детектор не имеет хорошей пользовательской репутации
Оба специализированных инструмента (GPTZero 2.5/5, ZeroGPT 1.3/5) имеют крайне негативные рейтинги. Доминирующая проблема — false positives.

### 2. ZeroGPT — наихудший по доверию
1.3/5 + незаявленный профиль + сочетание false positives И false negatives. Это ставит под вопрос рекомендацию "начать с ZeroGPT". Возможно, стоит начать сразу с GPTZero (2.5/5) несмотря на более высокую цену.

### 3. Grammarly нерелевантен
Trustpilot данные по Grammarly не отражают качество AI detection — почти все отзывы о grammar checking.

### 4. Стратегия подтверждена
AI detection = advisory signal, не gatekeeper. Ни один из инструментов не может быть единственным критерием для publish/reject. Human review обязателен.

---

## Источники

- https://www.trustpilot.com/review/gptzero.me
- https://www.trustpilot.com/review/zerogpt.com
- https://www.trustpilot.com/review/grammarly.com
- Дата проверки: 2 апреля 2026
