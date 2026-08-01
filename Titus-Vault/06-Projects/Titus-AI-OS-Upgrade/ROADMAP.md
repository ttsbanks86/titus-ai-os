# Titus AI OS — Roadmap

**Updated:** 2026-07-31
**Source of truth for milestone sequence.** Companion to `PROJECT_STATUS.md` (state) and `CURRENT_MILESTONE.md` (active milestone).

---

## Delivered Milestones

| # | Milestone | Status | Tag / Merge | Report |
|---|-----------|--------|-------------|--------|
| M1 | Research & Design | ✅ Complete | — | `FINAL_REPORT.md` |
| M2 | Knowledge & Context Engine | ✅ Complete | `titus-ai-os-m2-complete` → `3f2ba4c` | `M2_COMPLETION_REPORT.md` |
| M3 | Orchestration, Keyword Search & Branded Interface | ✅ Complete | `titus-ai-os-m3-complete` → `1394aa77` (PR #2) | `M3_COMPLETION_REPORT.md` |
| M4 | Hybrid OpenCode Integration and Unified Startup | ✅ Complete | `titus-ai-os-m4-complete` → `ec2971a` (PR #4) | `M4_COMPLETION_REPORT.md` |
| M5 | Autonomous Execution Engine | 🔄 In progress | — | `M5_COMPLETION_REPORT.md` |

## M4 (complete) — Hybrid OpenCode Integration and Unified Startup

**Goal:** Launching OpenCode auto-launches Titus AI OS — one command starts dashboard, knowledge engine, branded theme, resume context.

**Closure:** PR #4 → `ec2971a` (merge of `docs/m4-completion-records` @ `f6a78e7e`); CI run `30680866091` green; tag `titus-ai-os-m4-complete` → `ec2971a`. Post-closure records PR #5 → `868cdaef`.

| Phase | Scope | Status |
|-------|-------|--------|
| A | Architecture inspection | ✅ |
| B | Customization strategy | ✅ |
| C | Startup sequence design | ✅ |
| D | Live connections design | ✅ |
| E | Branding audit (reuse) | ✅ |
| F | Plugin/MCP audit | ✅ |
| G | Startup workflow implementation | ✅ |
| H | Project resume | ✅ |
| I | Testing | ✅ |
| J | Documentation | ✅ |

**Deliverables (M4):** `themes/titus.json`, `tui.json`, `plugins/titus-m4-startup.ts`, `commands/titus-status.md`, `bin/Start-TitusAIOS.ps1`, dashboard live-connection patch, `CURRENT_MILESTONE.md`.

## M5 (in progress) — Autonomous Execution Engine

**Goal:** A single milestone prompt drives plan → execute sprints → verify → checkpoint → approve-gate → one final verified report. Runner stops only at governance gates (destructive ops, architecture decisions, owner approvals, failed verification, security, safety limits).

| Phase | Scope | Status |
|-------|-------|--------|
| A | Workflow analysis | ✅ `M5_WORKFLOW_ANALYSIS.md` |
| B | Engine composition | ✅ `engine.py` |
| C | Checkpoint system | ✅ `checkpoint.py` |
| D | Execution queue | ✅ `queue.py` |
| E | Approval model | ✅ `approval.py` |
| F | Event system | ✅ `events.py` |
| G | Automation connectors | ✅ `connectors.py` |
| H | Long-run safety | ✅ `safety.py` |
| I | OpenCode + dashboard integration | ✅ `routes/engine.py` + `plugins/titus-m5-engine.ts` |
| J | Project memory | ✅ `memory.py` |
| K | Testing | ✅ 35 new tests; 70/70 combined |
| L | Documentation + records + commit | 🔄 IN PROGRESS |

**Deliverables (M5):** 8 engine modules under `api/orchestration/`, `api/routes/engine.py` (`/api/engine/*`), `~/.config/opencode/plugins/titus-m5-engine.ts`, engine state dir `~/.config/opencode/engine-state/`, 9 M5 docs, `test_m5_autonomous.py`.

## Later (backlog)

- Intelligence layer enhancements (vector embeddings, hybrid search) — noted in earlier plans
- Auto-indexing, n8n automation (previously listed under "M4" scope in M3-era notes; re-baselined)
- Auto-commit hook + guardrails CRITICAL routing into the engine (post-M5 refinements)
- OpenCode SDK live-activity panels in dashboard (session, vcs events via SSE) — deferred from M4 by design
- Web UI (opencode web) branded surface
- Electron desktop wrapper (rejected for M3 MVP, still an option later)
- Multi-workspace support (experimental_workspace adapters)

## Change History

- 2026-07-31: M5 started — phases A–K complete; phase L in progress (docs + records).
- 2026-08-01: M4 closed — PR #4 merged (`ec2971a`), tagged `titus-ai-os-m4-complete`; phase J complete; post-closure records PR #5 → `868cdaef`.
- 2026-07-31: Created. Replaces informal "Next Up" notes in PROJECT_STATUS.md with an explicit milestone sequence; re-baselined M4 scope to Hybrid OpenCode Integration and Unified Startup.
