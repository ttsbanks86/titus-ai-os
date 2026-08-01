# M4 Live Connections Design

**Date:** 2026-07-31
**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Status:** DESIGNED (implementation in Phase G/H)

---

## 1. Architecture Principle: Vault Is the Source of Truth

Both the dashboard and OpenCode **read** Titus-Vault records. Neither depends on the other's runtime state. This keeps the system decoupled and upgrade-safe.

```
                 ┌────────────────────────────┐
                 │   Titus-Vault (markdown)   │  ← source of truth
                 │  PROJECT_STATUS.md         │
                 │  CURRENT_MILESTONE.md      │
                 │  06-Projects/*/            │
                 │  02-Daily-Notes/           │
                 └─────────────┬──────────────┘
                  reads ▲       │ writes (daily notes)
                        │       │
          ┌─────────────┴────┐  │  ┌─────────────────────────────┐
          │ Dashboard (8000) │  │  │ OpenCode + Titus plugin     │
          │ FastAPI routes   │  │  │ - /titus status (tools)     │
          │ :3000 frontend   │  └──│ - resume context on start   │
          └──────────────────┘     └─────────────────────────────┘
```

## 2. Connections (each is a read from the vault)

### 2.1 Dashboard → Vault
| Route | Reads | Current issue | M4 fix (Phase G) |
|-------|-------|---------------|------------------|
| `/api/health` | static | none | keep |
| `/api/workspace` | **hardcoded** M3 values | Stale: says milestone M3 @45%, tests 131 | Read `PROJECT_STATUS.md` + `CURRENT_MILESTONE.md`; derive milestone/test/status dynamically |
| `/api/projects` | `06-Projects/*/README.md` | works | keep; add PROJECT_STATUS-driven status |
| `/api/milestones` | `M*_COMPLETION_REPORT.md` glob + **hardcoded M3 append** | Conflict: M3 appears twice (complete via glob, in_progress via hardcode) | Remove hardcoded append; read `CURRENT_MILESTONE.md` for current; parse completion files for status |
| `/api/agents` | agent definitions | works | keep |
| `/api/knowledge` | knowledge index | works | keep |
| `/api/verification` | verification records | works | keep |

### 2.2 OpenCode Plugin → Vault (Phase H)
| Data | Reads | Use |
|------|-------|-----|
| Active milestone | `CURRENT_MILESTONE.md` | Inject into session at start |
| Project status | `PROJECT_STATUS.md` | `/titus status` command output |
| Today's tasks | `02-Daily-Notes\YYYY-MM-DD.md` | Resume: "today's tasks" block |
| Project master notes | `06-Projects\*\` | Context when working in a project |

### 2.3 OpenCode → Dashboard (optional, additive)
- OpenCode exposes **SDK events** (session.*, vcs.branch.updated, todo.updated) via SSE.
- The dashboard MAY consume these later for live activity panels — but **not required** for M4. Dashboard reads vault; OpenCode writes vault. No duplicate state.
- Deferred to post-M4 (documented in M4_UPDATE_COMPATIBILITY.md as future enhancement).

## 3. State Model

| State | Owner | Where |
|-------|-------|-------|
| Milestone status | Vault (`CURRENT_MILESTONE.md`) | Written by CEO agent at milestone boundaries |
| Project status | Vault (`PROJECT_STATUS.md`) | Written by CEO agent |
| Daily tasks | Vault (`02-Daily-Notes\`) | Written by CEO agent end-of-session |
| Session activity | OpenCode (runtime) | Not persisted; surfaced via `/titus status` |
| Approval decisions | Vault (daily notes / project notes) | Written by CEO agent |

**Rule:** Never two writers for the same state. OpenCode never writes milestone/project records; the CEO agent (running inside OpenCode) writes them. Dashboard never writes; it reads.

## 4. Live Refresh Behavior

- Dashboard frontend polls `/api/*` every 30 s (client-side; no change to API model needed).
- `/titus status` in OpenCode reads fresh from vault each invocation (no caching).
- Knowledge index refresh is on-demand (M2 engine) — unchanged.

## 5. Health Signals (Phase G additions)

| Signal | Source | Check |
|--------|--------|-------|
| Dashboard API up | `http://localhost:8000/api/health` | Launcher poll |
| Frontend up | `http://localhost:3000` | Launcher poll |
| Knowledge index present | `knowledge_index.json` | Launcher + `/titus health` |
| Vault records present | `PROJECT_STATUS.md`, `CURRENT_MILESTONE.md` | `/titus status` |
| OpenCode plugins loaded | opencode log | Phase I check |

## 6. Acceptance Criteria

1. `/api/workspace` reflects M4 as current milestone, M3 as complete, tests 166 — no hardcoded stale values.
2. `/api/milestones` has no duplicate M3 entry.
3. `/titus status` in an OpenCode session returns milestone + project + tests from vault records.
4. Resume context (milestone, project, today's tasks) is injected at session start.
5. All reads fail soft: missing record → clear message, no crash.
