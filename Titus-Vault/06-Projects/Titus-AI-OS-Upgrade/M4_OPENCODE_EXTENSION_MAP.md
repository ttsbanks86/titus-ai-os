# M4 OpenCode Extension Map

**Date:** 2026-07-31
**Applies to:** OpenCode 1.17.18
**Purpose:** Every OpenCode surface area, classified by modification safety for Titus AI OS.

---

## 1. Safe Extension Points (use these)

| # | Surface | Mechanism | Titus AI OS use |
|---|---------|-----------|-----------------|
| 1 | Server plugin hooks | `~/.config/opencode/plugins/*.ts` exporting `Plugin` | Startup orchestration, event logging, tool registration |
| 2 | Custom tools | `tool()` helper in plugins | `titus_status`, `titus_health`, knowledge/agent status tools |
| 3 | TUI plugin (slots) | `tui` export with `api.slots.register` | Branded home logo, sidebar content |
| 4 | TUI routes | `api.route.register` | Custom dashboard route inside TUI |
| 5 | Theme | `~/.config/opencode/themes/titus.json` | Full Titus brand palette |
| 6 | Theme selection | `tui.json` → `"theme": "titus"` | One-line switch |
| 7 | Commands | `~/.config/opencode/commands/*.md` | `/titus-status`, `/milestone`, `/resume` |
| 8 | Agents | `~/.config/opencode/agent/*.md` | Existing 25 agents — already in place |
| 9 | Skills | `~/.config/opencode/skills/*/SKILL.md` | 88 skills — already in place |
| 10 | MCP servers | `opencode.json` → `mcp` | 5 servers configured (github, filesystem, notion, playwright, notebooklm) |
| 11 | Providers | `opencode.json` → `provider` | DeepSeek configured; fallbacks via model routing |
| 12 | Permission rules | `opencode.json` → `permission` | Safety guardrails |
| 13 | Instructions | `opencode.json` → `instructions` + `CLAUDE.md` | OS rules injected into context |
| 14 | Events (SSE) | SDK `event()` / plugin `event` hook | Live dashboard state (session, vcs, todo) |
| 15 | KV store | `api.kv` (TUI plugin) | Persistent UI state (active project, milestone) |
| 16 | Workspace adapters | `experimental_workspace.register` | Future remote workspace types |

## 2. Supported Configuration (files to edit, not code)

| File | Location | Purpose |
|------|----------|---------|
| `opencode.json` | `~/.config/opencode/` | Global config (existing) |
| `tui.json` | `~/.config/opencode/` | TUI config: theme, keybinds, plugin_enabled |
| `themes/*.json` | `~/.config/opencode/themes/` | Custom themes |
| `commands/*.md` | `~/.config/opencode/commands/` | Custom slash commands |
| `agent/*.md` | `~/.config/opencode/agent/` | Agent definitions |
| `skills/*/SKILL.md` | `~/.config/opencode/skills/` | Skills |
| `plugins/*.ts` | `~/.config/opencode/plugins/` | Local plugins (auto-loaded) |
| `package.json` | `~/.config/opencode/` | Plugin npm dependencies |
| `.env` | `~/.config/opencode/` | Env vars for providers/plugins |

## 3. Plugin Architecture (current Titus install)

**Existing plugins (2 local):**
- `titus-safety-net.ts` — `titus_safety_scan` tool; pattern-based sensitive-data detection; warns, never blocks
- `titus-workflow-plugins.ts` — 13 category tools (pdf, zoom, brand_voice, hr, operations, design, product_management, productivity, legal, data, marketing, sales, finance)

**Existing npm plugin (1):**
- `opencode-mobile@latest` — mobile access (serve mode)

**Plugin resolution:** `file:///C:/Users/tbank/.config/opencode/plugins/*.ts` confirmed in resolved config.

## 4. Command System

- **Built-in commands:** `completion`, `acp`, `mcp`, `run`, `debug`, `providers`, `agent`, `upgrade`, `uninstall`, `serve`, `web`, `models`, `stats`, `export`, `import`, `github`, `pr`, `session`, `plugin`, `db`
- **Slash commands:** 23 custom commands in `~/.config/opencode/commands/` (business-ops, cleanup, code, deep, erase, git-master-discipline, mobile, personal-operator, research, skills, switcher-*, video-pipeline, youtube-autonomous, etc.)
- **Command palette:** `api.keymap.dispatchCommand("command.palette.show")`

## 5. MCP Integration (current)

| Server | Type | Purpose |
|--------|------|---------|
| github | local (npx) | GitHub API |
| filesystem | local (npx) | Live Cowork, Titus-Vault, Desktop, Documents, Downloads |
| notion | local (npx) | Notion workspace |
| playwright | local (npx) | Browser automation (chromium) |
| notebooklm | local (uvx) | NotebookLM |

All enabled, 300s timeout. MCP status observable via SDK `mcp.status()` and TUI `api.state.mcp()`.

## 6. Provider System (current)

- **Configured:** DeepSeek (deepseek-chat primary + small, deepseek-reasoner available)
- **Keys:** env-var references (`{env:DEEPSEEK_API_KEY}`)
- **Routing:** `model` + `small_model` + `default_agent: ceo`
- **Fallback chain:** CEO routing in CLAUDE.md documents OpenCodeGo → Ollama → DeepSeek → GPT-4o-mini → local

## 7. Never-Modify List

1. `C:\Users\tbank\AppData\Roaming\npm\node_modules\opencode-ai\*` (all npm package files)
2. `opencode.exe` binary
3. `~/.local/share/opencode/opencode.db` (+ -wal, -shm)
4. `~/.local/share/opencode/storage/*` (runtime)
5. `~/.config/opencode/node_modules/*` (managed by bun install)
6. `~/.cache/opencode/*` (cache)
7. Any file inside `~/.config/opencode/backups/` (keep as restore points)

## 8. Customization-Intended Files

1. `~/.config/opencode/opencode.json` — primary config (exists, safe to edit)
2. `~/.config/opencode/tui.json` — TUI config (NEW — will create)
3. `~/.config/opencode/themes/titus.json` — Titus theme (NEW — will create)
4. `~/.config/opencode/plugins/titus-*.ts` — Titus plugins (exists; add M4 plugin)
5. `~/.config/opencode/commands/*.md` — Titus commands (exists)
6. `~/.config/opencode/agent/*.md` — Titus agents (exists)
7. `~/.config/opencode/package.json` — plugin deps (exists)
8. `<repo>/.opencode/` — project-level plugins/agents/skills (exists)

## 9. Update Compatibility

- All customization lives in `~/.config/opencode/` (persists across `opencode upgrade`)
- Plugin API version pinned: `@opencode-ai/plugin` 1.15.4 (installed in config package.json)
- Breaking-change watch: `experimental.*` hooks and `experimental_workspace` may change
- Migration path: backup `opencode.json` before major upgrades (already automated — `backups/` dir has 4 restore points)
- `opencode upgrade` verified as the only update path; binary replaced, config untouched
