---
id: REV-004
task: TASK-001 (NEEDS_CHANGES from REV-003)
type: result
submitted_at: 2026-03-30 18:55 MSK
status: pending_review
executor_claims:
  - "Skill file exists at ~/.claude/skills/expert-hunter.md"
  - "Skill file is 94 lines with trigger phrases, modes, steps, run commands, output schema, constraints"
  - "Trigger phrases: /expert-hunter, найди экспертов, expert search, поиск экспертов"
  - "Three modes documented: scan (full pipeline), verify (single expert), seed (demo)"
  - "Canonical run command: python3 build_candidates.py --from-scan scan_results_YYYYMMDD.json"
  - "Seed run command: python3 build_candidates.py --seed"
  - "Output schema documented: 14 fields matching PROTOCOL.md"
  - "Constraints section: no outreach, no anti-AI, claimed vs verified separate"
  - "Scripts unchanged: schema.py, build_candidates.py, scan.py remain the engine"
---

## Context

CURRENT_VERDICT NEEDS_CHANGES on REV-003: main finding = scripts not packaged as Claude Code skill.

## What was done

Created `/Users/timofeyzinin/.claude/skills/expert-hunter.md` — Claude Code skill file with:

1. **Trigger phrases**: `/expert-hunter`, `найди экспертов`, `expert search`, `поиск экспертов`
2. **Three modes**:
   - `/expert-hunter` or `/expert-hunter scan` — full pipeline
   - `/expert-hunter verify <url>` — single expert
   - `/expert-hunter seed` — demo with built-in data
3. **5-step workflow**: SCAN -> ENRICH -> SCORE -> EXPORT -> REPORT
4. **Canonical run commands** documented
5. **Output schema** (14 fields) documented
6. **Scoring table** (8 categories, max 100) documented
7. **Constraints** (no outreach, claimed vs verified separate)

## What was NOT changed

- `schema.py` — unchanged
- `build_candidates.py` — unchanged
- `scan.py` — unchanged
- Scan results JSON — unchanged
- All CSV/JSON outputs — unchanged

## Evidence

```bash
# Skill file exists
ls -la ~/.claude/skills/expert-hunter.md
# Expected: file exists, ~94 lines

# Line count
wc -l ~/.claude/skills/expert-hunter.md
# Expected: ~94

# Trigger phrases present
grep -c "expert-hunter\|найди экспертов\|expert search" ~/.claude/skills/expert-hunter.md
# Expected: >= 4

# Run commands documented
grep "python3 build_candidates.py" ~/.claude/skills/expert-hunter.md
# Expected: 2 lines (--from-scan and --seed)

# Engine scripts still work
cd ~/egor-project/expert-hunter && python3 build_candidates.py --seed 2>&1 | head -1
# Expected: [MODE] seeded demo: using built-in 20 candidates
```

## Files for review

- `/Users/timofeyzinin/.claude/skills/expert-hunter.md` (new)
