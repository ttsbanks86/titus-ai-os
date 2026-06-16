# AI OS Troubleshooting Lessons

Date started: 2026-06-16
Purpose: Compact operational memory so future agents do not repeat the same mistakes.

---

## Bot / Gateway / Token Safety

- Never assume BotFather text, pasted token text, and running gateway logs refer to the same bot. Verify with Telegram `getMe` or gateway logs before configuring automation.
- If a token was pasted in chat, treat it as exposed. Use it only for temporary diagnosis, then rotate before production or 24/7 deployment.
- Gateway status must be verified by actual log lines, not assumptions. Look for `gateway ready`, provider username, loaded plugins, model name, and listening port.
- Keep bot runtime folders separate: Hermes/OpenClaw gateway files should not be mixed with OpenCode config unless intentionally bridged.
- Do not create a new bot project if an existing working bot is already confirmed. First inspect the running gateway and existing app folders.

## Windows Build / EXE Locking

- If PyInstaller or file copy fails with `Permission denied` on an EXE, first check whether the app is still running. Stop the process before rebuilding.
- After rebuilding a Windows desktop app, verify the resulting EXE exists and verify the desktop shortcut target points to the rebuilt EXE.
- Do not report a rebuild as complete until source compile, EXE build, and shortcut verification are done.

## DocFlow / PySide UI Bugs

- Recursive overrides can crash PySide/PyQt apps. If a method like `show()` calls `self.show()`, replace with `super().show()`.
- For UI startup crashes, inspect the call stack first, then patch the narrowest failing method. Avoid refactoring the full app unless asked.

## Command Center

- Command Center should be treated as the visible control surface for the AI OS: bots, DocFlow, CRM/API, learning captures, skills/agents inventory, and memory status.
- For each new operational capability, prefer adding a simple button/status panel before building a complex dashboard.
- Before adding new buttons, verify target paths exist.

## Git / Repo Capture on Windows

- Large public repos can fail under deeply nested folders because of Windows path length. Clone large repos into short paths such as `C:\Users\tbank\Desktop\repo-name`, then copy selected outputs later.
- If a clone fails halfway, do not trust the partial directory. Mark it as failed and either delete/archive after approval or reclone in a short path.

## Skills / Agents

- Do not merge all skill folders into one giant runtime. Keep OpenCode, Claude, Goose, and workspace skills standalone.
- Do not delete or archive agents/skills without explicit user approval.
- First create a registry with runtime, path, status, risk, and keep/archive recommendation.
- Duplicate skill names are not automatically bad. Compare content and runtime purpose first.
- `skill-store/SKILL-INDEX.md` should be regenerated from actual installed skill folders; do not trust it as source of truth until refreshed.

## Memory / Brain

- Every major project should have a project note, troubleshooting note, and next-action note.
- For long sessions, create a regrounding summary before compaction or handoff.
- Keep concise lessons in this file; keep longer context in Obsidian/project notes.
- Add searchable observations to memory only after checking for duplicates when possible.

## Approval Gates

Always ask before:

- deleting files or folders
- archiving agents/skills
- connecting accounts
- sending email/social/LinkedIn messages
- posting or uploading content
- spending money
- deploying exposed services
- enabling always-on mic/camera
- using leaked/pasted secrets for production

## Default Recovery Pattern

When stuck:

1. Verify actual state with logs/files/processes.
2. Identify the smallest failing component.
3. Patch narrowly.
4. Run the minimum meaningful verification.
5. Write the lesson here if it can prevent recurrence.
