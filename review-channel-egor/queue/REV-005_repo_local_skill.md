---
id: REV-005
task: TASK-001 (NEEDS_CHANGES from REV-004)
type: result
submitted_at: 2026-03-30 19:02 MSK
status: pending_review
executor_claims:
  - "SKILL.md exists at egor-project/expert-hunter/SKILL.md (repo-local source of truth)"
  - "install.sh exists at egor-project/expert-hunter/install.sh (copies SKILL.md to ~/.claude/skills/)"
  - "install.sh is executable (chmod +x)"
  - "Running install.sh produces: Installed: ~/.claude/skills/expert-hunter.md"
  - "diff between repo SKILL.md and installed skill = IDENTICAL"
  - "Repo file tree: SKILL.md, install.sh, schema.py, build_candidates.py, scan.py, scan_results_20260330.json"
  - "Full end-to-end path from repo: install.sh -> /expert-hunter -> build_candidates.py --seed -> CSV"
---

## Context

CURRENT_VERDICT NEEDS_CHANGES on REV-004: skill only in ~/.claude/skills/, not in repo.

## What was done

1. **`SKILL.md`** — copied skill definition into repo at `egor-project/expert-hunter/SKILL.md` (source of truth)
2. **`install.sh`** — install script that copies SKILL.md to `~/.claude/skills/expert-hunter.md`
3. Verified: `diff SKILL.md ~/.claude/skills/expert-hunter.md` = IDENTICAL

## Repo file tree

```
egor-project/expert-hunter/
  SKILL.md                    # Skill definition (source of truth)
  install.sh                  # Install to ~/.claude/skills/
  schema.py                   # ExpertCandidate, scoring, CSV/JSON export
  build_candidates.py         # Build pipeline (--from-scan | --seed)
  scan.py                     # WebSearch query definitions + parser
  scan_results_20260330.json  # Saved scan artifact (20 candidates)
```

## Reproducible end-to-end path

```bash
cd ~/egor-project/expert-hunter

# 1. Install skill
./install.sh
# Output: Installed: ~/.claude/skills/expert-hunter.md

# 2. Run seed mode
python3 build_candidates.py --seed
# Output: candidates_full.seed.csv + candidates_shortlist.seed.csv

# 3. Or scan-backed mode
python3 build_candidates.py --from-scan scan_results_20260330.json
# Output: candidates_full.scan.csv + candidates_shortlist.scan.csv
```

## Evidence

```bash
# Repo-local skill exists
ls -la ~/egor-project/expert-hunter/SKILL.md
# Expected: exists, ~94 lines

# Install script works
~/egor-project/expert-hunter/install.sh
# Expected: "Installed: ..."

# Files identical
diff ~/egor-project/expert-hunter/SKILL.md ~/.claude/skills/expert-hunter.md
# Expected: no output (identical)

# End-to-end run
cd ~/egor-project/expert-hunter && python3 build_candidates.py --seed 2>&1 | head -1
# Expected: [MODE] seeded demo
```

## What was NOT changed

- schema.py, build_candidates.py, scan.py — unchanged
- scan_results_20260330.json — unchanged
- ~/.claude/skills/expert-hunter.md — now installed FROM repo, not independent

## Files for review

- `/Users/timofeyzinin/egor-project/expert-hunter/SKILL.md` (new, source of truth)
- `/Users/timofeyzinin/egor-project/expert-hunter/install.sh` (new)
