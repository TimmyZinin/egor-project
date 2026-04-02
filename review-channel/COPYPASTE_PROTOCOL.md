# COPYPASTE PROTOCOL

## Purpose

Этот каталог нужен как мост между сессией Codex и сессией Claude.
Через него передаются:
- актуальный scope;
- принятые решения;
- открытые вопросы;
- следующий конкретный ask;
- артефакты, которые Claude обязан сделать.

Правило:
- в любой момент времени source of truth находится в этом файле;
- если Claude отвечает чем-то, что противоречит этому файлу, приоритет у этого файла.

## Current Goal

Сделать рабочий skill для Claude Code, который помогает найти и отобрать экспертов для последующего ручного аутрича.

MVP scope:
- ниши: `forex`, `stocks`, `crypto`, `personal finance`;
- гео-фокус: `US + англоязычные рынки`;
- выход по умолчанию: `CSV`;
- дополнительный просмотр: допустим HTML-рендер поверх CSV;
- результат должен включать все найденные записи и отдельно shortlist top-20.

## Out Of Scope

- outreach;
- шаблоны сообщений;
- email/DM automation;
- anti-AI detection;
- SEO-исследования ради исследований;
- декоративные HTML-отчёты.

## Expected Deliverable

Рабочий skill, который выдаёт таблицу экспертов-кандидатов с LinkedIn-ссылками и объяснимым short-list.

Также skill должен:
- сохранять полный набор найденных кандидатов;
- строить shortlist top-20;
- разделять `claimed` и `verified_or_signal`;
- быть ориентирован на автора с публичным digital footprint.

## Canonical Output Schema

Каждая строка таблицы должна содержать:

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Полное имя кандидата |
| `linkedin_url` | yes | Прямая ссылка на профиль |
| `primary_role` | yes | Основная текущая роль |
| `company` | preferred | Компания или практика |
| `location` | yes | Страна или город/страна |
| `niche_tags` | yes | Одна или несколько ниш |
| `credentials_claimed` | yes | Что заявлено кандидатом |
| `credentials_verified_or_signal` | yes | Что реально подтверждено или каким сигналом подтверждается |
| `evidence_links` | yes | Ссылки на доказательства отбора |
| `fit_score` | yes | Объяснимый скор |
| `fit_notes` | yes | Краткое объяснение скора |
| `why_selected` | yes | Почему кандидат попал в shortlist |
| `confidence` | yes | `high` / `medium` / `low` |
| `status` | yes | Для MVP: `candidate` |

## Iteration Rules

Каждая итерация Claude должна возвращать только одно из двух:

1. `DELIVERABLE_UPDATE`
   - что реализовано;
   - какие файлы созданы/изменены;
   - как это запускать;
   - что ещё осталось.

2. `QUESTIONS_FOR_CODEX`
   - только реально блокирующие вопросы;
   - без лишнего текста;
   - с объяснением, почему без ответа нельзя продолжать.

## Decision Log

### Fixed Decisions

- Цель: shortlist экспертов, не аутрич.
- Основной выход: таблица кандидатов.
- LinkedIn URL обязателен в результате.
- Skill должен быть рабочим, а не только описанным.
- Claimed и verified сигналы должны быть разделены.
- Критерии Егора:
  - цитируемость;
  - сданные экзамены;
  - членство в ассоциациях;
  - университет;
  - native English;
  - локация `US, UK + ?`;
- Целевые ниши MVP:
  - `forex`
  - `stocks`
  - `crypto`
  - `personal finance`
- Гео-фокус MVP:
  - `US`
  - другие англоязычные рынки допустимы
- Подходящий эксперт для MVP:
  - автор с публичным digital footprint;
  - профиль должен быть пригоден для последующей ручной оценки и аутрича;
  - верификация допускается смешанная: verified where possible, signal-based where not possible.
- Источники MVP допустимы:
  - LinkedIn как обязательная ссылка в результате;
  - Google search;
  - официальные реестры;
  - conference speaker pages;
  - personal sites;
  - авторские страницы и медиа-профили;
  - платные API допустимы как future option, но не обязательны в MVP.
- Формат результата по умолчанию:
  - `CSV`
- Дополнительные представления:
  - HTML viewer поверх результата допустим, но не обязателен для MVP.
- Объём результата:
  - все найденные кандидаты;
  - отдельно shortlist top-20.
- Scoring:
  - MVP должен быть rule-based и explainable;
  - должен быть `why_selected`.

### Unresolved Decisions

- Точное определение `UK+` и набора англоязычных рынков после US.
- Какая минимальная доля verified-сигналов обязательна для top-20.
- Нужен ли в MVP отдельный import layer для exam/registry pages или достаточно signal fields с местом под расширение.
- Точный путь skill внутри репозитория, если в нём уже есть принятый layout Claude Code skills.

## Message Templates

### Codex -> Claude

```text
CONTEXT
- Goal: ...
- Current iteration: ...
- Constraints: ...

TASK
- Build/modify: ...
- Do not do: ...
- Return format: DELIVERABLE_UPDATE or QUESTIONS_FOR_CODEX

ACCEPTANCE CRITERIA
- ...
- ...
- ...
```

### Claude -> Codex

```text
DELIVERABLE_UPDATE
- Summary: ...
- Files changed: ...
- Run command: ...
- Output shape: ...
- Remaining gaps: ...
```

или

```text
QUESTIONS_FOR_CODEX
1. ...
Why blocked: ...

2. ...
Why blocked: ...
```

## Immediate Next Step

Claude должен реализовать MVP skill, который:
- принимает критерии и ниши из этого протокола;
- ищет кандидатов по допустимым источникам;
- нормализует данные в каноническую схему;
- сохраняет полный результат;
- строит shortlist top-20;
- экспортирует результат в CSV;
- не занимается outreach.
