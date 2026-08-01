# M4 Update Compatibility

**Date:** 2026-07-31
**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Status:** ASSESSED

---

## 1. Principle

All M4 customization lives outside the OpenCode binary and npm package. `opencode upgrade` replaces the binary and package files only — it never touches `~/.config/opencode/` or Titus-Vault. Every M4 deliverable survives upgrades by construction.

## 2. What `opencode upgrade` Replaces (verified)

| Path | Replaced | M4 impact |
|------|----------|-----------|
| `C:\Users\tbank\AppData\Roaming\npm\node_modules\opencode-ai\` | Yes (binary + launcher) | None — nothing M4 edits lives here |
| `opencode.exe` (platform pkg) | Yes | None |
| `~/.cache/opencode/*` | Yes (cache) | None (regenerated) |

## 3. What Survives Upgrades

| Path | Content | M4 deliverable |
|------|---------|----------------|
| `~/.config/opencode/opencode.json` | Global config | pre-existing (M3 era) |
| `~/.config/opencode/tui.json` | Theme selection | M4 (created) |
| `~/.config/opencode/themes/titus.json` | Titus theme | M4 (created) |
| `~/.config/opencode/plugins/*.ts` | Titus plugins (safety-net, workflow, m4-startup) | M4 (m4-startup created) |
| `~/.config/opencode/commands/*.md` | Slash commands (incl. titus-status) | M4 (titus-status created) |
| `~/.config/opencode/agent/*.md` | Agents | pre-existing |
| `~/.config/opencode/skills/*` | Skills | pre-existing |
| `~/.config/opencode/package.json` | Plugin deps (pinned API) | pre-existing |
| `Titus-Vault\06-Projects\Titus-AI-OS-Upgrade\*.md` | M4 docs + records | M4 (created) |
| `Live Cowork\bin\Start-TitusAIOS.ps1` | Unified launcher | M4 (created) |
| `titus-ai-os-dashboard\api\*.py` | Dashboard API (patched) | M4 (patched) |

## 4. Plugin API Pinning

- `@opencode-ai/plugin@1.15.4` pinned in `~/.config/opencode/package.json` (verified).
- The M4 startup plugin uses only stable hooks: `tool` (tool definitions), `event` (session.created). These are core API surface, present since plugin API 1.x.
- `experimental.*` hooks (chat.system.transform, session.compacting) are NOT used by the M4 plugin — deliberately, to minimize breakage risk. If a future M5 needs system-prompt injection, it will be gated behind a compatibility check.

## 5. Theme/Config Format Stability

- Theme JSON format (`$schema: https://opencode.ai/theme.json`) is documented and stable. All 50 tokens validated against the schema.
- `tui.json` format is documented (`https://opencode.ai/tui.json`). Only `$schema` and `theme` keys used — the minimal surface.
- If a future OpenCode renames theme tokens, the fix is a one-file edit (`themes/titus.json`), no code.

## 6. Dashboard Decoupling

- Dashboard (FastAPI :8000, static :3000) is fully independent of OpenCode. No shared runtime state; both read Titus-Vault.
- Dashboard upgrades are independent of OpenCode upgrades.
- M4 dashboard patch (main.py, milestones.py) reads vault records — the same pattern the dashboard already used for other routes.

## 7. Launcher Resilience

- `Start-TitusAIOS.ps1` invokes `opencode` from PATH — if OpenCode upgrades change CLI behavior, the launcher needs no change (it only spawns the process).
- Port checks make the launcher immune to dashboard restart churn.
- All failures are non-fatal (warn and continue).

## 8. Upgrade Test (Phase I, done)

| Check | Result |
|-------|--------|
| `opencode debug config` after M4 changes | ✅ loads all plugins + config, no errors |
| Plugin init logs | ✅ opencode-mobile + Titus plugins init OK |
| Theme file validation (50 tokens) | ✅ all valid |
| Dashboard tests after patch (35) | ✅ all pass |
| Core knowledge tests (68) | ✅ all pass |
| Live API endpoints | ✅ M4 current, 166/166 tests |
| Launcher parse + run | ✅ idempotent, milestone read correct |

## 9. Conclusion

M4 customization is upgrade-proof by design: zero changes inside the binary, npm package, or runtime data dirs; all extension points are documented, pinned, or format-stable; rollback is per-file. `opencode upgrade` can run at any time without preparation beyond the existing config backups (`~/.config/opencode/backups/`).
