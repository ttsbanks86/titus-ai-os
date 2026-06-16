# AI OS Platform Separation + Persistent Brain Plan

Date: 2026-06-16
Owner: Titus Banks
Purpose: Separate OpenCode, Goose/.agents, and Claude/Cloud systems so each can run standalone, reduce duplicate skills/agents, and create a persistent side-brain that survives long conversations and new sessions.

---

## 1. Current Problem

The AI OS is powerful but crowded. Several tools overlap:

- OpenCode agents and skills
- Claude Code agents and skills
- Goose-style `.agents/skills`
- Hermes/OpenClaw gateway files
- Workspace project-specific skills
- Fable 5 behavior guardrail skills
- Newly cloned external skill/repo inspirations

This caused repeated friction:

1. Bot setup confusion between Telegram, Hermes, OpenClaw, and OpenCode Go API.
2. Tokens were pasted in chat instead of isolated secret stores.
3. Agent/gateway used one bot while BotFather text referenced another.
4. Command Center rebuild failed because old EXE was still running and locking files.
5. DocFlow failed because of a recursive `show()` method.
6. Antigravity repo clone failed because Windows path length was too deep.
7. Skills were duplicated across multiple runtime folders.
8. The skill-store index was stale compared to real installed skills.
9. Long conversations required too much re-explaining because memory was not consolidated into a side-brain.

The fix is separation + registry + persistent memory.

---

## 2. Target Architecture

### A. OpenCode Standalone System

OpenCode should be the main active execution system.

Primary folders:

- `C:\Users\tbank\.config\opencode\opencode.json`
- `C:\Users\tbank\.config\opencode\agent`
- `C:\Users\tbank\.config\opencode\skills`

Role:

- Main CEO-agent interface
- Local project execution
- Coding, QA, browser, file ops, automation
- Command Center integration
- Workflow orchestration

OpenCode should NOT automatically load every Claude/Goose skill. It should have a curated set only.

Keep in OpenCode:

- `ceo`
- `engineer`
- `qa`
- `research`
- `browser`
- `automation`
- `file-ops`
- `github-ops`
- `gmail-ops`
- `workflow-orchestrator`
- `project-manager`
- `reasoning`
- `documentation`
- executive agents: CEO/COO/CFO/CTO/CMO/CDO/Faith
- `learning-extractor`
- `project-radar`
- `business-ops-experts`
- `windows-automation`
- `workflow-orchestration`
- `memory-optimization`
- `mcp-builder`
- `local-ai`
- `personal-ai-operator` if installed

Archive or keep outside OpenCode:

- Large experimental cloud/provider skills that are not used daily
- Duplicate Goose-only versions
- Old OpenClaw/Hermes migration skills unless needed
- UI/media-only project skills unless OpenCode actively uses them

### B. Goose / .agents Standalone System

Goose-style skills should live in:

- `C:\Users\tbank\.agents\skills`

Role:

- Reusable personal workflows
- Lightweight skills that can be used by multiple tools
- No giant duplicate library
- No OpenCode-specific config

Keep in Goose:

- `learning-extractor`
- `titus-banks-brand`
- `book-launch`
- `identity-credit`
- `review-lead-recovery`
- `browser-automation`
- `file-organization`
- `gmail-automation`
- `windows-automation`
- `workflow-orchestration`
- `project-radar`

Remove/archive from Goose if duplicated and not needed:

- Any skill that only belongs in OpenCode or Claude Code
- Old skill versions with weaker instructions

### C. Claude / Cloud Standalone System

Claude Code should keep its advanced specialist library.

Primary folders:

- `C:\Users\tbank\.claude\agents`
- `C:\Users\tbank\.claude\skills`
- `C:\Users\tbank\.claude\CLAUDE.md`

Role:

- Specialist code review
- Research/paper workflows
- Security audits
- Pattern libraries
- Graphify/Obsidian/deep memory
- Advanced Claude-specific workflows

Keep in Claude:

- Feynman/research skills
- GSAP/animation specialists
- coding pattern skills
- security-scan/security-review
- context-budget
- obsidian-mind
- markdown-memory
- strategic-compact
- regrounding-summary
- grounded-progress
- subagent-orchestration
- skill-refactorer

Do not force all Claude skills into OpenCode. Keep Claude as a separate specialist environment.

### D. Workspace Project Skills

Workspace-specific skills live here:

- `C:\Users\tbank\Desktop\Live Cowork\.agents\skills`

Role:

- HyperFrames
- Video/animation
- website-to-hyperframes
- GSAP adapters
- Tailwind/Three/Lottie/WAAPI/TypeGPU
- project-specific media workflows

Keep these here. Do not mix them into global OpenCode unless they are needed globally.

---

## 3. Troubleshooting Lessons → Required Guardrail Skills

Based on the issues we hit, these skills/guardrails should stay active:

### 1. Scope Guard

Why: Prevents doing destructive work before confirmation.

Used for:

- deleting bot folders
- deleting old `.hermes` / `.openclaw`
- killing gateway processes
- cloud deploys

