# Open Design API and MCP Setup Notes

Date: 2026-07-11

## Current confirmed state

- Open Design Desktop is installed.
- Open Design is configured to use `opencode` as its local agent.
- `od` CLI is not currently available on PATH.
- OpenCode is installed and working.
- OpenCode config currently has NotebookLM MCP configured.
- No API keys were written to files during setup.
- Open Design telemetry is now off for metrics, content, and artifact manifest.
- Open Design `customInstructions` now points Titus/Open Door work to the reusable `DESIGN.md` file.
- The Titus Open Door design-system package lives at `C:\Users\tbank\Desktop\Live Cowork\BRAND\Open-Design\design-systems\titus-open-door\`.

## Local-first routing policy

Preferred order:

1. OpenCode default local or low-cost model path.
2. Ollama local models when available.
3. DeepSeek API when configured by environment variable.
4. GPT-4o-mini or similar low-cost fallback when explicitly approved.
5. Premium models only for final review, not loops.

## MCP setup policy

Only install MCP servers that meet these requirements:

- They can run locally or with explicit credentials.
- They do not require storing secrets in repo files.
- They support clear enable/disable controls.
- They do not auto-publish, auto-spend, or auto-upload.
- They can be audited from config before use.

## Recommended MCP entries for OpenCode

Already configured:

- `notebooklm`

Candidate entries to add after verification:

- `open-design`: blocked for now. The installed app exposes Open Design runtime packages, but no verified MCP executable or `od` CLI command was found.
- `playwright`: for browser inspection of generated pages.
- `filesystem`: only with restricted roots, never full user profile.

## Open Design custom design-system registration

Read-only inspection found that bundled design systems are stored as records in the Open Design SQLite `installed_plugins` table. Existing records are all `source_kind='bundled'` and `trust='bundled'`.

Decision:

- Do not edit bundled app resources.
- Do not direct-insert a custom plugin into SQLite unless the user explicitly approves a backup-backed experiment.
- Use the existing Open Design `customInstructions` field as the safe integration path.
- Keep the `open-design.json` manifest ready for future official import support.

## API keys

Do not store API keys in `opencode.json`, `DESIGN.md`, or Open Design project files.

Use user-level environment variables only:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_GENERATIVE_AI_API_KEY`
- `DEEPSEEK_API_KEY`
- `OPENROUTER_API_KEY`

If a key is missing, workflows should degrade to local or ask for approval.

## Open Design telemetry recommendation

For Titus work, use privacy-first settings:

- Metrics telemetry: off unless explicitly approved. Current: off.
- Content telemetry: off. Current: off.
- Artifact manifest telemetry: off. Current: off.

## Verification checklist

- Open Design opens without sign-in.
- Open Design uses Local CLI, OpenCode, default.
- Titus Open Door design system file exists.
- Open Design custom instructions reference the Titus Open Door design system.
- A small prototype can be generated without external account sign-in.
- No secrets appear in changed files.
