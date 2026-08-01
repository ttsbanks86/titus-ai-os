# M4 Architecture Inspection

**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Date:** 2026-07-31
**Inspected:** OpenCode 1.17.18 (opencode-ai@1.17.18, npm global)
**Status:** COMPLETE

---

## 1. Application Architecture

OpenCode 1.17.18 is distributed as a **compiled Bun single-file binary** (`opencode.exe`, ~184 MB) via npm package `opencode-ai`. The npm package is a launcher wrapper only (`bin/opencode.exe` + `postinstall.mjs`); platform binaries ship as optional dependencies (`opencode-windows-x64`, etc.).

**Runtime:** Bun (compiled binary)
**Language:** TypeScript (compiled)
**Distribution:** npm `opencode-ai` → platform binaries

### Component Layers (from observable surface)

| Layer | Technology | Evidence |
|-------|-----------|----------|
| **TUI (frontend)** | OpenTUI — `@opentui/core`, `@opentui/solid` (SolidJS-based terminal UI), `@opentui/keymap` | Plugin package peerDependencies; `tui.d.ts` imports `@opentui/core`, `@opentui/solid`, `@opentui/keymap` |
| **Server (backend)** | Headless server (`opencode serve`), SDK server/client (`@opencode-ai/sdk`), SSE event bus | `sdk.gen.d.ts` client class; `server.d.ts` `createOpencodeServer`; CLI `opencode serve` |
| **State** | SQLite (`opencode.db` in `~/.local/share/opencode`), JSON storage, KV | Data dir listing shows `opencode.db`, `storage/`, `snapshot/`, `repos/` |
| **Config** | JSON config files (`opencode.json`, `tui.json`, theme JSON) | Resolved via `opencode debug config` |
| **Shell** | Bun shell API (`$`) injected into plugins | `shell.d.ts` (`BunShell`) |
| **Plugins** | TypeScript/JS modules with hooks | `index.d.ts` (`Hooks` interface), auto-loaded from plugin dirs |

### Frontend
- **Framework:** OpenTUI + SolidJS (`@opentui/solid`) for the terminal UI
- **Rendering:** CLI renderer (`CliRenderer` from `@opentui/core`)
- **Slots system:** Host slots (`app`, `home_logo`, `home_prompt`, `session_prompt`, `sidebar_title`, `sidebar_content`, `sidebar_footer`, `home_bottom`, `home_footer`) registered via `api.slots.register`
- **Routes:** TUI routes (`home`, `session`, custom) via `api.route.register`
- **Theme:** JSON theme system with dark/light variants; `api.theme` (install/set/has/mode)
- **Commands/keymap:** `api.keymap` with layers, bindings, command palette (`command.palette.show`)
- **Dialogs/UI:** `api.ui` (Dialog, DialogAlert, DialogConfirm, DialogPrompt, DialogSelect, Slot, Prompt, toast)
- **Attention:** `api.attention` (notifications + soundboard)

### Backend
- **Server:** `opencode serve` starts a headless server; `opencode web` starts server + web UI
- **SDK client:** full typed client — `project`, `session`, `message`, `tool`, `config`, `provider`, `mcp`, `lsp`, `vcs`, `event` (SSE), `tui` control
- **Events:** SSE event bus; ~50 event types (session.*, message.*, tool.*, file.*, permission.*, tui.*, vcs.branch.updated, etc.)

## 2. Startup Sequence (observed)

1. `opencode.exe` launched
2. Config loaded: `~/.config/opencode/opencode.json` → project `opencode.json`
3. Plugins loaded (order): global config → project config → global plugin dir → project plugin dir
4. MCP servers launched (config-specified)
5. Server starts (port binding)
6. TUI starts; routes render; workspace/project detected from cwd
7. Session state restored (if `--continue` / `--session`)
8. `opencode debug startup` reports timing (~570 ms)

