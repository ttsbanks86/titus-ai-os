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
| M5 | Autonomous Execution Engine | ✅ Complete | `titus-ai-os-m5-complete` → `c3cfcee4` (PR #6) | `M5_COMPLETION_REPORT.md` |
| M5.5 | Platform Validation, Hardening & Production Readiness | ✅ Complete | `titus-ai-os-m55-complete` | `M5_5_FINAL_REPORT.md` |

## M5.5 (complete) — Platform Validation, Hardening, and Production Readiness

**Goal:** Prove the Titus AI OS is reliable and stable enough to be the primary daily development environment. Automatic startup, resume, long-run execution, multi-project isolation, OpenCode compatibility, benchmarked performance, failure recovery, security, and a documented readiness decision. Repair only verified defects; no new features.

**Decision:** PRODUCTION_READY — all 12 definition-of-done checks verified (`M5_5_PRODUCTION_READINESS.md`).

| Phase | Scope | Status |
|-------|-------|--------|
| A | System audit | ✅ `M5_5_PLATFORM_VALIDATION.md` |
| B | Automatic startup | ✅ launch-string defect repaired (uvicorn `api.main:app`) |
| C | Project resume | ✅ live resume test |
| D | Long-run validation | ✅ 40-sprint run + runtime guard |
| E | Multi-project validation | ✅ isolation verified |
| F | OpenCode compatibility | ✅ OpenCode 1.17.18 + plugin API |
| G | Performance | ✅ `M5_5_PERFORMANCE_REPORT.md` |
| H | Failure recovery | ✅ `M5_5_RECOVERY_TESTS.md` |
| I | Security | ✅ scan clean + gates enforced |
| J | Owner experience | ✅ dashboard + plugin tools |
| K | Readiness decision | ✅ PRODUCTION_READY |
| L | Documentation + records + commit + merge + tag | ✅ COMPLETE |

**Deliverables (M5.5):** 5 docs under `06-Projects/Titus-AI-OS-Upgrade/`, launcher + dashboard script + README repairs.

## M5 (complete) — Autonomous Execution Engine

**Goal:** A single milestone prompt drives plan → execute sprints → verify → checkpoint → approve-gate → one final verified report. Runner stops only at governance gates (destructive ops, architecture decisions, owner approvals, failed verification, security, safety limits).

**Closure:** PR #6 → `c3cfcee4` (merge of `docs/m5-autonomous-engine` @ `8d788e33`); CI test + secret-scan green; tag `titus-ai-os-m5-complete` → `c3cfcee4`.

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
| L | Documentation + records + commit + merge + tag | ✅ COMPLETE |

**Deliverables (M5):** 8 engine modules under `api/orchestration/`, `api/routes/engine.py` (`/api/engine/*`), `~/.config/opencode/plugins/titus-m5-engine.ts`, engine state dir `~/.config/opencode/engine-state/`, 9 M5 docs, `test_m5_autonomous.py`.

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

## Next Up

- M6 (not started — do not begin until M5.5 closure is confirmed):
  - Per-project engine state dirs by default (M5.5 observation #1)
  - Intelligence layer enhancements (vector embeddings, hybrid search)
  - Auto-indexing, n8n automation
  - Auto-commit hook + guardrails CRITICAL routing into the engine
  - OpenCode SDK live-activity panels in dashboard (session, vcs events via SSE)

## Later (backlog)

- Web UI (opencode web) branded surface
- Electron desktop wrapper (rejected for M3 MVP, still an option later)
- Multi-workspace support (experimental_workspace adapters)
- Vault-style milestone records for Titus Video Studio and BA Campus Academy (M5.5 observation #2)

## Change History

- 2026-07-31: M5.5 closed — PRODUCTION_READY, tagged `titus-ai-os-m55-complete`; phase L complete.
- 2026-07-31: M5 closed — PR #6 merged (`c3cfcee4`), tagged `titus-ai-os-m5-complete`; phase L complete.
- 2026-07-31: M5 started — phases A–K complete; phase L in progress (docs + records).
- 2026-08-01: M4 closed — PR #4 merged (`ec2971a`), tagged `titus-ai-os-m4-complete`; phase J complete; post-closure records PR #5 → `868cdaef`.
- 2026-07-31: Created. Replaces informal "Next Up" notes in PROJECT_STATUS.md with an explicit milestone sequence; re-baselined M4 scope to Hybrid OpenCode Integration and Unified Startup.