Status: Keep.

### 2. No Gold Plating

Why: Prevents overbuilding when user asks for a focused fix.

Used for:

- DocFlow recursion fix
- Command Center control buttons
- bot setup

Status: Keep.

### 3. Grounded Progress

Why: Prevents claiming work that was not actually done.

Used for:

- verifying DocFlow EXE rebuild
- verifying shortcut targets
- verifying Telegram token with getMe
- verifying repo clone status

Status: Keep.

### 4. Regrounding Summary

Why: Long sessions need final reports that make sense without hidden context.

Used for:

- Facebook learning capture report
- agent/skill audit
- execution reports

Status: Keep.

### 5. Memory Optimization

Why: Prevents repeated re-explaining.

Used for:

- persistent side-brain
- project registry
- troubleshooting lessons

Status: Keep.

### 6. Obsidian Mind

Why: Local durable memory layer independent of any single chat.

Used for:

- daily session notes
- linked project notes
- troubleshooting archive
- system registry

Status: Keep and implement.

### 7. Project Radar

Why: User wants to say “continue this project” and have context ready.

Used for:

- active project status
- next actions
- project owners
- dependencies

Status: Keep.

### 8. Learning Extractor

Why: User sends videos/links and wants extraction + implementation decisions.

Used for:

- Facebook Reels capture
- repo radar
- skill inspiration intake

Status: Keep.

### 9. Verification Loop / QA

Why: Every build must be tested, compiled, or verified.

Used for:

- `py_compile`
- PyInstaller rebuilds
- shortcut verification
- token getMe checks

Status: Keep.

---

## 4. Skills to Keep in OpenCode Core

OpenCode should be lean and practical. Recommended core skills:

### Execution / Local Ops

- `windows-automation`
- `desktop-automation`
- `browser-automation`
- `file-organization`
- `workflow-orchestration`
- `verification-loop`
- `tdd-workflow`
- `security-review`
- `mcp-builder`

### Memory / Project Continuity

- `memory-optimization`
- `project-radar`
- `learning-extractor`
- `obsidian-mind` if OpenCode can access it, otherwise keep Claude-side and mirror summaries
- `markdown-memory`

### Business / Daily Work

- `business-ops-experts`
- `career-ops`
- `internal-comms`
- `gmail-automation`
- `marketing-skills`
- `content-scheduling`
- `titus-banks-brand` or `brand-guidelines`

### Build / Design

- `web-artifacts-builder`
- `figma`
- `ux-design-systems`
- `local-ai`
- `local-llm-router`

### Guardrails

- `scope-guard`
- `no-gold-plating`
- `grounded-progress`
- `regrounding-summary`
- `act-when-ready`
- `subagent-orchestration`

---

## 5. Skills to Keep Outside OpenCode

### Claude-only / specialist skills

Keep in Claude, not OpenCode:

- Feynman paper/research skills
- GSAP plugin deep skills
- coding pattern skills if OpenCode already has simpler equivalents
- peer-review/literature-review/research-heavy skills
- context-budget/token-budget advisor

### Workspace-only skills

Keep under workspace `.agents/skills`:

- HyperFrames
- HyperFrames CLI/media/registry
- GSAP/Anime/Lottie/Three/WAAPI/TypeGPU adapter skills
- website-to-hyperframes
- remotion-to-hyperframes

### Goose-only reusable personal workflows

Keep under `~/.agents/skills`:

- book-access-workflow
- learning-extractor
- identity-credit
- review-lead-recovery
- titus-banks-brand
- book-launch

---

## 6. Archive Candidates

Do not delete yet. Archive first.

### Archive old docs / stale setups

Potential archive target:

`C:\Users\tbank\Desktop\Live Cowork\ARCHIVE\old-agent-setups`

Move later after review:

- old Goose/OpenClaw setup docs that no longer match active runtime
- duplicate setup reports
- failed partial repo clone from Antigravity inside learning capture folder

### Archive duplicate skills

Create a duplicate report first. Do not remove blindly.

Duplicates to inspect:

- `learning-extractor`
- `browser-automation`
- `file-organization`
- `gmail-automation`
- `windows-automation`
- `workflow-orchestration`
- `career-ops`
- `doc-coauthoring`
- `brand-guidelines`
- `local-ai`
- `mcp-builder`

Rule:

- Keep newest/most specific version in active runtime
- Archive older duplicate to `ARCHIVE/skills/<runtime>/<skill-name>`
- Keep a pointer file noting replacement

---

## 7. Persistent Side-Brain Architecture

The side-brain should not depend on one chat. It should have four layers.

### Layer 1: Obsidian Vault

Purpose: Human-readable long-term project memory.

Suggested folder:

`C:\Users\tbank\Desktop\Live Cowork\OBSIDIAN-AI-OS`

Suggested structure:

