# Проект Егора — Документация (Source of Truth)

> Обновлено: 3 апреля 2026

Система инструментов для финансового контент-проекта: поиск экспертов, генерация broker reviews, проверка качества текстов.

**Wiki:** [github.com/TimmyZinin/egor-project/wiki](https://github.com/TimmyZinin/egor-project/wiki) (12 страниц с Mermaid-диаграммами)

---

## Структура

```
docs/
├── README.md                      ← Этот файл (индекс)
│
├── expert-hunter/                 ← /expert-hunter — поиск экспертов
│   ├── spec.md                    Source of Truth: спецификация скилла
│   ├── egor-instructions.md       Инструкции для Егора
│   └── citability-backlog.md      Бэклог citability enrichment
│
├── broker-content/                ← /broker-writer + /broker-checker
│   ├── broker-writer-spec-v2.md   Source of Truth: генерация reviews
│   ├── broker-checker-spec.md     Source of Truth: quality gate
│   ├── integration.md             Как writer + checker + Ahrefs работают вместе
│   ├── content-pipeline-spec.md   Полная спецификация контент-пайплайна
│   └── source-of-truth-decision.md  Решение: где живёт контент-система
│
├── ai-detection/                  ← Исследование AI-детекторов
│   ├── zerogpt-research.md        ZeroGPT: API, pricing, accuracy
│   ├── zerogpt-decision.md        Решение: ZeroGPT отклонён
│   ├── gptzero-research.md        GPTZero: API, pricing, accuracy
│   ├── gptzero-decision.md        Решение: GPTZero — основной AI-детектор (согласовано)
│   ├── grammarly-research.md      Grammarly: API (Enterprise only), RAID #1
│   ├── trustpilot-benchmark.md    Trustpilot рейтинги трёх сервисов
│   └── ahrefs-verification-plan.md  Ahrefs AI detection capabilities
│
└── research/                      ← SEO и конкурентный research
    ├── broker-review-seo-research.md  SEO-анализ broker reviews
    └── content-skill-plan.md      Первоначальный план скилла
```

## Source of Truth по компонентам

| Компонент | Source of Truth | Статус |
|-----------|----------------|--------|
| `/expert-hunter` | `docs/expert-hunter/spec.md` + `expert-hunter/SKILL.md` | Работает (MVP) |
| `/broker-writer` | `docs/broker-content/broker-writer-spec-v2.md` (спека) + `broker-writer/SKILL.md` (скилл) | Скилл создан, установлен, первый draft IG готов |
| `/broker-checker-gptzero` | `docs/broker-content/broker-checker-spec.md` (базовая спека) + GPTZero интеграция | **В разработке** — спека базового checker готова, GPTZero API ключ получен, скилл не создан |
| AI Detection pipeline | `docs/ai-detection/` (7 документов) | Исследование завершено, GPTZero выбран |
| Архитектура интеграции | `docs/broker-content/integration.md` | Спека готова |

## Live страницы (GitHub Pages)

- [Исследование + экспертная панель](https://timzinin.com/egor-project/research.html)
- [Content Generation Research](https://timzinin.com/egor-project/content-gen-research.html)
- [AI Detection Benchmark](https://timzinin.com/egor-project/ai-detection-benchmark.html)

## Для Егора

Если ты Егор и хочешь использовать expert-hunter:
1. Читай `docs/expert-hunter/egor-instructions.md`
2. Рабочий код в `expert-hunter/` (hunt.py, SKILL.md)

## Для следующей Claude-сессии

1. Начни с этого README
2. Wiki: [github.com/TimmyZinin/egor-project/wiki](https://github.com/TimmyZinin/egor-project/wiki) — обзор всего проекта
3. Спеки writer/checker → `docs/broker-content/`
4. AI detection research → `docs/ai-detection/`
5. Текущий план → `~/.claude/plans/shiny-imagining-harbor.md` (4 спринта: Wiki → Source of Truth → Скилл → Тест)
6. GPTZero API ключ → env var `GPTZERO_API_KEY` (ключ Егора, лимит 300K слов/мес, экономить)

## Collaborative Data

Данные брокеров можно подготовить в приватном Google Sheet (shared Tim + Egor).

Sheet помогает заполнить поля для `brokers/{slug}/input.json`.
При запуске `/broker-writer {slug}`:
- Если `input.json` уже существует → используется напрямую
- Если нет → данные вводятся в диалог скилла (можно читать из Sheet)

Sheet **не заменяет** `content/{slug}/brief.md` — бриф создаётся отдельно
(в диалоге скилла или вручную).

Структура Sheet tab "BrokerData": колонки соответствуют полям `input.json`
(см. docs/broker-content/broker-writer-spec-v2.md → "Формат input.json").

Sheet URL НЕ хранится в репозитории. Передаётся участникам приватно.
