# Agents & Skills Audit — Titus Banks AI OS

Date: 2026-06-16

## Executive Summary

Your system has a large multi-agent / multi-skill setup across OpenCode, Claude Code, Goose-style `.agents`, workspace HyperFrames skills, and Fable 5 behavior skills.

The setup is powerful, but it has overlap and duplication. The best move is not to delete aggressively; it is to keep one primary operating layer and archive/consolidate duplicates over time.

Recommended primary stack:

1. **OpenCode as the active command center / CEO-agent runtime**
2. **Claude Code skills as the broad specialist skill library**
3. **Workspace `.agents/skills` for project-specific media/HyperFrames work**
4. **`~/.agents/skills` for reusable Titus personal/business workflows**
5. **Fable 5 behavior skills as guardrails, not product features**

## Agent Inventory

### 1. OpenCode Agents — Active Primary Agents

Location:

`C:\Users\tbank\.config\opencode\agent`

Count: **23 markdown agent files**

Primary config:

`C:\Users\tbank\.config\opencode\opencode.json`

Default agent: **ceo**

These appear to be your current active OpenCode subagents. They operate through OpenCode's agent/task routing. The CEO agent is the primary orchestrator and delegates work to specialized subagents.

| Agent | Role / Purpose | Keep? | Notes |
|---|---|---:|---|
| ceo | Primary orchestrator, delegates work, coordinates results | Keep | Core default agent |
| project-manager | Task breakdown, planning, timelines | Keep | Useful for large projects |
| research | Web research and synthesis | Keep | Core research role |
| engineer | Coding, debugging, feature work | Keep | Core build role |
| qa | Testing, bug finding, quality review | Keep | Core verification role |
| browser | Browser automation and scraping | Keep | Approval-gated for sensitive actions |
| documentation | READMEs, docs, guides | Keep | Useful for productizing projects |
| automation | PowerShell, Windows ops, scheduled tasks | Keep with caution | High-power local ops |
| file-ops | File organization and cleanup | Keep with caution | Approval needed before delete/move |
| gmail-ops | Gmail labels, inbox automation | Keep with caution | External account actions require approval |
| github-ops | GitHub commits, PRs, issues | Keep with caution | No commits/pushes without approval |
| linkedin-jobs | Job search, LinkedIn automation | Keep with caution | Messaging/applying requires approval |
| workflow-orchestrator | Trigger → AI → execute → notify chains | Keep | Good fit for Command Center workflows |
| reasoning | Strategic analysis, decision support | Keep | Useful for major decisions |
| content-director | Content planning, scripts, newsletters | Keep | Useful for content-income system |
| product-manager | Product specs, courses, launches | Keep | Useful for Business Suite/product work |
| exec-ceo | Executive strategy | Keep | Could overlap with ceo; keep as specialist |
| exec-coo | Ops/SOP/workflow design | Keep | Useful for operations |
| exec-cfo | Budget/forecast/pricing | Keep | Useful for business ops |
| exec-cto | Architecture/security/tool evaluation | Keep | Useful technical reviewer |
| exec-cmo | Marketing/funnel/growth | Keep | Useful for campaigns |
| exec-cdo | Design/creative direction | Keep | Useful for UI/branding |
| faith-mission | Faith/mission alignment | Keep | Distinct values review role |

### 2. Claude Code Agents

Location:

`C:\Users\tbank\.claude\agents`

Count: **69 agent files**

These are available to Claude Code as local subagents. They are more granular than OpenCode's 23 agents and cover language-specific reviews, security, homelab/networking, sales, marketing, and specialized workflows.

Representative categories:

- Architecture/code: `architect`, `code-architect`, `code-explorer`, `code-reviewer`, `code-simplifier`, `refactor-cleaner`
- Build/test: `build-error-resolver`, `e2e-runner`, `pr-test-analyzer`, `tdd-guide`
- Language reviewers: Python, TypeScript, React, Go, Rust, Java, Kotlin, Swift, C++
- Security/compliance: `security-reviewer`, `healthcare-reviewer`, `opensource-sanitizer`
- Network/homelab: `network-architect`, `network-config-reviewer`, `network-troubleshooter`, `homelab-architect`
- Sales/marketing: `sales-company`, `sales-contacts`, `sales-competitive`, `sales-opportunity`, `sales-strategy`, `marketing-agent`, `seo-specialist`
- Specialized: `gan-*`, `mle-reviewer`, `performance-optimizer`, `chief-of-staff`, `loop-operator`

Recommendation: **Keep**, but use them only when Claude Code is the active runtime. Do not try to mirror every Claude agent into OpenCode.

### 3. Architecture / Prompt Docs

These are reference docs, not necessarily executable agents:

