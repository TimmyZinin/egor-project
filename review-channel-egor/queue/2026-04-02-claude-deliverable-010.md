# DELIVERABLE_UPDATE — EGOR-GPTZERO-RESEARCH-010

**From:** claude
**Date:** 2026-04-02
**Status:** COMPLETE — waiting for review

---

## Deliverables Produced

2 documents in `egor-project/docs/`:

1. **`gptzero-checker-research.md`** — full GPTZero research: API, pricing, accuracy, output format, comparison table vs ZeroGPT vs Ahrefs
2. **`gptzero-integration-decision.md`** — verdict: GPTZero SUITABLE as upgrade path, not starter tool

---

## GPTZero: ключевые факты

### Подтверждённо:
- **API:** REST, base `api.gptzero.me`, auth `x-api-key`, Stoplight docs
- **Endpoints:** `/v2/predict/text`, `/v2/predict/files`, + Relevant Sources API (fact-check)
- **Output:** 3-class classification (HUMAN_ONLY/MIXED/AI_ONLY) + confidence (high/medium/low) + sentence-level scores
- **Rate limit:** 30,000 req/hour (documented)
- **Pricing API:** $45/mo (300K words), $135/mo (1M), $250/mo (2M). Overage $0.15/1K words
- **Cost/article (4500 words):** ~$0.675 (vs ZeroGPT $0.15)
- **Batch:** 50 files/request, max 15 MB
- **SOC 2 compliant**
- **Unique: Relevant Sources API** — extracts claims, finds supporting/contradicting sources

### Accuracy:
- Chicago Booth 2026: 99.3% recall at 0.1% FPR (credible academic study)
- Real-world: 5-15% FPR (independent tests, MPG ONE: 12.5%)
- Better academic validation than ZeroGPT (which has zero peer-reviewed benchmarks)

---

## Recommendation: UPGRADE PATH, not starter

| Phase | Tool | Why |
|-------|------|-----|
| Start (0-20 articles) | **ZeroGPT** | Pay-as-you-go, $0.15/article, sufficient for calibration |
| Scale (20+ articles) | **GPTZero** | 3-class confidence, Relevant Sources API, better accuracy |
| Post-publish | **Ahrefs** | Irreplaceable for SEO + site audit AI levels |

### Triggers for GPTZero upgrade:
- ≥20 articles/month
- ZeroGPT false positive rate >20%
- Need external fact-checking (Relevant Sources API)

### GPTZero vs ZeroGPT head-to-head:
- GPTZero: better accuracy, 3-class output, fact-check, SOC 2, documented rate limits. **4.5x more expensive.**
- ZeroGPT: pay-as-you-go, cheaper, adequate for start. Weaker docs, no academic validation.
- Use ONE, not both simultaneously.

---

## Open Questions

1. Relevant Sources API pricing — included in plan or separate? [UNVERIFIED]
2. Python SDK (PyPI `gptzero` v0.1.2) — possibly outdated, verify at integration time
3. Finance-specific accuracy — no AI detector tested on financial content specifically

---

Claude is waiting for the next `go`.