**Note:** On Windows the desktop app state dir is `C:\Users\tbank\AppData\Roaming\ai.opencode.desktop\opencode`.

## 3. Configuration System

- **Global config:** `~/.config/opencode/opencode.json` (validated against `https://opencode.ai/config.json`)
- **Project config:** `<project-root>/opencode.json` (project-level override)
- **TUI config:** `~/.config/opencode/tui.json` (theme, keybinds, prompt, plugin_enabled, attention, mouse, etc.)
- **Env:** `.env` in config dir; env var references `{env:VAR}` in provider config
- **Schema keys:** `agent`, `model`, `small_model`, `default_agent`, `provider`, `mcp`, `plugin`, `permission`, `instructions`, `experimental`, `shell`, `formatter`, `lsp`, `snapshot`, `skills`, `watcher`, `layout`, `autoupdate`, `server`, `command`, `compaction`, `mode`, `username`, `disabled_providers`, `enabled_providers`, `enterprise`, `reference(s)`, `share`, `subagent_depth`, `tool_output`, `tools`, `attachment`

## 4. Extension Points (documented, official)

| Extension Point | Mechanism | Class |
|-----------------|-----------|-------|
| **Plugins** | `~/.config/opencode/plugins/*.ts` / `.opencode/plugins/*.ts` — auto-loaded; hooks object | **PLUGIN** |
| **Custom tools** | Plugin `tool: { name: ToolDefinition }` with Zod schema; `tool()` helper | **PLUGIN** |
| **Server hooks** | `event`, `config`, `chat.message`, `chat.params`, `chat.headers`, `permission.ask`, `command.execute.before`, `tool.execute.before/after`, `shell.env`, `tool.definition`, compaction hooks | **PLUGIN** |
| **TUI plugin** | `tui` export — `api.route.register`, `api.slots.register`, `api.keymap`, `api.theme`, `api.kv`, `api.ui`, `api.attention`, `api.event`, `api.state` | **PLUGIN** |
| **Themes** | `~/.config/opencode/themes/*.json` — full color token mapping | **THEME** |
| **Theme selection** | `tui.json` `theme` key; `/theme` command; `api.theme.set/install` | **SUPPORTED_CONFIGURATION** |
| **Custom commands** | `~/.config/opencode/commands/*.md` — slash commands with templates | **SUPPORTED_CONFIGURATION** |
| **Agents** | `~/.config/opencode/agent/*.md` — markdown agent definitions | **SUPPORTED_CONFIGURATION** |
| **Skills** | `~/.config/opencode/skills/*/SKILL.md` — skill loading | **SUPPORTED_CONFIGURATION** |
| **MCP servers** | `opencode.json` `mcp` section — local/remote/oAuth | **SUPPORTED_CONFIGURATION** |
| **Providers** | `opencode.json` `provider` section — custom provider/models | **SUPPORTED_CONFIGURATION** |
| **Model routing** | `model`, `small_model` config | **SUPPORTED_CONFIGURATION** |
| **Instructions** | `instructions` config; `CLAUDE.md` (respected by tooling) | **SUPPORTED_CONFIGURATION** |
| **Permissions** | `permission` config — rules/ask/deny/allow | **SUPPORTED_CONFIGURATION** |
| **Keybinds** | `tui.json` `keybinds`; `api.keymap.registerLayer` | **SUPPORTED_CONFIGURATION** / **PLUGIN** |
| **npm plugins** | `plugin: ["pkg@version"]` — installed via Bun | **PLUGIN** |
| **Workspace adapters** | `experimental_workspace.register(type, adapter)` | **PLUGIN** (experimental) |

## 5. Unsafe / Unsupported Modification Points

