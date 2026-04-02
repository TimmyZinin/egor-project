# Проект Егора — Документация (Source of Truth)

> Обновлено: 2 апреля 2026

Система инструментов для финансового контент-проекта: поиск экспертов, генерация broker reviews, проверка качества текстов.

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
│   ├── broker-writer-spec.md      Source of Truth: генерация reviews
│   ├── broker-checker-spec.md     Source of Truth: quality gate
│   ├── integration.md             Как writer + checker + Ahrefs работают вместе
│   ├── content-pipeline-spec.md   Полная спецификация контент-пайплайна
│   └── source-of-truth-decision.md  Решение: где живёт контент-система
│
├── ai-detection/                  ← Исследование AI-детекторов
│   ├── zerogpt-research.md        ZeroGPT: API, pricing, accuracy
│   ├── zerogpt-decision.md        Решение: ZeroGPT как стартовый detector
│   ├── gptzero-research.md        GPTZero: API, pricing, accuracy
│   ├── gptzero-decision.md        Решение: GPTZero как upgrade path
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
| `/broker-writer` | `docs/broker-content/broker-writer-spec.md` | Спека готова, код не написан |
| `/broker-checker` | `docs/broker-content/broker-checker-spec.md` | Спека готова, код не написан |
| AI Detection pipeline | `docs/ai-detection/` (6 документов) | Исследование завершено |
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
2. Спеки writer/checker → `docs/broker-content/`
3. AI detection research → `docs/ai-detection/`
4. Handoff из предыдущей сессии → `.agent-bridge/workspace11/CLAUDE_SOLO_HANDOFF_FULL_2026-04-02.md`
