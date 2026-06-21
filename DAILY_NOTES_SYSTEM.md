# Daily Notes System

**Date:** 2026-06-21
**Purpose:** Define the daily notes format, workflow, and integration with the OpenCode operating system.

---

## Why Daily Notes

Daily notes are the operational memory of the Titus AI OS. They solve the "what happened yesterday" problem for OpenCode sessions. When an OpenCode instance starts, it reads today's daily note first. If today's note does not exist yet, it reads yesterday's. This gives every session immediate awareness of:
- What was worked on
- What decisions were made
- What problems are open
- What needs follow-up

Without daily notes, every session starts from zero context. With daily notes, every session continues from where the last one left off.

---

## Daily Note Format

Every daily note lives in `02-Daily-Notes/` and follows the naming convention `YYYY-MM-DD.md`.

### Template

```markdown
# YYYY-MM-DD

## Index
[One sentence summary of the day. Searchable.]

## Daily Summary
[2-4 sentences covering the major activities and outcomes.]

## Key Decisions
- Decision 1 — rationale
- Decision 2 — rationale

## Work Completed
- [x] Task that was finished
- [x] Another completed task

## Open Tasks
- [ ] Task still in progress
- [ ] Task blocked (with reason)

## Problems Encountered
- Problem 1 — attempted solutions, resolution status
- Problem 2 — attempted solutions, resolution status

## Follow-Up Actions
- [ ] Action 1 (due: date, owner: agent/person)
- [ ] Action 2 (due: date, owner: agent/person)

## Linked Projects
- [[Project-Name]] — brief status note
- [[Another-Project]] — brief status note

## Agent Sessions
- [[CEO-Agent]] — tasks executed
- [[Engineer-Agent]] — tasks executed
```

### Field Purposes

| Field | Purpose | Required? |
|---|---|---|
| **Index** | One-line summary for search and quick scan. | Yes |
| **Daily Summary** | Narrative of the day. What happened and why. | Yes |
| **Key Decisions** | Decisions that affect future work. Include rationale. | Only if decisions were made |
| **Work Completed** | What was finished. Progress markers. | Yes |
| **Open Tasks** | What is not done. Blockers, dependencies. | Yes |
| **Problems Encountered** | Issues that blocked or slowed work. | Only if problems occurred |
| **Follow-Up Actions** | Specific next actions with owners and dates. | Yes |
| **Linked Projects** | Which projects were worked on. Current status. | Yes |
| **Agent Sessions** | Which agents were used. What they did. | Only if agents were delegated |

---

## OpenCode Integration Workflow

### Session Start

When OpenCode starts a session, it follows this sequence:

1. **Check for today's daily note** at `02-Daily-Notes/YYYY-MM-DD.md`
2. **If today's note exists:** Read it. Load linked project notes for context.
3. **If today's note does not exist:** Read yesterday's note. Read any project notes linked from it. Create today's note from the template.
4. **Read `01-Dashboard/Home.md`** and follow wiki-links for active projects.
5. **Execute the user's request** with full context.

### During Session

OpenCode does not update the daily note mid-session (to avoid context fragmentation). Instead, it tracks:
- Decisions made
- Tasks completed
- Problems encountered
- New open tasks

At session end, it writes everything to the daily note.

### Session End

When a session ends (or the user requests a summary):

1. **Update the daily note** with all tracked items.
2. **Update linked project notes** if project state changed.
3. **Update any SOPs** if a process was refined.
4. **Verify the daily note is complete.**

---

## Multi-Session Coordination

If multiple OpenCode sessions run concurrently:

1. **Each session reads today's note at start.** This gives awareness of what other sessions are doing.
2. **Each session appends to the same daily note at end.** No conflicts because each session writes to different sections (or appends sequentially).
3. **Project notes are the single source of truth for project state.** If session A completes a task in [[CareNotes-Pro]], it updates the project note. Session B that starts later reads the updated project note and knows the state.

Rule: **Daily notes capture what happened. Project notes capture current state. SOPs capture how things should be done.**

---

## Example Daily Note

```markdown
# 2026-06-21

## Index
Obsidian vault migration audited, avatar video generated with OmniHuman + ElevenLabs voice research.

## Daily Summary
Performed full knowledge audit across three locations (Live Cowork, OpenCode config, Claude config). Identified 19,112 total .md files with 89% dead weight. Generated OmniHuman 1.5 avatar video from profile picture using KIE API + GitHub raw URLs. Researched professional avatar platforms (HeyGen, Synthesia, D-ID) for future pipeline. Began Obsidian vault migration deliverables.

## Key Decisions
- ElevenLabs voice cloning will be set up later; priority is vault migration first.
- Recommended D-ID + ElevenLabs as the professional avatar pipeline (API-first, native integration).
- Vault structure designed with 12 top-level folders, 54 master notes.
- Claude agent/skill system officially frozen; OpenCode is canonical runtime.

## Work Completed
- [x] Full knowledge audit (OBSIDIAN_MIGRATION_AUDIT.md)
- [x] Vault structure design (VAULT_STRUCTURE.md)
- [x] Master notes plan (MASTER_NOTES_PLAN.md)
- [x] OmniHuman avatar video generated and saved to desktop
- [x] Image uploaded to imgur, audio via Windows TTS, both to GitHub raw for KIE API

## Open Tasks
- [ ] Generate remaining vault migration deliverables
- [ ] Set up ElevenLabs API key and voice clone
- [ ] Evaluate professional avatar pipeline (D-ID vs HeyGen vs KIE OmniHuman)

## Problems Encountered
- KIE API model names don't match documentation — only `nano-banana-2` and `omnihuman-1-5` confirmed working. All video model names returned 422.
- KIE servers cannot download from imgur or catbox.moe — required GitHub raw URLs.
- Claude-mem MCP connection failed during audit. Need to investigate.

## Follow-Up Actions
- [ ] Complete vault migration deliverables (due: today)
- [ ] Test D-ID API with ElevenLabs integration (due: after vault setup)
- [ ] Fix claude-mem connection (due: when needed)

## Linked Projects
- [[Obsidian-Vault-Migration]] — audit complete, structure designed
- [[Professional-Avatar-Pipeline]] — researched, awaiting setup
- [[CareNotes-Pro]] — no activity today

## Agent Sessions
- [[CEO-Agent]] — orchestrated audit, research, and deliverables
- [[Research-Agent]] — attempted (failed), ran direct research instead
- [[Explore-Agent]] — file system audit
```

---

## Anti-Bloat Rules for Daily Notes

1. **One file per day.** Never split a day across multiple daily notes.
2. **Do not create daily notes for days with zero activity.** If nothing happened, no note.
3. **Do not duplicate project status in daily notes.** Link to the project note instead.
4. **Keep the Index field to one sentence.** It is for search, not summary.
5. **Archive old daily notes after 90 days.** Move to `10-Archive/Daily-Notes/`. Keep them searchable but out of the active view.

---

This system ensures every OpenCode session starts with context, ends with a record, and never loses track of what happened.