```text
OBSIDIAN-AI-OS/
  00-Dashboard.md
  01-Projects/
    Command-Center.md
    DocFlow.md
    Hermes-Gateway.md
    Business-Suite.md
    Learning-Captures.md
  02-Agents/
    OpenCode-Agent-Team.md
    Claude-Agent-Team.md
    Goose-Skills.md
  03-Skills/
    Skill-Registry.md
    Skill-Duplicates.md
    Skill-Archive-Queue.md
  04-Troubleshooting/
    Bot-Setup-Mismatch.md
    DocFlow-Recursion.md
    Command-Center-Build-Lock.md
    Windows-Git-Path-Length.md
    Token-Safety.md
  05-Decisions/
    Platform-Separation.md
    Memory-Architecture.md
  06-Daily-Logs/
```

### Layer 2: Markdown Memory

Purpose: Machine-friendly, compact lessons that agents read first.

Suggested file:

`C:\Users\tbank\Desktop\Live Cowork\AI-OS-GOVERNANCE\LESSONS.md`

Example lessons:

- Always verify shortcut target after rebuild.
- Do not paste or reuse leaked tokens for 24/7 deployment.
- For Windows repo clones, use short paths for large repos.
- When PyInstaller fails with permission denied, check for running EXE lock.
- For Qt/PySide recursion errors, inspect overridden methods like `show()`.

### Layer 3: Agent/Skill Registry

Purpose: structured source of truth.

Suggested file:

`C:\Users\tbank\Desktop\Live Cowork\AI-OS-GOVERNANCE\AGENT-SKILL-REGISTRY.csv`

Columns:

```text
name,type,runtime,path,status,risk,keep_action,notes,last_reviewed
```

Status values:

- active
- reference
- duplicate
- archive-candidate
- archived

Runtime values:

- opencode
- claude
- goose
- workspace
- docs

### Layer 4: claude-mem / corpora

Purpose: searchable memory retrieval across sessions.

Recommended corpora:

1. `ai-os-troubleshooting`
2. `ai-os-projects`
3. `agent-skill-registry`
4. `business-suite`
5. `learning-captures`

Workflow:

- At end of major work, write Markdown summary.
- Add concise memory observation.
- Update registry.
- Update Command Center status.

---

## 8. Command Center Integration

Command Center should become the visual control surface for the AI OS.

Recommended new sections:

### Agent Inventory

Shows:

- OpenCode agents
- Claude agents
- Goose workflows
- status: active/reference/archive

### Skill Inventory

Shows:

- skill name
- runtime
- duplicate count
- keep/archive action
- risk level

### Troubleshooting Brain

Shows:

- known issue
- cause
- fix
- related project
- last verified date

### Project Continuity

Shows:

- project name
- last worked date
- current status
- next action
- relevant files

### Learning Inbox

Shows:

- captured video/link
- extracted lesson
- saved repo/site
- adoption decision

---

## 9. Implementation Phases

### Phase 1 — Do Not Delete, Build Registry

1. Create `AI-OS-GOVERNANCE` folder.
2. Create agent/skill registry CSV.
3. Create lessons file.
4. Create platform separation plan.
5. Mark duplicates, but do not move yet.

### Phase 2 — Separate Standalone Systems

1. OpenCode: curated `~/.config/opencode/skills` and `agent` team.
2. Goose: reusable personal workflows in `~/.agents/skills` only.
3. Claude: specialist agents/skills remain under `.claude` only.
4. Workspace: project-specific skills remain under workspace `.agents` only.

### Phase 3 — Archive Duplicates

1. Compare duplicate skills.
2. Keep primary version.
3. Move old versions to archive.
4. Add pointer files.
5. Update registry.

### Phase 4 — Side-Brain Activation

1. Create Obsidian AI OS vault.
2. Add project notes.
3. Add troubleshooting notes.
4. Add daily/session logs.
5. Configure OpenCode/Claude to read governance summaries at startup.

### Phase 5 — Command Center Integration

1. Add tabs for Agent Inventory, Skill Inventory, Project Radar, Learning Inbox.
2. Add buttons to open registry and Obsidian vault.
3. Add status indicators for gateway, bot, DocFlow, CRM, repo radar.

---

## 10. Immediate Next Actions

Recommended next step for execution:

1. Create `AGENT-SKILL-REGISTRY.csv`.
2. Create `LESSONS.md` from the troubleshooting patterns.
3. Create Obsidian vault structure.
4. Add Command Center buttons to open these governance files.
5. Only after that, start archiving duplicates.

Do not delete anything yet.

---

## 11. Final Recommendation

Your system should not become one giant merged AI folder. It should become three clean standalone systems connected by one memory/registry layer:

- OpenCode = daily operator and execution layer
- Goose/.agents = reusable personal workflow layer
- Claude/Cloud = specialist research/review/deep skill layer
- Obsidian + markdown registry = persistent side-brain
- Command Center = visual control panel

This gives you the ability to start any new conversation and say:

> Continue DocFlow.
> Continue Command Center.
> Continue bot/gateway.
> Continue learning capture.

And the system can pull the project note, registry, troubleshooting history, and next actions without you re-explaining everything.
