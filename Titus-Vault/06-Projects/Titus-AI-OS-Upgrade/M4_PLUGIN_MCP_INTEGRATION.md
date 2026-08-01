# M4 Plugin & MCP Integration Audit

**Date:** 2026-07-31
**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Status:** AUDIT COMPLETE

---

## 1. Existing Plugin Inventory

| Plugin | Type | Status | Notes |
|--------|------|--------|-------|
| `titus-safety-net.ts` | Local (TS) | ✅ active | `titus_safety_scan` tool; regex pattern matching (sk-/pk- keys, GitHub tokens, AWS, private keys, SSN, credit cards, inline passwords, Mongo/Postgres URIs); **warns, never blocks** |
| `titus-workflow-plugins.ts` | Local (TS) | ✅ active | Category tools (13): pdf, zoom, brand_voice, hr, operations, design, product_management, productivity, legal, data, marketing, sales, finance — each with promise/guardrails/workflow/outputs |
| `opencode-mobile@latest` | npm | ✅ active | Mobile access via serve mode |

**Plugin API version pinned:** `@opencode-ai/plugin@1.15.4` (in `~/.config/opencode/package.json`).

**Load mechanism:** `file:///` paths in `opencode.json` `plugin` array. Verified in resolved config.

## 2. Existing MCP Inventory

| Server | Runner | Purpose | Health |
|--------|--------|---------|--------|
| `github` | npx `@modelcontextprotocol/server-github` | GitHub API (repos, PRs, issues) | ✅ configured |
| `filesystem` | npx `server-filesystem` | Live Cowork, Titus-Vault, Desktop, Documents, Downloads | ✅ configured |
| `notion` | npx `@notionhq/notion-mcp-server` | Notion workspace | ✅ configured |
| `playwright` | npx `@playwright/mcp` (BROWSER=chromium) | Browser automation | ✅ configured |
| `notebooklm` | uvx `notebooklm-mcp-cli` | NotebookLM | ✅ configured |

All local, `experimental.mcp_timeout` = 300000 ms.

## 3. Audit Findings

### Gaps
1. **No startup/resume automation.** Sessions start cold — no milestone/project/today-context injection. (M4 fills this: `titus-m4-startup.ts`.)
2. **No Titus status tool.** Dashboard has routes but OpenCode has no quick `/titus status`. (M4 fills this.)
3. **No health tool.** No way to verify dashboard/knowledge/records health from inside a session. (M4 fills this.)
4. **Theme not branded.** Default theme only. (M4 fills this: `themes/titus.json`.)
5. **Dashboard stale values.** `/api/workspace` and `/api/milestones` contain hardcoded M3-era values that now conflict with real state (M3 complete, M4 current, 166 tests). (M4 fix in Phase G.)
6. **No CURRENT_MILESTONE.md record.** Resume source missing; must be created (Phase J).
7. **No `tui.json`.** Theme selection and TUI plugin config unset. (M4 creates it.)
8. **MCP servers lack startup readiness check.** Launcher should verify MCP availability and report failures. (M4 launcher.)

### Strengths (keep as-is)
1. Safety net is warn-only and pattern-based — correct posture.
2. Workflow plugins are category-keyed and well-scoped.
3. MCP set covers the operational surface (github/filesystem/notion/playwright/notebooklm).
4. Plugin API pinned — upgrade risk contained.

## 4. Recommended Bundle (M4 deliverables)

| # | Component | Type | Purpose |
|---|-----------|------|---------|
| 1 | `titus-m4-startup.ts` | Plugin (local) | Startup hooks: resume context injection on `session.created`; `/titus status` + `/titus resume` commands; `titus_status`, `titus_resume`, `titus_health` tools |
| 2 | `titus.json` | Theme | Brand palette mapping (dark primary, light secondary) |
| 3 | `tui.json` | Config | `"theme": "titus"`, plugin_enabled, keybinds for Titus commands |
| 4 | `Start-TitusAIOS.ps1` | Launcher | Idempotent dashboard + OpenCode unified startup; MCP readiness note |
| 5 | Dashboard patch | Code (Titus-owned) | `/api/workspace` + `/api/milestones` read vault instead of hardcoded values |
| 6 | `CURRENT_MILESTONE.md` | Record (vault) | Active milestone source for resume + dashboard |
| 7 | `commands/titus-*.md` | Commands | `/titus-status` (human-readable status from vault) — complements plugin tool |

## 5. Non-Recommendations (explicitly out)

- Do NOT add more MCP servers in M4 (current 5 suffice; scope creep).
- Do NOT modify `titus-safety-net.ts` behavior (warn-only is correct).
- Do NOT touch `opencode-mobile` (works, out of M4 scope).
- Do NOT convert workflow-plugins categories to MCP (plugin tools are the right layer).

## 6. Verification Plan (Phase I)

1. Plugin loads clean: `opencode` starts, no plugin errors in `~/.local/share/opencode/log/`.
2. `/titus status` returns milestone/project/test data from vault.
3. Resume context present in a fresh session (milestone + project + today's tasks).
4. Theme renders: navy background, gold accent, cream text in TUI.
5. `tui.json` selects Titus theme; `/theme` lists it.
6. Launcher idempotent: second run starts nothing new.
7. Dashboard endpoints return current (M4) values.
8. `opencode upgrade` simulation: config dir untouched (backup/restore test in Phase I).
