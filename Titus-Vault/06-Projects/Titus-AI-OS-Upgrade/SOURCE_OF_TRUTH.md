# SOURCE_OF_TRUTH

**Updated:** 2026-08-01
**Purpose:** Definitive record of where authoritative state lives for the Titus AI OS. No duplicated state. When a reader needs "what is true right now," this file is the index.

---

## 1. Milestone / Project State

| Question | Source of truth | Path |
|----------|-----------------|------|
| Which milestone is active? | `CURRENT_MILESTONE.md` | `Titus-Vault\06-Projects\Titus-AI-OS-Upgrade\CURRENT_MILESTONE.md` |
| Full milestone status summary (tests, branch, tags) | `PROJECT_STATUS.md` | `Titus-Vault\06-Projects\Titus-AI-OS-Upgrade\PROJECT_STATUS.md` |
| Milestone sequence | `ROADMAP.md` | `Titus-Vault\06-Projects\Titus-AI-OS-Upgrade\ROADMAP.md` |
| This index | `SOURCE_OF_TRUTH.md` | `Titus-Vault\06-Projects\Titus-AI-OS-Upgrade\SOURCE_OF_TRUTH.md` |
| Release tags | Git tags `titus-ai-os-*-complete` | `main` branch; m4 tag `titus-ai-os-m4-complete` → `ec2971a` (PR #4) |

## 2. Knowledge / Vault

| Question | Source of truth | Path |
|----------|-----------------|------|
| Vault entry points (dashboard, rules, goals) | `Home.md`, `My-Rules.md`, `My-Goals.md` | `Titus-Vault\01-Dashboard\` |
| Daily activity | Daily notes | `Titus-Vault\02-Daily-Notes\YYYY-MM-DD.md` |
| Project master notes | Per-project docs | `Titus-Vault\06-Projects\<project>\` |
| Repeatable processes | `SOPs-Index.md` | `Titus-Vault\07-SOPs\` |
| Agent definitions | Agent files | `Titus-Vault\08-Agents\` + `~/.config/opencode/agent\` |

## 3. OpenCode Integration (M4)

| Question | Source of truth | Path |
|----------|-----------------|------|
| OpenCode config | `opencode.json` | `~/.config/opencode\opencode.json` |
| TUI config (theme selection) | `tui.json` | `~/.config/opencode\tui.json` |
| Brand theme | `titus.json` | `~/.config/opencode\themes\titus.json` |
| Titus plugins | `titus-*.ts` | `~/.config/opencode\plugins\` |
| Custom commands | `commands\*.md` | `~/.config/opencode\commands\` |
| Unified startup | `Start-TitusAIOS.ps1` | `Live Cowork\bin\Start-TitusAIOS.ps1` |
| Brand tokens (web surfaces) | `tokens.css` | `Live Cowork\BRAND\tokens.css` |

## 4. Dashboard

| Question | Source of truth | Path |
|----------|-----------------|------|
| Dashboard API | FastAPI app + routes | `Titus-Vault\titus-ai-os-dashboard\api\` |
| Dashboard frontend | static app | `Titus-Vault\titus-ai-os-dashboard\frontend\` |
| Dashboard start | `start.ps1` (legacy) / `Start-TitusAIOS.ps1` (M4) | dashboard dir / `Live Cowork\bin\` |

## 5. Ownership Rules (enforced)

1. **CEO agent writes** milestone/project records and daily notes. OpenCode tools never write them; the plugin only reads.
2. **Dashboard reads only.** No dashboard route writes vault state.
3. **No duplication.** `CURRENT_MILESTONE.md` is the only "active milestone" record; `PROJECT_STATUS.md` is the only full status summary; `ROADMAP.md` is the only sequence. Update these, not copies.
4. **Archive, never delete.** Stale records move to `Titus-Vault\10-Archive\`.

## 6. Reader Guidance

- Agent at session start: read `CURRENT_MILESTONE.md` + `PROJECT_STATUS.md` + today's daily note (via `titus_resume` tool or directly).
- Dashboard `/api/workspace` and `/api/milestones`: read vault records (patched in M4 to stop hardcoding).
- Any new feature that needs state: declare its source of truth here before building. Do not create parallel records.
