# Migration Execution Plan

**Date:** 2026-06-21
**Status:** Plan complete. Awaiting approval to execute.

---

## Overview

This plan migrates the Titus AI OS from five scattered knowledge systems into one structured Obsidian vault. The migration is designed to be safe (zero deletion), phased (incremental progress), and reversible (archive checkpoints at each phase).

---

## Pre-Migration Checklist

Before any files move:
- [ ] User reviews and approves this plan
- [ ] All 6 planning documents reviewed (Audit, Structure, Master Notes, Daily Notes, Memory Integration, SOP Framework)
- [ ] Git working tree is clean (stash or commit pending changes)
- [ ] Archive checkpoint created (ZIP of current state)
- [ ] Vault root directory created at `C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\`

---

## Phase 0: Safety Checkpoint

**Duration:** 5 minutes
**Risk:** Zero
**Reversible:** Yes

1. Commit all current planning documents to git.
2. Create archive checkpoint:
   ```
   ZIP: C:\Users\tbank\.agent-archive\PRE-VAULT-MIGRATION-2026-06-21.zip
   ```
3. Verify the ZIP is valid and restorable.

**Success criteria:** Rollback point exists. All current files are safe.

---

## Phase 1: Create Vault Structure

**Duration:** 10 minutes
**Risk:** Zero (only creates empty directories)
**Reversible:** Yes (delete empty directories)

1. Create the vault root: `Titus-Vault/`
2. Create all 12 top-level folders:
   ```
   01-Dashboard/
   02-Daily-Notes/
   03-Businesses/
   04-Products/
   05-Career/
   06-Projects/
   07-SOPs/
   08-Agents/
   09-Knowledge/
   10-Archive/
   11-Templates/
   12-Reference/
   ```
3. Create subdirectories:
   ```
   07-SOPs/Career/
   07-SOPs/Content/
   07-SOPs/Business/
   07-SOPs/Development/
   07-SOPs/Operations/
   07-SOPs/Marketing/
   09-Knowledge/AI-Systems/
   09-Knowledge/Brand/
   09-Knowledge/Marketing/
   09-Knowledge/Technology/
   09-Knowledge/Finance/
   10-Archive/ChatGPT-Exports/
   10-Archive/Legacy-Agents/
   10-Archive/Legacy-Skills/
   10-Archive/Legacy-Commands/
   10-Archive/Legacy-Rules/
   10-Archive/Staging/
   10-Archive/Deprecated-Projects/
   10-Archive/Daily-Notes/
   12-Reference/Books/
   12-Reference/Courses/
   12-Reference/Papers/
   12-Reference/People/
   ```
4. Create all 11 template files from `11-Templates/` specifications.
5. Create index notes: `SOPs-Index.md`, `Agents-Index.md`, `Knowledge-Index.md`, `Templates-Index.md`, `Archive-Index.md`, `Reference-Index.md`.

**Success criteria:** Full directory tree exists. All template files created.

---

## Phase 2: Migrate Personal Context

**Duration:** 15 minutes
**Risk:** Low (moving small number of files)
**Reversible:** Yes (original files remain until verified)

1. Consolidate `my-context.md` → `01-Dashboard/Personal-Context.md`
   - Remove duplicate copies in `ABOUT ME/`
   - Add wiki-links to related areas
2. Consolidate `my-rules.md` → `01-Dashboard/My-Rules.md`
   - Preserve all rules verbatim
   - Add vault-specific rules (from MEMORY_INTEGRATION_PLAN.md)
3. Consolidate `my-goals.md` → `01-Dashboard/My-Goals.md`
   - Preserve all goals verbatim
   - Add timeline context
4. Consolidate `my-voice.md` → `01-Dashboard/My-Voice.md`
   - Remove all duplicate copies
   - This becomes the single canonical voice definition
5. Create `01-Dashboard/Home.md` — the vault index
   - Wiki-links to every Tier 2 master note
   - One-paragraph summaries for each area

**Success criteria:** All personal context centralized in `01-Dashboard/`. Zero duplicates remain.

---

## Phase 3: Migrate Existing Obsidian Content

**Duration:** 15 minutes
**Risk:** Low (moving content to new structure)
**Reversible:** Yes (original OBSIDIAN-AI-OS preserved until verified)

1. Move `OBSIDIAN-AI-OS/01-Projects/` → `06-Projects/`
2. Move `OBSIDIAN-AI-OS/02-Agents/` → `08-Agents/`
3. Move `OBSIDIAN-AI-OS/03-Skills/` → `09-Knowledge/AI-Systems/Skill-Registry/`
4. Move `OBSIDIAN-AI-OS/06-Daily-Logs/` → `02-Daily-Notes/`
5. Move `OBSIDIAN-AI-OS/04-Troubleshooting/` → `10-Archive/Legacy-Troubleshooting/`
6. Move `OBSIDIAN-AI-OS/05-Decisions/` → integrated into relevant project notes
7. Archive the now-empty `OBSIDIAN-AI-OS/` directory

**Success criteria:** All existing Obsidian content migrated. Old directory archived.

---

## Phase 4: Create Master Notes

**Duration:** 60 minutes
**Risk:** Low (creating new files only)
**Reversible:** N/A (new files, nothing overwritten)

Create all 54 master notes per MASTER_NOTES_PLAN.md:

### Tier 1 (5 notes)
- [ ] Home.md
- [ ] Personal-Context.md
- [ ] My-Rules.md
- [ ] My-Goals.md
- [ ] My-Voice.md

### Tier 2 — Businesses (4 notes)
- [ ] Businesses.md
- [ ] CareNotes-Pro.md
- [ ] Business-Ideas.md
- [ ] Legacy-Businesses.md

### Tier 2 — Products (9 notes)
- [ ] Products.md
- [ ] Personal-AI-Operator.md
- [ ] Content-Income-System.md
- [ ] EchoKeys.md
- [ ] NOLA-Voice.md
- [ ] Whisper-Pro.md
- [ ] Floating-AI-Tutor.md
- [ ] DocFlow.md
- [ ] Hermes-Gateway.md

### Tier 2 — Career (8 notes)
- [ ] Career.md
- [ ] Job-Search.md
- [ ] Resume.md
- [ ] LinkedIn-Strategy.md
- [ ] Portfolio.md
- [ ] Certifications.md
- [ ] Education.md
- [ ] Business-Analyst-Path.md

### Tier 2 — Projects (6 notes)
- [ ] Projects.md
- [ ] AeroCardia.md
- [ ] Bonolo-Book-Marketing.md
- [ ] PM-Portfolio.md
- [ ] Ministry-Return.md
- [ ] Local-Business-AI-Services.md

### Knowledge Domains (17 notes)
- [ ] Knowledge-Index.md
- [ ] All AI-Systems sub-notes (4)
- [ ] All Brand sub-notes (3)
- [ ] All Marketing sub-notes (3)
- [ ] All Technology sub-notes (3)
- [ ] All Finance sub-notes (3)

### Index Notes (5 notes)
- [ ] SOPs-Index.md
- [ ] Agents-Index.md
- [ ] Templates-Index.md
- [ ] Archive-Index.md
- [ ] Reference-Index.md

**Success criteria:** All 54 master notes exist with proper structure and wiki-links.

---

## Phase 5: Migrate Knowledge Content

**Duration:** 45 minutes
**Risk:** Medium (moving operational knowledge)
**Reversible:** Yes (originals preserved until verified)

1. **Migrate SOPs** from `Knowledge_Base/SOPs/` and `AI_Agents/09_SOPs/`:
   - Update each to the new SOP template
   - Place in appropriate `07-SOPs/` subdirectory
   - Link from `SOPs-Index.md`

2. **Migrate agent profiles** from `AI_Agents/`:
   - Create agent notes in `08-Agents/`
   - Link from `Agents-Index.md`

3. **Migrate brand content** from `BRAND/` and `BRAND-SYSTEM/`:
   - Consolidate into `09-Knowledge/Brand/`
   - Eliminate duplicates

4. **Migrate project documentation** from `PROJECTS/`:
   - Move into `06-Projects/`
   - Create project master notes linking to existing documentation

5. **Migrate career content** from `JOB-SEARCH/`:
   - Move into `05-Career/`
   - Link from career master notes

**Success criteria:** All operational knowledge migrated. Each piece reachable from its domain master note.

---

## Phase 6: Archive Dead Weight

**Duration:** 30 minutes
**Risk:** Low (archiving, not deleting)
**Reversible:** Yes (all files in 10-Archive/)

1. **Archive `ABOUT ME/`** (5,725 files):
   - Move to `10-Archive/ChatGPT-Exports/`
   - Add entry to `Archive-Index.md`

2. **Archive Claude skills** (106 files):
   - Move to `10-Archive/Legacy-Skills/`
   - Keep only skills already ported to OpenCode

3. **Archive Claude agents** (10 files):
   - Move to `10-Archive/Legacy-Agents/`

4. **Archive Claude commands** (93 files):
   - Move to `10-Archive/Legacy-Commands/`

5. **Archive Claude rules** (16 files):
   - Move to `10-Archive/Legacy-Rules/`

6. **Archive staging content**:
   - `CYBERSECURITY-SKILLS-STAGING/` → `10-Archive/Staging/`

7. **Archive deprecated projects**:
   - Move inactive projects to `10-Archive/Deprecated-Projects/`

**Success criteria:** 89% dead weight removed from active knowledge surface. All archived content indexed and recoverable.

---

## Phase 7: Integrate with OpenCode

**Duration:** 20 minutes
**Risk:** Medium (modifying CLAUDE.md and agent files)
**Reversible:** Yes (back up original CLAUDE.md and agent files)

1. **Update CLAUDE.md**:
   - Remove personal context (moved to vault)
   - Remove duplicate rule content (moved to vault)
   - Add vault integration section per MEMORY_INTEGRATION_PLAN.md
   - Add session start/end workflow instructions

2. **Update agent .md files** (23 files):
   - Add memory integration instruction to each:
     ```
     ## Memory
     Read relevant vault notes before acting. Report to CEO for daily note integration.
     ```

3. **Decommission scattered systems**:
   - Archive `Knowledge_Base/` directory
   - Archive `AI_Agents/00_System/Memory Bank/`
   - Remove `.claude/rules/` (moved to archive)

4. **Decommission claude-mem** (if still offline):
   - Disable the MCP server in opencode.json
   - Document in `10-Archive/`

**Success criteria:** OpenCode reads vault at startup. CLAUDE.md is clean. Agent files reference vault.

---

## Phase 8: Verify and Test

**Duration:** 20 minutes
**Risk:** Zero (verification only)
**Reversible:** N/A

1. **Structural verification:**
   - All 12 folders exist
   - All 54 master notes exist
   - All wiki-links resolve (no broken links)

2. **Functional verification:**
   - OpenCode starts a session and reads `Home.md`
   - OpenCode follows wiki-links to an active project
   - OpenCode writes today's daily note
   - OpenCode updates a project note

3. **Rollback verification:**
   - Pre-migration checkpoint is intact
   - All archived files are recoverable from `10-Archive/`

**Success criteria:** All verifications pass. System operates from vault.

---

## Timeline

| Phase | Duration | Cumulative |
|---|---|---|
| Phase 0: Safety Checkpoint | 5 min | 5 min |
| Phase 1: Create Vault Structure | 10 min | 15 min |
| Phase 2: Migrate Personal Context | 15 min | 30 min |
| Phase 3: Migrate Existing Obsidian | 15 min | 45 min |
| Phase 4: Create Master Notes | 60 min | 1h 45min |
| Phase 5: Migrate Knowledge Content | 45 min | 2h 30min |
| Phase 6: Archive Dead Weight | 30 min | 3h |
| Phase 7: Integrate with OpenCode | 20 min | 3h 20min |
| Phase 8: Verify and Test | 20 min | 3h 40min |
| **Total estimated migration** | **~4 hours** | |

---

## Rollback Plan

If migration causes issues at any phase:

1. **Stop.** Do not continue to the next phase.
2. **Identify the phase where the issue occurred.**
3. **Restore from the pre-migration checkpoint** (`PRE-VAULT-MIGRATION-2026-06-21.zip`).
4. **Or restore individual directories** from `10-Archive/` since nothing is deleted.

---

## Post-Migration State

| Metric | Before | After |
|---|---|---|
| Knowledge locations | 5 scattered systems | 1 vault |
| Active skill definitions | 182 (both systems) | 76 (OpenCode only) |
| Active agent definitions | 33 (both systems) | 16 (OpenCode only) |
| Active knowledge files | ~686 (scattered) | ~200 (organized) |
| Dead weight indexed | ~17,000 files | 0 (all archived) |
| Duplicate files | 50+ | 0 |
| Daily note consistency | Inconsistent | Enforced |
| Session startup context | Manual from user | Automatic from vault |

---

## Recommended Migration Path and Expected Impact on Agent Performance

### Recommended Path
Execute the phases in order. Do not skip phases. Each phase builds on the previous. If time is limited, Phase 0-3 can run in one session (~45 minutes) and deliver immediate value: a centralized vault with personal context and daily notes. Phases 4-6 add depth. Phases 7-8 wire it into OpenCode.

### Expected Impact

**Context Retrieval:** Dramatic improvement. OpenCode currently starts sessions with zero awareness of project state. After migration, it reads `Home.md`, follows wiki-links to active projects, reads yesterday's daily note, and loads all relevant SOPs — all without user input. Session startup context goes from "whatever the user types" to "the entire vault graph."

**Decision Quality:** Moderate improvement. Master notes capture past decisions with rationale. SOPs enforce proven processes. When OpenCode knows what was decided and why, it makes better recommendations.

**Continuity Across Sessions:** Transformational. Currently, each session is an island. After migration, any session can read yesterday's daily note and immediately understand what was worked on, what was decided, and what needs follow-up. Multiple concurrent sessions can coordinate through shared vault writes.

**Memory Bloat:** Massive reduction. 89% of indexed files are dead weight. After migration, the active knowledge surface shrinks from ~19,000 files to ~200 well-organized notes. OpenCode spends fewer tokens scanning irrelevant files.

**Agent Independence:** Model providers become truly swappable. The knowledge system is plain markdown files. No vector database. No proprietary memory format. Any model that can read files can access the vault. This fulfills the core philosophy: models are replaceable, the knowledge system is permanent.

**Risk:** Low throughout. Every phase archives instead of deleting. A pre-migration checkpoint exists. Individual phases can be rolled back independently. The existing OpenCode configuration (opencode.json, agent files, providers) is not modified until Phase 7, and even then, the changes are additive (new instructions, not removal of existing ones).

---

This plan is complete and ready for review. No files have been moved or modified. All 7 planning documents are ready at the workspace root.
