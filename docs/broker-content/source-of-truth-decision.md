# Решение: Source of Truth для контент-системы

> Версия: 1.0 | Дата: 2026-04-02
> Статус: РЕШЕНИЕ (требует согласования)
> Автор: Claude (executor session, task EGOR-BROKER-WRITER-RESEARCH-008)

---

## Вопрос

Где должна жить контент-система для broker reviews?

Варианты:
1. В `egor-project` (текущий репозиторий)
2. В `content-pipeline` (существующий репо Tim'а)
3. В новом отдельном репозитории

---

## Решение: оставить в `egor-project` на данном этапе

### Почему НЕ `content-pipeline`

**`content-pipeline` уже существует** — это Tim's personal SMM auto-publisher (n8n, 13 платформ, PostgreSQL, Scout→Writer→Publisher). Это **другая система** с другим назначением. Использовать то же имя или пытаться интегрировать — путаница.

### Почему НЕ новый репо (пока)

Предыдущая спецификация (`content-pipeline-spec.md`) предлагала отдельный репо `TimmyZinin/content-pipeline` (имя занято) или `TimmyZinin/rated-brokers` (из research.html). Аргументы за отдельный репо валидны, но **преждевременны**:

1. **Нет ни одного артефакта контента.** Система не сгенерировала ни одного текста. Создавать repo structure для пустой системы — over-engineering.
2. **Скиллы ещё не написаны.** Writer и checker — спецификации, не код. Spec может измениться после первого реального использования.
3. **Непонятна target platform.** Куда публиковать broker reviews? WordPress? Static site? Custom CMS? Это влияет на структуру репо, но ответа пока нет.
4. **`egor-project` уже содержит всё.** Research, expert-hunter, docs, review channel — всё в одном месте. Разделение до первого working prototype усложняет навигацию.

### Текущее решение: `egor-project/` с поддиректориями

```
egor-project/
├── expert-hunter/           # существует, работает
├── docs/                    # существует, спецификации
│   ├── broker-writer-spec.md      # NEW
│   ├── ahrefs-checker-spec.md     # NEW
│   ├── broker-writer-ahrefs-integration.md  # NEW
│   └── source-of-truth-decision.md          # NEW (этот файл)
├── review-channel-egor/     # существует, review protocol
├── content/                 # NEW — будущие артефакты контента
│   ├── manifest.json
│   └── {slug}/
│       ├── brief.md
│       ├── draft-v{N}.md
│       ├── review-v{N}.md
│       └── approved.md
├── brokers/                 # NEW — structured broker data
│   └── {slug}/
│       └── input.json
├── templates/               # NEW — review template, schema templates
│   ├── broker-review.md
│   ├── schema-review.json
│   └── schema-article.json
├── quality/                 # NEW — criteria, patterns, ahrefs results
│   ├── criteria.json
│   ├── humanization-patterns.md
│   └── ahrefs-checks/
│       └── {slug}.json
├── skills/                  # NEW — skill files (installed to ~/.claude/skills/)
│   ├── broker-writer.md
│   └── broker-checker.md
├── research.html            # существует
├── content-gen-research.html # существует
└── .wiki/                   # существует
```

---

## Когда выносить в отдельный репо

**Trigger для создания отдельного репозитория:**

1. ✅ Writer и checker работают и прошли ≥5 полных циклов
2. ✅ Определена целевая платформа публикации
3. ✅ Накопилось ≥10 артефактов контента (drafts, reviews)
4. ✅ Git history `egor-project` стала неудобной из-за mix research + content

Когда все 4 условия выполнены → создать `TimmyZinin/broker-content` (не `rated-brokers`, не `content-pipeline`).

### Что перенести при выделении

| Из egor-project/ | В broker-content/ |
|------------------|-------------------|
| `content/` | `content/` |
| `brokers/` | `brokers/` |
| `templates/` | `templates/` |
| `quality/` | `quality/` |
| `skills/` | `skills/` |
| Релевантные docs/ | `docs/` |

### Что остаётся в egor-project

| Директория | Причина |
|-----------|---------|
| `expert-hunter/` | Отдельный рабочий инструмент |
| `research.html` | Research, не production |
| `content-gen-research.html` | Research |
| `review-channel-egor/` | Review protocol (может использоваться для обоих) |
| `docs/` (research-specific) | Анализы, планы |

---

## Именование скиллов: окончательное решение

| Предыдущие имена | Решение | Причина |
|-----------------|---------|---------|
| `/rb-content-gen` (research.html) | `/broker-writer` | Яснее назначение: пишет broker review |
| `/rb-expert-scout` (research.html) | `/expert-hunter` | Уже существует и работает |
| `/broker-reviewer` (content-pipeline-spec.md) | `/broker-checker` | "Checker" точнее: автоматическая проверка, не редакционная рецензия |

---

## Что зеркалить

Пока всё в `egor-project`, зеркалирование не нужно.

При выделении в `broker-content`:
- `egor-project/docs/` сохраняет копии спецификаций (как archive/reference)
- `broker-content/` становится source of truth для контентной системы
- `expert-hunter/` может читать из обоих репо, но живёт в `egor-project`

---

## Открытые вопросы (требуют ответа перед реализацией)

1. **Целевая платформа публикации.** WordPress? Static site? Custom? Влияет на формат output и post-publish workflow.
2. **Ahrefs API key.** Есть ли у Егора? Какой план (Lite/Standard/Advanced)? Определяет доступные API endpoints и объём units.
3. **Expert integration.** Будет ли эксперт из expert-hunter реально ревьюить контент перед публикацией? Если да — нужен дополнительный state `human_review` между `approved` и `published`.
4. **Масштаб.** Сколько broker reviews в месяц? 5-10 → ручной workflow достаточен. 50+ → нужна автоматизация через n8n.
5. **Бюджет на AI detection.** Если нужна автоматическая pre-publish проверка → Originality.ai ($15-25/мес) или GPTZero ($10-30/мес). Если достаточно ручной Ahrefs → $0 extra.
