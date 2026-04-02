---
id: REV-009
task: EGOR-PROD-QA-004
type: result
submitted_at: 2026-03-30 19:55 MSK
status: pending_review
executor_claims:
  - "hunt.py exists as production entrypoint, no hardcoded candidates, parameter-driven"
  - "5 test fixtures in fixtures/ from real WebSearch (forex_us, stocks_us, crypto_us, personal_finance_us, forex_uk)"
  - "5 test scenarios passed: 30 unique candidates total"
  - "Skill packaging fixed: ~/.claude/skills/expert-hunter/SKILL.md (directory layout)"
  - "Old single-file expert-hunter.md removed"
  - "install.sh updated to create directory layout and remove old file"
  - "Skill visible in Claude Code skill list as 'expert-hunter'"
  - "build_candidates.py --seed is legacy, hunt.py is primary"
  - "CSV outputs per niche+geo: candidates_forex_us.csv, candidates_stocks_us.csv, etc."
---

## Context

EGOR-PROD-QA-004: production path + packaging fix (codex-to-claude-010 + codex-to-claude-011).

## What was done

### 1. Production entrypoint: hunt.py

New file, 240 lines. Zero hardcoded candidates.

Parameters:
- `--niche forex|stocks|crypto|personal_finance`
- `--geo US|UK|CA|AU`
- `--all-niches`
- `--test-fixture <path>` (for reproducible tests with saved search results)
- `--output-dir <path>`

Production mode: prints parameterized queries for live WebSearch.
Test mode: loads from fixture JSON.

### 2. Five test scenarios (all passed)

| Scenario | Fixture | Candidates | Score range | High conf |
|----------|---------|-----------|-------------|-----------|
| forex / US | fixtures/forex_us.json | 9 | 47-85 | 8 |
| stocks / US | fixtures/stocks_us.json | 6 | 49-85 | 5 |
| crypto / US | fixtures/crypto_us.json | 6 | 76-85 | 6 |
| personal_finance / US | fixtures/personal_finance_us.json | 4 | 47-81 | 3 |
| forex / UK | fixtures/forex_uk.json | 5 | 76-85 | 5 |

### 3. Packaging fix (codex-to-claude-011)

Before: `~/.claude/skills/expert-hunter.md` (single file, NOT discoverable)
After: `~/.claude/skills/expert-hunter/SKILL.md` (directory layout, discoverable)

Evidence: skill appears in Claude Code skill list as:
```
expert-hunter: /expert-hunter — Find and rank finance experts
```

install.sh updated:
- Creates `~/.claude/skills/expert-hunter/` directory
- Removes old single-file layout if exists
- Copies SKILL.md into directory

### 4. Mode separation

| File | Role | Primary? |
|------|------|---------|
| hunt.py | Production entrypoint | YES |
| build_candidates.py --seed | Legacy demo | NO (kept for calibration only) |
| build_candidates.py --from-scan | Legacy scan | NO (superseded by hunt.py) |

## Evidence

```bash
cd /Users/timofeyzinin/egor-project/expert-hunter

# hunt.py has zero hardcoded candidates
grep -c "RAW\s*=" hunt.py
# Expected: 0

# Skill is directory-based
ls -la ~/.claude/skills/expert-hunter/SKILL.md
# Expected: file exists

# Old single-file removed
ls ~/.claude/skills/expert-hunter.md 2>&1
# Expected: No such file

# 5 fixtures exist
ls fixtures/*.json | wc -l
# Expected: 5

# Test runs
python3 hunt.py --niche forex --geo US --test-fixture fixtures/forex_us.json 2>&1 | grep "EXPORT"
# Expected: 9 candidates
python3 hunt.py --niche stocks --geo US --test-fixture fixtures/stocks_us.json 2>&1 | grep "EXPORT"
# Expected: 6 candidates
python3 hunt.py --niche crypto --geo US --test-fixture fixtures/crypto_us.json 2>&1 | grep "EXPORT"
# Expected: 6 candidates
python3 hunt.py --niche personal_finance --geo US --test-fixture fixtures/personal_finance_us.json 2>&1 | grep "EXPORT"
# Expected: 4 candidates
python3 hunt.py --niche forex --geo UK --test-fixture fixtures/forex_uk.json 2>&1 | grep "EXPORT"
# Expected: 5 candidates

# install.sh creates directory layout
cat install.sh | grep "mkdir -p"
# Expected: mkdir -p "$TARGET_DIR"
```

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/hunt.py` (production entrypoint)
- `/Users/timofeyzinin/egor-project/expert-hunter/install.sh` (updated for directory layout)
- `/Users/timofeyzinin/egor-project/expert-hunter/fixtures/` (5 test fixtures)
- `~/.claude/skills/expert-hunter/SKILL.md` (installed, discoverable)
