# M4 Customization Strategy

**Date:** 2026-07-31
**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Scope:** How Titus AI OS customizes OpenCode, in priority order, with maintenance cost and update compatibility.

---

## 1. Strategy Principles

1. **Extension over modification.** Never modify the OpenCode binary, npm package, or generated files.
2. **Config over code.** Prefer `opencode.json` / `tui.json` / theme JSON / command markdown over writing TypeScript where the built-in mechanism suffices.
3. **Wrapper over fork.** All startup sequencing happens in a thin PowerShell launcher, not inside the OpenCode codebase.
4. **Upgrade-proof.** Every customization lives in `~/.config/opencode/` (persists across `opencode upgrade`). The plugin API version is pinned; breaking changes are watched via `installation.update-available` events.
5. **Fallback-first.** Provider routing, permission rules, and safety net plugins ensure the system works even when premium APIs are down.

## 2. Priority Ladder (always pick the highest that satisfies the requirement)

| Priority | Mechanism | Effort | Maintenance | Update risk | Used for |
|----------|-----------|--------|-------------|-------------|----------|
| 1 | Theme (JSON) | Low | None | None | Branding, UI polish |
| 2 | Config (opencode.json / tui.json) | Low | Low | None | Model routing, MCP, permissions, theme selection |
| 3 | Commands + Agents + Skills (markdown) | Low | Low | None | Slash commands, agent defs, skill docs |
| 4 | Plugin (local TS) | Medium | Medium | Low (API pinned) | Startup hooks, tools, events, slots |
| 5 | Extension (hooks/tools/slots/routes via plugin) | Medium | Medium | Low | Custom tools, TUI additions, live state |
| 6 | Wrapper (PowerShell launcher) | Medium | Medium | None | Startup sequence: dashboard + knowledge + OpenCode |
| 7 | Fork | Very high | Very high | High | Never for M4 scope |

## 3. Decisions by Titus AI OS Feature

### 3.1 Unified Startup (launch OpenCode → Titus AI OS loads)
- **Chosen:** Wrapper (PowerShell `start-titus-ai-os.ps1`) + Plugin startup hooks.
- **Why:** Startup sequencing (start dashboard, verify knowledge index, inject context, launch OpenCode with workspace) is orchestration, not product code. A wrapper keeps it external and re-runnable.
- **Mechanism:**
  - Launcher: `start-titus-ai-os.ps1` → starts dashboard API (uvicorn :8000) if not running → starts knowledge engine health check → launches `opencode` with cwd = Live Cowork (workspace root).
  - Plugin `event` hook on `session.created` / `server.connected` runs the resume sequence (see Phase H) — injects current milestone, active project, today's tasks into the session.
- **Maintenance:** Launcher ~50 lines; plugin ~100 lines. Both versioned in Titus-Vault.
- **Update risk:** None. `opencode upgrade` does not touch either.

### 3.2 Dashboard Integration
- **Chosen:** Keep the existing FastAPI dashboard (`titus-ai-os-dashboard`) as the live-ops panel; OpenCode TUI slot (`sidebar_content`, `home_logo`) shows a lightweight status surface via plugin.
- **Why:** The dashboard already exists from M3 (FastAPI, routes: projects, milestones, agents, knowledge, verification). Rewriting it inside OpenCode would duplicate state and increase risk. OpenCode's job is the working surface; the dashboard's job is the at-a-glance panel.
- **Mechanism:** Dashboard reads Titus-Vault records (source of truth) + OpenCode SDK events where useful (session, vcs). OpenCode plugin exposes `/titus status` and optional `home_logo`/`home_footer` slots with brand mark.
- **Update risk:** Low. Both sides are additive.

### 3.3 Branding
- **Chosen:** Theme (JSON) — Priority 1.
- **Mechanism:** `~/.config/opencode/themes/titus.json` mapping the Titus brand tokens (navy #0F2742, gold #D4A14A, etc.) onto OpenCode theme tokens (primary, background, sidebar, accent, syntax colors). Selected via `tui.json` → `"theme": "titus"`.
- **Fallback:** If theme format changes, the theme file is isolated and re-mapped in minutes. No code impact.

### 3.4 Model Routing & Providers
- **Chosen:** Config — Priority 2 (already done in M3-era opencode.json: DeepSeek primary, small model, env-var keys).
- **Additions in M4:** ensure `small_model` is budget-tier, document fallback chain (OpenCodeGo → Ollama → DeepSeek → GPT-4o-mini → local) in provider config comments / README.

### 3.5 Safety & Permissions
- **Chosen:** Config `permission` section + existing `titus-safety-net` plugin (Priority 2 + 4).
- **Mechanism:** Permission rules for common tools; safety-net plugin remains warn-only. M4 adds startup-time permission sanity check (verify allow/deny/ask lists still valid after upgrade).

### 3.6 Live State & Resume
- **Chosen:** Plugin (Priority 4/5).
- **Mechanism:** Plugin reads Titus-Vault records (CURRENT_MILESTONE.md, project master notes, daily note) at session start; exposes tools (`titus_resume`, `titus_status`) and injects context via `experimental.chat.system.transform` (or instruction file) — decide after testing which hook is stable.
- **Fallback:** If hook API changes, fall back to reading instructions file from config (pure config, no plugin).

### 3.7 External Services (MCP)
- **Chosen:** Config — Priority 2 (already configured: github, filesystem, notion, playwright, notebooklm).
- **M4 addition:** MCP readiness check in the launcher (fail-fast message if an MCP server fails to start, with retry guidance).

## 4. Explicitly Out of Scope (do not do in M4)

- Modifying `opencode.exe` or npm package internals.
- Editing `~/.local/share/opencode/*` (runtime DB, storage).
- Editing SDK-generated client files.
- Forking OpenCode.
- Replacing the dashboard with an OpenCode-internal one.
- Renaming/restructuring the existing agent/skill/command trees.

## 5. Rollback Plan

Every customization is a discrete file in `~/.config/opencode/` or Titus-Vault. Rollback = remove/restore that file.

| Change | Rollback |
|--------|----------|
| Theme `titus.json` | Delete file; `tui.json` back to `"theme": "opencode"` or unset |
| `tui.json` | Restore from `~/.config/opencode/backups/` (4 existing restore points) |
| Plugin `titus-m4-startup.ts` | Remove from `plugin` array in opencode.json |
| Launcher script | Delete; OpenCode still runs standalone |
| Config changes | `opencode.json` backed up before edit; restore point in `backups/` |

## 6. Verification Gate (Phase I)

Each customization is verified against: startup time impact, plugin load errors in log, dashboard connectivity, resume content correctness, theme rendering, and upgrade compatibility (dry-run check of `opencode debug` after install). Full checklist in M4_COMPLETION_REPORT.md.