- `TITUS-BANKS-8-AGENT-OPERATING-ARCHITECTURE.md`
- `TITUS-BANKS-EXECUTIVE-AGENT-PROMPTS.md`
- Goose/Hermes setup docs
- Hermes `AGENTS.md`

Recommendation: **Keep as documentation**, but do not treat them as the source of truth for runtime. Runtime source of truth should be:

1. `~/.config/opencode/agent`
2. `~/.config/opencode/opencode.json`
3. `~/.claude/agents`

## Skill Inventory

### 1. OpenCode Skills

Location:

`C:\Users\tbank\.config\opencode\skills`

Count: **79 skill folders**

This is your main OpenCode skill library. OpenCode config points here, so these are the most relevant for your current CEO-agent workflow.

Representative skills found:

- `ai-inspiration`
- `business-ops-experts`
- `career-ops`
- `desktop-automation`
- `doc-coauthoring`
- `file-organization`
- `findskills`
- `gmail-automation`
- `identity-eraser`
- `internal-comms`
- `learning-extractor`
- `local-ai`
- `local-llm-router`
- `mcp-builder`
- `memory-optimization`
- `marketing-skills`
- `project-radar`
- `system-cleanup`
- `windows-automation`
- `workflow-orchestration`

Recommendation: **Keep most of these**, because this is your active skill runtime.

### 2. Claude Skills

Location:

`C:\Users\tbank\.claude\skills`

Count: **128 skill folders**

Additional plugin/cache skills:

`C:\Users\tbank\.claude\plugins`

Count: **34 skill/plugin files**

These are broad and powerful. They include coding patterns, GSAP skills, research/Feynman skills, security, graphify, personal AI operator, business ops, and more.

Recommendation: **Keep**, but periodically prune unused experimental skills only after confirming they are not referenced by active workflows.

### 3. Workspace `.agents` Skills

Location:

`C:\Users\tbank\Desktop\Live Cowork\.agents\skills`

Count: **16 skill folders**

Primary focus:

- HyperFrames video/composition skills
- Animation adapters: GSAP, Anime.js, CSS, Lottie, Three.js, TypeGPU, WAAPI, Tailwind
- Website-to-video workflows
- Book access workflow

Recommendation: **Keep**. These are project-specific and useful for video/landing/media work.

### 4. Fable 5 Behavior Skills

Location:

`C:\Users\tbank\Desktop\Live Cowork\fable5-skills\skills`

Count: **10 skill folders**

Skills:

- `act-when-ready`
- `autonomous-continuation`
- `effort-calibrator`
- `grounded-progress`
- `markdown-memory`
- `no-gold-plating`
- `regrounding-summary`
- `scope-guard`
- `skill-refactorer`
- `subagent-orchestration`

Recommendation: **Keep**. These are guardrails that fix common high-effort agent behavior issues.

### 5. User `.agents` Skills

Location:

`C:\Users\tbank\.agents\skills`

Count: **20 skill folders**

Observed skills:

- `book-access-workflow`
- `book-launch`
- `brand-guidelines`
- `browser-automation`
- `career-ops`
- `doc-coauthoring`
- `file-organization`
- `gmail-automation`
- `identity-credit`
- `identity-eraser`
- `internal-comms`
- `learning-extractor`
- `local-ai`
- `mcp-builder`
- `project-radar`
- `review-lead-recovery`
- `system-cleanup`
- `titus-banks-brand`
- `windows-automation`
- `workflow-orchestration`

Recommendation: **Keep as reusable personal/business skills**, but many duplicate OpenCode skills. Decide whether this is a Goose/shared skill folder or an active runtime folder.

### 6. Skill Store

Location:

`C:\Users\tbank\Desktop\Live Cowork\skill-store`

Direct skill count: **0 direct `SKILL.md` folders**

Important files:

- `SKILL-INDEX.md`
- `README.md`
- `install-skill.ps1`
- `index.html`
- `auditor.html`

Finding: The index appears stale/incomplete compared with the actual OpenCode skill folder.

Recommendation: **Keep but update**. Do not use it as the current source of truth until it is regenerated.

## Duplicate / Overlap Audit

### Clear duplicates across locations

These skills appear in multiple places or have overlapping purpose:

- `book-access-workflow`
- `browser-automation`
- `career-ops`
- `doc-coauthoring`
- `file-organization`
- `gmail-automation`
- `identity-eraser`
- `internal-comms`
- `learning-extractor`
- `local-ai`
- `mcp-builder`
- `project-radar`
- `system-cleanup`
- `windows-automation`
- `workflow-orchestration`
- `brand-guidelines`

This is not automatically bad. It usually means the same workflow was installed for multiple runtimes: OpenCode, Goose, Claude, and workspace-local.

Risk: Medium. Duplicate skills can diverge and produce inconsistent behavior.

Recommendation: Pick a primary source per skill:

