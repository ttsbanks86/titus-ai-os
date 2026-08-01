# SOURCE_OF_TRUTH

**Updated:** 2026-07-31
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

## 5. M5 Engine Runtime State

Engine runtime state is NOT vault state and NOT repo state. It lives in a
shared state dir outside the repo so the dashboard and the OpenCode plugin
always read the same files.

| Question | Source of truth | Path |
|----------|-----------------|------|
| Engine queue (what to do next) | `queue.json` | `~/.config/opencode\engine-state\queue.json` |
| Pending / decided approvals | `approvals.json` | `~/.config/opencode\engine-state\approvals.json` |
| Event trail (JSONL) | `events.log` | `~/.config/opencode\engine-state\events.log` |
| Latest checkpoint pointer | `latest.json` | `~/.config/opencode\engine-state\checkpoints\latest.json` |
| Checkpoint snapshots | `checkpoint-*.json` | `~/.config/opencode\engine-state\checkpoints\` |
| Liveness / heartbeat | `heartbeat.json` | `~/.config/opencode\engine-state\heartbeat.json` |
| Resume context bundle | `context.json` | `~/.config/opencode\engine-state\context.json` |
| Engine API (read + owner decisions) | `/api/engine/*` | `http://localhost:8000/api/engine/*` |
| Engine tools (OpenCode) | `titus_engine_status`, `titus_engine_resume`, `titus_engine_approve` | `~/.config/opencode\plugins\titus-m5-engine.ts` |

**Rule:** the engine (in OpenCode) is the ONLY writer of `queue.json`,
`approvals.json`, `events.log`, `heartbeat.json`, and checkpoint files.
The dashboard and plugin only read them — except owner decision endpoints
(`/api/engine/approvals/{id}/decide`, `titus_engine_approve`) which write
approval decisions on explicit owner action.

## 6. Ownership Rules (enforced)

1. **CEO agent writes** milestone/project records and daily notes. OpenCode tools never write them; the plugin only reads.
2. **Dashboard reads only.** No dashboard route writes vault state. Engine decision endpoints write only engine runtime state (section 5), never vault records.
3. **No duplication.** `CURRENT_MILESTONE.md` is the only "active milestone" record; `PROJECT_STATUS.md` is the only full status summary; `ROADMAP.md` is the only sequence. Update these, not copies.
4. **Archive, never delete.** Stale records move to `Titus-Vault\10-Archive\`.

## 7. Reader Guidance

- Agent at session start: read `CURRENT_MILESTONE.md` + `PROJECT_STATUS.md` + today's daily note (via `titus_resume` tool or directly).
- Autonomous engine resume: `titus_engine_resume` → engine state bundle; restore from latest checkpoint when resuming an interrupted run.
- Dashboard `/api/workspace` and `/api/milestones`: read vault records (patched in M4 to stop hardcoding).
- Any new feature that needs state: declare its source of truth here before building. Do not create parallel records.
