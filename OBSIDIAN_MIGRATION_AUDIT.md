# Obsidian Migration Audit

**Audit Date:** 2026-06-21
**Scope:** Full filesystem sweep of Live Cowork workspace, OpenCode config, Claude config, and memory stores
**Status:** Audit complete. No files moved or modified.

---

## Executive Summary

The current knowledge system spans three separate locations with 182 skill definitions, 33 agent profiles, 115 commands, and ~686 user-authored markdown files spread across dozens of directories. There are 19,112 total .md files in the workspace, but 89% of them are cloned repositories or ChatGPT chat exports that provide no active value. The system has grown organically without cleanup, resulting in significant duplication, dead weight, and retrieval friction.

**Key numbers:**
- 19,112 total .md files (89% dead weight)
- ~686 user-authored knowledge files
- 182 skill definitions across two systems
- 33 agent definitions across two systems
- 115 slash commands across two systems
- 16 rules files in Claude config
- 51 root-level loose files in workspace
- 5 separate memory/knowledge locations
- 3 copies of my-voice.md found
- 2 copies of my-context.md found

---

## 1. File System Inventory

### 1.1 Total .md File Count by Location

| Location | Count | Category |
|---|---|---|
| `C:\Users\tbank\Desktop\Live Cowork` (raw) | 22,895 | All files |
| Excluded (node_modules, .git) | -3,783 | Build artifacts |
| **Clean workspace total** | **19,112** | |
| LEARNING-CAPTURES (cloned repos) | 11,319 | Reference only |
| ABOUT ME (ChatGPT vault exports) | 5,725 | Chat history archives |
| hermes-source (open-source project) | 1,352 | Reference code docs |
| **True user-authored content** | **~686** | Actionable knowledge |
| `C:\Users\tbank\.config\opencode\` | 122 | Skills + agents + commands |
| `C:\Users\tbank\.claude\` | 450 | Skills + agents + commands + rules |
| **Grand total (all locations)** | **~19,684** | |

### 1.2 Breakdown by Content Type

| Type | Count | Location |
|---|---|---|
| Root-level loose files | 51 | Live Cowork root |
| Business strategy docs | 40 | BRAND-SYSTEM |
| Agent system docs | 41 | AI_Agents |
| SOPs & workflows | 22 | Knowledge_Base, AI_Agents, Commands |
| Project documentation | 73 | PROJECTS |
| Career/job search | 10 | JOB-SEARCH |
| Brand & content | 19 | BRAND, CONTENT-INCOME-SYSTEM |
| Book marketing | 36 | BOOK-PROJECTS, BOOK-MARKETING-SYSTEM |
| Daily logs | 9 | OBSIDIAN-AI-OS |
| Governance & audits | ~15 | Root, AI-OS-GOVERNANCE |
| Technical projects | 74 | jcode-test |
| Cybersecurity staging | 57 | CYBERSECURITY-SKILLS-STAGING |
| Skills (OpenCode) | 76 | .config/opencode/skills |
| Skills (Claude) | 106 | .claude/skills |
| Agent definitions (OpenCode) | 23 | .config/opencode/agent |
| Agent definitions (Claude) | 10 | .claude/agents |
| Commands (OpenCode) | 22 | .config/opencode/commands |
| Commands (Claude) | 93 | .claude/commands |
| Rules (Claude) | 16 | .claude/rules |

### 1.3 Top-Level Workspace Directories (by file count, user-authored)

```
ROOT (51 loose .md files)
AI_Agents/              (41)
BRAND-SYSTEM/           (40)
BOOK-PROJECTS/          (27)
JOB-SEARCH/             (10)
OBSIDIAN-AI-OS/         (9 + structure)
Knowledge_Base/         (18)
BRAND/                  (19)
CONTENT-INCOME-SYSTEM/  (9)
PERSONAL-AI-OPERATOR/   (3)
PROJECTS/               (73)
CYBERSECURITY-SKILLS-STAGING/ (57)
BOOK-MARKETING-SYSTEM/  (9)
BUSINESS-SUITE/         (4)
Reports/                (5)
AI-OS-GOVERNANCE/       (4)
```

---

## 2. Duplicate Identification

### 2.1 File Duplicates

| File | Copies Found | Locations |
|---|---|---|
| my-voice.md | 3 | ROOT, ABOUT ME/, ABOUT ME/PROJECTS/TEMPLATES/OUTPUTS/... |
| my-context.md | 2 | ROOT (authoritative), ABOUT ME/ (stale copy) |
| AGENT_SYSTEM_REDESIGN_AUDIT.md | 2 | ROOT (latest), similar audit exists as MASTER_AGENT_SYSTEM_AUDIT.md |
| profile-pic.jpeg | 2 | ROOT (stale), Profile Pictures/ (current) |
| brand-voice references | multiple | BRAND/, BRAND-SYSTEM/, personal-ai-operator/, OBSIDIAN-AI-OS |

### 2.2 Skill Duplicates Across Systems

| Overlap Count | Skill Name | In Both OpenCode and Claude? |
|---|---|---|
| 40+ skills | analytics-metrics, aws-account-management, brand-voice, bun, business-ops-experts, career-ops, cloudflare, content-scheduling, deep-research, documentation-lookup, fal-ai, feynman-*, figma, git-master-discipline, github-trending, google-workspace-cli, honest-agent, langchain, learning-extractor, local-ai, local-llm-router, marketing-skills, memory-optimization, mermaid-diagrams, meta-ads, mobile-responsiveness, mongodb, nano-banana-pro, owasp-security, personal-ai-operator, railway, security-review, self-skill-builder, tdd-workflow, ux-design-systems, vercel, verification-loop, video-edit, web-accessibility, workflow-orchestration, x-twitter-scraper, youtube-autonomous, yuv-* | Yes (40+) |

**Conclusion:** ~55% of OpenCode skills are duplicates of Claude skills. Many are identically named. Neither set is canonical.

### 2.3 Agent Duplicates

| Agent | OpenCode (16 registered + 7 .md only) | Claude (10) | Duplicate? |
|---|---|---|---|
| CEO/strategic | ceo.md, exec-ceo.md, exec-cdo.md | architect.md, planner.md | Yes (5 files for similar role) |
| Engineering | engineer.md | code-reviewer.md, performance-optimizer.md, tdd-guide.md | Yes |
| Security | qa.md (covers security) | security-reviewer.md | Yes |
| Research | research.md | seo-specialist.md (some overlap) | Partial |
| Database | none | database-reviewer.md | Unique to Claude |
| Marketing | none | marketing-agent.md | Unique to Claude |
| Documentation | documentation.md | docs-lookup.md | Yes |
| Project mgmt | project-manager.md | none | Unique to OpenCode |
| Product mgmt | product-manager.md | none | Unique to OpenCode |
| Faith | faith-mission.md | none | Unique to OpenCode |

**Conclusion:** 5-7 agents are functionally duplicated across systems with overlapping responsibilities.

---

## 3. Memory Bloat Sources

### 3.1 Primary Bloat Sources

| Source | Size | Impact | Recommendation |
|---|---|---|---|
| ABOUT ME/ directory | 5,725 files | Massive. ChatGPT KnowledgeVault exports. Never referenced by agents. | Archive entire directory. Zero operational value. |
| LEARNING-CAPTURES/ | 11,319 files | Massive. Cloned repos for reference learning. | Keep as reference only. Do not index. |
| hermes-source/ | 1,352 files | Reference code. Already exists as webui. | Archive or flag as reference-only. |
| CYBERSECURITY-SKILLS-STAGING/ | 57 files | Staging content. Not yet deployed. | Consolidate or archive. |
| .claude/skills/ (Claude-only) | 106 skills | 106 SKILL.md files. System is OpenCode now, not Claude. | Archive Claude skills not ported to OpenCode. |
| .claude/commands/ | 93 commands | Most are Claude-specific workflow commands. | Archive unless ported to OpenCode. |
| .claude/agents/ | 10 agents | Claude-specific agent definitions. | Archive. OpenCode has its own agent system. |
| .claude/rules/ | 16 rules | Claude-specific rules. | Consolidate into vault memory rules. |

### 3.2 Agent Memory Bloat

| Agent System | Files | Current State |
|---|---|---|
| OpenCode agents | 23 .md files | 7 of 23 are executive agents not in opencode.json. 16 active. |
| Claude agents | 10 .md files | All inactive. System is OpenCode now. |
| Agent memory files | AI_Agents/00_System/Memory Bank/ | Separate memory system. Not integrated with vault. |

### 3.3 Knowledge Fragmentation

Knowledge is currently stored in 5 separate systems:
1. **Knowledge_Base/** — SOPs, workflows, templates (18 files)
2. **AI_Agents/00_System/** — Agent memory and workflow definitions (41 files)
3. **OBSIDIAN-AI-OS/** — Existing Obsidian vault with some structure (9+ files)
4. **.claude/rules/** — Claude-specific rules (16 files)
5. **Root-level files** — Plans, audits, strategy docs (51 files)

None of these systems talk to each other. None are consolidated.

---

## 4. Consolidation Opportunities

### 4.1 Content That Can Merge

| Content Type | Current Location(s) | Target Vault Location |
|---|---|---|
| Career docs | ROOT + JOB-SEARCH/ + AI_Agents/ | `05-Career/` |
| Business plans | ROOT + BRAND-SYSTEM/ + BRAND/ + PROJECTS/ | `03-Businesses/` |
| SOPs | Knowledge_Base/SOPs/ + AI_Agents/09_SOPs/ + Commands/Quality/ | `07-SOPs/` |
| Agent definitions | .config/opencode/agent/ (23) + .claude/agents/ (10) | `08-Agents/` |
| Personal context | my-context.md + my-rules.md + my-goals.md + my-voice.md | `01-Dashboard/` |
| Project docs | PROJECTS/ (73) + multiple root files | `06-Projects/` |
| Brand/voice | BRAND/ (19) + BRAND-SYSTEM/ (40) + ABOUT ME/ (duplicates) | `09-Knowledge/Brand/` |
| Daily logs | OBSIDIAN-AI-OS/06-Daily-Logs/ | `02-Daily-Notes/` |

### 4.2 Content That Can Be Archived

| Content | Reason |
|---|---|
| ABOUT ME/ (5,725 files) | ChatGPT exports. Zero operational value. |
| LEARNING-CAPTURES/ (11,319 files) | Reference repos. Flag as reference. Do not index. |
| .claude/skills/ (106 files) | System is OpenCode now. Archive Claude skills not ported. |
| .claude/agents/ (10 files) | Claude-only agents. System runs on OpenCode. |
| .claude/commands/ (93 files) | Claude-only commands. Not used. |
| CYBERSECURITY-SKILLS-STAGING/ (57 files) | Staging content. Archive or consolidate. |
| .agent-archive/ | Already archived. Leave as-is. |
| Legacy-Business-Assets/ | Already archived. Leave as-is. |
| Duplicate root files | Multiple versions of audit docs, strategy docs. Keep latest only. |

### 4.3 Skills That Need Deduplication

40+ skills are duplicated between `.config/opencode/skills/` and `.claude/skills/`. Only the OpenCode versions are active. The 106 Claude skills should either be:
- Ported to OpenCode if they have unique value
- Archived if the OpenCode version is sufficient

---

## 5. Current Active Systems

### 5.1 OpenCode (Canonical Runtime)

| Component | Count | Notes |
|---|---|---|
| Subagents (registered) | 16 | Defined in opencode.json |
| Agent .md files | 23 | 16 active + 7 executive extras |
| Skills | 76 | Registered in opencode.json |
| Commands | 22 | Active slash commands |
| Providers | 5 | anthropic, openai, ollama-local, ollama-cloud, opencodego |
| MCP Servers | 18 (12 enabled) | playwright, filesystem, memory, firecrawl, etc. |

### 5.2 Claude (Legacy, Frozen)

| Component | Count | Notes |
|---|---|---|
| CLAUDE.md | 1 | Philosophy document. Rewritten as OpenCode philosophy. |
| Skills | 106 | Frozen. Not actively used unless ported. |
| Agents | 10 | Frozen. Not actively used. |
| Commands | 93 | Frozen. Not actively used. |
| Rules | 16 | Frozen. |

### 5.3 Existing Obsidian Vault (Partial)

`C:\Users\tbank\Desktop\Live Cowork\OBSIDIAN-AI-OS\` already contains:
- `00-Dashboard.md` — current system dashboard
- `01-Projects/` — project notes
- `02-Agents/` — agent profiles
- `03-Skills/` — skill registry
- `04-Troubleshooting/` — issue log
- `05-Decisions/` — decision records
- `06-Daily-Logs/` — daily notes (inconsistent use)

This structure provides a starting point but needs expansion per the new vault design.

---

## 6. Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Knowledge loss during migration | Medium | Zero deletion. Archive everything. Phase migration. |
| Agent confusion from dual skill sets | High | Archive Claude skills. Single source of truth. |
| Context fragmentation across 5 systems | High | Consolidate into vault. Decommission scattered systems. |
| File count slowing retrieval | Medium | Archive 89% dead weight. Reduce search surface. |
| Multi-session inconsistency | High | Implement shared vault. Daily note as session handoff. |

---

## 7. Migration Summary

| Metric | Before | After (Target) |
|---|---|---|
| Knowledge locations | 5 scattered systems | 1 structured vault |
| Skill definitions | 182 across 2 systems | ~76 active (OpenCode only) |
| Agent definitions | 33 across 2 systems | 16 active (OpenCode only) |
| User-authored .md files | ~686 | ~150 consolidated notes |
| Dead weight files | ~17,000 | Archived, not indexed |
| Duplicate files | 50+ | Eliminated |
| Daily note consistency | Inconsistent | Enforced daily |
| Multi-session awareness | None | Shared vault enables |

---

This audit was performed using the filesystem, explore agent, and direct configuration reads. No files were moved, deleted, or modified. All findings are based on actual file counts and directory inspection dated 2026-06-21.
