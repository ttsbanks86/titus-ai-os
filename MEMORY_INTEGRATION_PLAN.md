# Memory Integration Plan

**Date:** 2026-06-21
**Purpose:** Define how OpenCode reads from and writes to the Obsidian vault as its primary knowledge system.

---

## Current Problem

OpenCode currently has five separate memory systems:
1. **Agent .md files** (`.config/opencode/agent/`) — 23 files defining agent behavior.
2. **Skill SKILL.md files** (`.config/opencode/skills/`) — 76 files defining skill workflows.
3. **CLAUDE.md** (`.claude/CLAUDE.md`) — 130-line system philosophy document.
4. **Claude-mem** (separate MCP server) — currently offline, connection failed.
5. **Workspace files** — ~686 user-authored .md files scattered across 20+ directories.

None of these systems talk to each other. OpenCode reads CLAUDE.md and agent files at startup, but it does not automatically read project notes, daily notes, SOPs, or knowledge files. The result: every session requires the user to re-provide context that already exists in files.

---

## Target State

One knowledge system: **The Obsidian vault.** OpenCode reads from it. OpenCode writes to it. All other memory systems are either consolidated into the vault or archived.

### What OpenCode Reads

| Source | When | Purpose |
|---|---|---|
| `01-Dashboard/Home.md` | Session start | Vault index. Entry point for all context. |
| `01-Dashboard/My-Rules.md` | Session start | How to operate. Constraints. Preferences. |
| `01-Dashboard/My-Goals.md` | Session start | What matters. Direction. Priorities. |
| `01-Dashboard/My-Voice.md` | When writing | Voice and tone rules. |
| `02-Daily-Notes/today.md` | Session start | Yesterday's context. Open tasks. Decisions. |
| Project master notes | When working on a project | Current project state, linked notes. |
| SOP notes | Before executing a process | Documented workflow to follow. |
| Agent notes | When delegating to an agent | Agent capabilities, model, fallback. |
| Knowledge notes | When domain context is needed | Brand voice, tech stack, finances. |

### What OpenCode Writes

| Target | When | Content |
|---|---|---|
| `02-Daily-Notes/today.md` | Session end | Decisions, completed work, open tasks, problems. |
| Project master notes | When project state changes | Updated status, new tasks, completed milestones. |
| SOP notes | When a process is refined | Updated workflow, new steps, lessons learned. |

### What OpenCode Never Writes

| Never | Reason |
|---|---|
| New files outside the vault | Creates fragmentation. |
| Duplicate information across notes | Violates single source of truth. |
| Agent .md files | These are configuration, not memory. |
| CLAUDE.md | This is static philosophy, not dynamic memory. |
| Skill files | These are tool definitions, not memory. |

---

## Integration Mechanism

### Option A: Direct File I/O (Recommended)

OpenCode reads and writes vault files using its existing file system tools. This is the simplest and most reliable approach.

**Advantages:**
- No new infrastructure
- Works with any model provider
- Files are plain markdown — human-readable and version-controllable
- Zero latency (local filesystem)

**Implementation:**
```
Session Start:
  1. Read 01-Dashboard/Home.md
  2. Read 01-Dashboard/My-Rules.md
  3. Read 01-Dashboard/My-Goals.md
  4. Read 02-Daily-Notes/{date}.md (today or yesterday)
  5. Follow wiki-links to active project notes

During Session:
  6. Track: decisions, completed tasks, problems, open tasks

Session End:
  7. Write 02-Daily-Notes/{date}.md
  8. Update any project notes with changed state
```

### Option B: MCP Server (Future Enhancement)

A dedicated Obsidian MCP server could provide structured vault access with search, backlinks, and graph traversal. This is a future enhancement, not a Phase 1 requirement.

### Option C: Obsidian Plugin (Not Recommended)

An Obsidian plugin that communicates with OpenCode would require Obsidian to be running. This adds complexity without clear benefit over direct file I/O.

**Recommendation:** Start with Option A (direct file I/O). It works today with zero additional infrastructure. Add Option B later if the vault grows large enough to need structured search.

---

## CLAUDE.md Update

The current CLAUDE.md needs revision to reflect the vault as the primary knowledge system:

**Current CLAUDE.md behavior:**
- Contains system philosophy, routing rules, and fallback chains.
- Contains personal context (Titus identity).
- Serves as the primary startup file for OpenCode.

**Updated CLAUDE.md behavior:**
- Contains ONLY system philosophy, routing rules, and architecture.
- Personal context moves to `01-Dashboard/Personal-Context.md`.
- Rules move to `01-Dashboard/My-Rules.md`.
- At startup, OpenCode reads CLAUDE.md for system rules, then reads vault for context.

**Proposed CLAUDE.md additions:**
```markdown
## Knowledge System

- Primary knowledge source: Obsidian vault at `C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\`
- Session start: Read `01-Dashboard/Home.md`, `My-Rules.md`, `My-Goals.md`, today's daily note.
- Session end: Write today's daily note. Update project notes if state changed.
- SOPs: Before executing any process, check `07-SOPs/` for documented workflow.
- Never create knowledge files outside the vault.
- Never duplicate information.
- Archive, never delete.
```

---

## Agent Prompt Updates

Each agent's .md file should include a brief memory instruction:

```markdown
## Memory
When executing tasks, read relevant project notes from the Obsidian vault before acting.
After completing work, report findings to the CEO agent for daily note integration.
Do not create standalone memory files. All knowledge lives in the vault.
```

This ensures every agent participates in the shared knowledge system.

---

## Claude-mem Disposition

Claude-mem is currently offline (connection failed during audit). Its role in the new system:

- **If repairable:** Keep as a semantic search layer over the vault. Not a separate memory store.
- **If not repairable:** Decommission. The vault's wiki-link architecture provides sufficient retrieval without semantic search for the current scale (~54 master notes + ~150 sub-notes).

For the immediate term, decommission Claude-mem. The direct file I/O approach is sufficient. Re-evaluate when the vault exceeds 1,000 notes.

---

## Migration Checklist

- [ ] Create vault directory structure
- [ ] Create all master notes from MASTER_NOTES_PLAN.md
- [ ] Migrate personal context files to `01-Dashboard/`
- [ ] Migrate existing OBSIDIAN-AI-OS content to new vault structure
- [ ] Update CLAUDE.md with vault integration instructions
- [ ] Update agent .md files with memory instructions
- [ ] Decommission scattered knowledge systems (Knowledge_Base, AI_Agents memory, .claude/rules)
- [ ] Archive Claude-mem if offline
- [ ] Verify: OpenCode can start a session, read vault context, and execute without user-provided background

---

## Success Criteria

1. OpenCode reads `01-Dashboard/Home.md` at session start and follows wiki-links to load context.
2. OpenCode writes daily notes without being prompted.
3. Project notes accurately reflect current project state.
4. No new knowledge files appear outside the vault.
5. A session that starts in the morning can continue exactly where yesterday's session left off, with zero user context re-explanation.
