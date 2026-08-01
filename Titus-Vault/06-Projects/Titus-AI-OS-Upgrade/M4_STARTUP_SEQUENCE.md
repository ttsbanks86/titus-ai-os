# M4 Startup Integration Sequence

**Date:** 2026-07-31
**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Status:** DESIGNED (implementation in Phase G)

---

## 1. Goal

One command starts the entire Titus AI OS:

```
Start-TitusAIOS
```

Launching OpenCode auto-launches the Titus AI OS working environment: dashboard up, knowledge engine indexed, session resumed with current milestone, active project, and today's tasks. Everything is idempotent, failure-tolerant, and upgrade-proof.

## 2. Design Constraints (from M3 decision + M4 strategy)

1. **No fork.** OpenCode remains stock. (M3 decision: standalone dashboard; M4 adds only safe extensions.)
2. **Source of truth stays the vault.** Both the dashboard and OpenCode read Titus-Vault records. They do not depend on each other's runtime state.
3. **Graceful degradation.** If the dashboard fails to start, OpenCode still launches. If OpenCode fails, dashboard still runs.
4. **Idempotent.** Re-running the launcher never starts duplicate servers.
5. **Wrapper over fork.** All sequencing lives in a PowerShell launcher + a plugin; nothing inside the OpenCode binary.

## 3. Sequence (Phase G implementation)

### Stage 0 — Pre-flight
1. Verify `python` available (dashboard requirement).
2. Verify `opencode` available on PATH (npm global install).
3. Verify Titus-Vault path exists.
4. Record start timestamp for the log.

### Stage 1 — Knowledge Engine Health
1. Check `Titus-Vault\knowledge_engine\` present.
2. Check knowledge index (`knowledge_index.json`) present; if missing, note it (rebuilt on demand by the engine — no blocking).

### Stage 2 — Dashboard (idempotent)
1. Check if port 8000 is already listening → skip API start if yes.
2. Check if port 3000 is already listening → skip frontend start if yes.
3. Start missing components (uvicorn :8000 from `api\`, http.server :3000 from `frontend\`), minimized windows, logs to `Titus-Vault\titus-ai-os-dashboard\logs\`.
4. Health-check: poll `http://localhost:8000/docs` (or `/` root) up to ~10 s.

### Stage 3 — Resume Context (prepares OpenCode launch)
1. Read `PROJECT_STATUS.md` → current milestone + status.
2. Read `CURRENT_MILESTONE.md` (created in Phase J) → active milestone name + phase.
3. Read today's daily note `02-Daily-Notes\2026-07-31.md` (or latest if missing).
4. Bundle a one-block context summary into an env var or a temp context file consumed by the plugin at session start.

### Stage 4 — Launch OpenCode
1. Launch `opencode` with `cwd = C:\Users\tbank\Desktop\Live Cowork` (workspace root with `.opencode\` project config).
2. OpenCode loads global config + project config + plugins (existing 2 + M4 plugin).
3. Plugin `event` hook on `session.created` runs the resume sequence (Phase H) — injects milestone/active-project/today-task context into the session.
4. Plugin exposes `/titus status` command and tools (`titus_status`, `titus_resume`, `titus_health`).

### Stage 5 — Verify (Phase I)
1. Dashboard reachable (API :8000, frontend :3000).
2. OpenCode loaded without plugin errors (log check).
3. Resume context present in the session (test `/titus status`).
4. Startup time recorded (target: < 5 s overhead vs. bare OpenCode ~570 ms).

## 4. Files (created in Phase G)

| File | Location | Role |
|------|----------|------|
| `Start-TitusAIOS.ps1` | `C:\Users\tbank\Desktop\Live Cowork\` (or `bin\`) | Launcher (Stages 0–4) |
| `titus-m4-startup.ts` | `C:\Users\tbank\.config\opencode\plugins\` | Plugin: resume, tools, status |
| `titus-theme.json` (as `titus.json`) | `C:\Users\tbank\.config\opencode\themes\` | Brand theme |
| `tui.json` | `C:\Users\tbank\.config\opencode\` | Theme selection + plugin_enabled |
| `CURRENT_MILESTONE.md` | `Titus-Vault\06-Projects\Titus-AI-OS-Upgrade\` (mirrored concept in vault root) | Resume source |

## 5. Logging & Failure Modes

| Failure | Behavior |
|---------|----------|
| Python missing | Launcher warns, skips dashboard, still launches OpenCode |
| Port 8000 in use by non-dashboard | Launcher warns, assumes existing service, continues |
| Knowledge index missing | Note in log; engine rebuilds on demand; not blocking |
| Plugin error at load | OpenCode logs plugin failure, continues with remaining plugins |
| Resume context missing files | Plugin falls back to generic session (no crash) |
| OpenCode launch fails | Launcher reports, dashboard remains up |

## 6. Update Compatibility

- Launcher: standalone script, unaffected by OpenCode upgrades.
- Plugin: pinned against `@opencode-ai/plugin` 1.15.4; if hooks change on upgrade, plugin is isolated in config dir and can be updated independently.
- Theme/config: JSON files, format stable; re-mapped in minutes if token names change.

## 7. Acceptance Criteria

1. One command starts dashboard + OpenCode.
2. Re-running never duplicates servers.
3. OpenCode session auto-contains current milestone, active project, today's tasks.
4. Dashboard live with projects/milestones/agents/knowledge/verification routes.
5. No modification to OpenCode binary or npm internals.
6. `opencode upgrade` leaves all customization intact.