- For active OpenCode: `~/.config/opencode/skills`
- For shared Goose-style skills: `~/.agents/skills`
- For project-specific skills: workspace `.agents/skills`
- For Claude Code behavior/research: `~/.claude/skills`

## Keep / Consolidate / Remove Recommendations

## Keep

Keep these as core system layers:

1. `~/.config/opencode/agent` — active OpenCode agent team
2. `~/.config/opencode/skills` — active OpenCode skills
3. `~/.claude/agents` — Claude Code specialist subagents
4. `~/.claude/skills` — Claude Code skills
5. Workspace `.agents/skills` — HyperFrames/media/project-specific skills
6. `fable5-skills` — behavior guardrails
7. `~/.agents/skills/learning-extractor` — already useful for Facebook Reel captures
8. `project-radar`, `business-ops-experts`, `personal-ai-operator`, `windows-automation`, `workflow-orchestration` — key for your Command Center direction

## Consolidate / Update

These should be cleaned up or made source-of-truth consistent:

1. `skill-store/SKILL-INDEX.md`
   - Current index is stale versus actual installed skills.
   - Action: regenerate index from `~/.config/opencode/skills` and `~/.agents/skills`.

2. Duplicate user skills between:
   - `~/.config/opencode/skills`
   - `~/.agents/skills`
   - `.claude/skills`

   Action: Make a spreadsheet/report with columns: skill name, locations, last modified, primary runtime, keep/archive.

3. Executive prompt docs vs OpenCode agents
   - If `exec-cfo`, `exec-cto`, etc. are finalized in OpenCode, keep docs as archive/reference only.

4. Goose/Hermes docs
   - Keep while Hermes gateway is running, but mark which docs are current vs historical.

## Remove / Archive Candidates

Do not delete immediately. Archive first.

1. Stale duplicated skills that have newer equivalents in `~/.config/opencode/skills`
   - Risk: Medium if deleted blindly.
   - Action: compare timestamps and content before removal.

2. Old setup docs that no longer match current runtime
   - Examples: older Goose/OpenClaw setup guides, if replaced by Hermes/OpenCode runtime.
   - Recommendation: move to `ARCHIVE/old-agent-setups/`.

3. Failed partial clone of Antigravity skills inside the learning capture repositories folder
   - You have a successful clone at `C:\Users\tbank\Desktop\ag-skills`.
   - The partial failed checkout in the capture folder can be removed later after confirmation.

4. Experimental/high-risk automation skills if unused
   - `identity-eraser`, `desktop-automation`, `gmail-automation`, `linkedin-jobs`, `github-ops`, `system-cleanup`, `windows-automation`
   - These are powerful; keep only if you actively use them and keep approval gates.
   - Recommendation: keep installed but do not auto-run. Require explicit approval for destructive/external actions.

## Risk Audit

### High-power skills/agents that require approval gates

- `windows-automation`
- `desktop-automation`
- `file-organization`
- `system-cleanup`
- `gmail-automation`
- `linkedin-jobs`
- `github-ops`
- `identity-eraser`
- `workflow-orchestrator`
- `browser-automation`

Rules to keep:

- No deleting files without approval
- No sending emails/messages/DMs without approval
- No connecting accounts without approval
- No spending money or deploying cloud resources without approval
- No force push / Git destructive operations without approval

## Recommended Operating Model

### Daily use

Use OpenCode CEO agent as the front door:

1. CEO receives request
2. CEO chooses skill or subagent
3. Specialized subagent executes
4. QA/verification checks output
5. CEO reports back

### Skills

Use skills as workflow instructions, not as always-on processes.

### Command Center

Command Center should become the visible control surface for:

- Gateway start/stop
- Bot status
- Learning captures
- Repository Radar
- Skill Inbox
- Project Radar
- DocFlow / CRM launchers

## Immediate Next Steps

1. Create `AGENT-SKILL-REGISTRY.csv` with:
   - name
   - type: agent/skill
   - runtime: OpenCode/Claude/Goose/workspace
   - path
   - status: active/reference/archive
   - risk level
   - keep/consolidate/remove

2. Update `skill-store/SKILL-INDEX.md` from the real installed skill folders.

3. Add a Command Center tab/button for:
   - Agent Inventory
   - Skill Inventory
   - Learning Inbox
   - Repository Radar

4. Do not delete any agent or skill yet. First archive duplicates after a diff review.

## Bottom Line

You have a strong but crowded AI OS. The active core should be:

- **OpenCode CEO + 23 OpenCode agents** for execution
- **OpenCode skills** for daily workflows
- **Claude skills/agents** for advanced specialist work
- **Workspace skills** for HyperFrames/media projects
- **Fable 5 guardrails** to prevent over-planning, gold-plating, and unsafe scope creep

Main cleanup need: consolidate duplicates and regenerate the skill index. Removal should be conservative and approval-gated.