| Area | Why unsafe | Class |
|------|-----------|-------|
| `opencode.exe` binary | Compiled artifact; modified on every upgrade; not editable | **UNSUPPORTED** |
| npm package internals (`opencode-ai/`) | Replaced on every `opencode upgrade` | **UNSUPPORTED** |
| SDK-generated client files | Generated code; overwritten on upgrade | **UNSUPPORTED** |
| `~/.local/share/opencode/opencode.db` | Runtime state; format not stable | **UNSUPPORTED** |
| Internal TUI component tree | Not exposed beyond slots; would require fork | **REQUIRES_FORK** |
| Server request handlers | Not overridable; use hooks instead | **REQUIRES_FORK** |
| Provider auth internals | Use `auth` hook / `provider` hook | **REQUIRES_FORK** (for deep changes) |

## 6. Findings for M4 Requirements

| Requirement | Finding | Classification |
|-------------|---------|----------------|
| Existing branding support | Yes — full JSON theme system with all UI tokens (primary, background, markdown, syntax, diff) | **SAFE_EXTENSION** |
| Existing dashboard support | No built-in dashboard; dashboard is a separate app (Titus FastAPI dashboard exists from M3); OpenCode TUI slots (`home_logo`, `home_footer`, `sidebar_content`) can embed custom views | **PLUGIN** (slots) |
| Existing command palette | Yes — `command.palette.show`, `api.keymap.dispatchCommand`, custom commands | **SUPPORTED_CONFIGURATION** |
| Existing startup hooks | Yes — plugin `event` hook (session.* events), `experimental.chat.system.transform`, plugin init runs at startup | **PLUGIN** |
| Existing plugin architecture | Yes — mature plugin system, server + TUI plugins, npm + local file plugins | **PLUGIN** |
| Existing automation hooks | Yes — `tool.execute.before/after`, `command.execute.before`, `permission.ask`, `shell.env`, event bus | **PLUGIN** |
| Existing MCP integration | Yes — native MCP config (5 servers currently configured) | **SUPPORTED_CONFIGURATION** |
| Existing provider system | Yes — provider config with fallbacks; DeepSeek configured; env-var keys | **SUPPORTED_CONFIGURATION** |
| Workspace/project loading | Yes — project detection from cwd; `project.current` via SDK; worktree support | **SUPPORTED_CONFIGURATION** |
| Session restore | Yes — `--continue`/`--session` flags; session list/create/fork via SDK | **SUPPORTED_CONFIGURATION** |
| Build pipeline | Bun-compiled; not part of user extensibility | **UNSUPPORTED** (for user) |
| Update mechanism | `opencode upgrade`; `autoupdate` config; `installation.updated` event | **SUPPORTED_CONFIGURATION** |

## 7. Classification Summary

- **SAFE_EXTENSION:** plugin hooks, custom tools, TUI slots, routes, theme install, KV store, attention, events
- **SUPPORTED_CONFIGURATION:** opencode.json, tui.json, themes/*.json, commands, agents, skills, MCP, providers, permissions, instructions
- **PLUGIN:** server plugins + TUI plugins (npm or local file)
- **THEME:** JSON theme files with dark/light variants
- **REQUIRES_FORK:** internal TUI component tree, server handlers (only if hooks insufficient)
- **UNSUPPORTED:** compiled binary, npm package internals, SQLite runtime DB, generated SDK files

## 8. Implications for M4

1. **No fork required.** Every desired Titus AI OS feature maps to a supported extension mechanism.
2. **Priority path:** Theme (JSON) → Config (tui.json/opencode.json) → Plugin (local TS plugins) → Extension (hooks/tools/slots/routes) → Wrapper (startup script) → Fork (never, for M4 scope).
3. **Startup automation:** Achievable via plugin init + event hooks + a lightweight launcher wrapper (PowerShell) that starts OpenCode with the workspace and the dashboard.
4. **Live connections:** Read from OpenCode via SDK client (project, session, vcs, mcp, event SSE) or via plugin state (KV + events). Avoid duplicating state.
5. **Update compatibility:** All customization lives outside the binary (config dir, plugin dirs, theme files). `opencode upgrade` preserves all of it.
