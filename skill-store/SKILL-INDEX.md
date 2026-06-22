# OpenCode Skill Store — Master Index

> **19 skills cataloged** | Updated June 4, 2026
>
> This is the central registry for every skill in the OpenCode system.
> Each skill has a name, purpose, trigger keywords, risk rating, and install status.
> Use the **FindSkills** router to auto-match any task to the best skill.

---

## Skill Legend

| Icon | Meaning |
|------|---------|
| ✅ | Installed & active |
| 🟢 | Safe — no file write, no network, no code exec |
| 🟡 | Low risk — reads files, uses APIs with user consent |
| 🟠 | Medium risk — writes files, executes scripts locally |
| 🔴 | High risk — modifies system, network calls, auth tokens |

---

## Skills

| # | Status | Risk | Skill | Description | Triggers (say these) | Author |
|---|--------|------|-------|-------------|----------------------|--------|
| 1 | ✅ | 🟢 | **brand-guidelines** | Brand voice, visual identity, content style, messaging | brand, voice, style guide, NOLO, Open Door AI | system |
| 2 | ✅ | 🟡 | **browser-automation** | Web automation, form filling, clicking, scraping | browser, website, click, fill form, navigate, scrape | system |
| 3 | ✅ | 🟡 | **career-ops** | Job search, resumes, Handshake, LinkedIn, WGU | jobs, career, recruiter, Handshake, resume, interview | system |
| 4 | ✅ | 🟠 | **content-scheduling** | Video scheduling, captions, CSV uploads, transcripts | NOLO, Brand2Social, YouTube, TikTok, caption | system |
| 5 | ✅ | 🟢 | **customize-opencode** | OpenCode config, agents, subagents, plugins, MCP | opencode config, agent, skill, plugin, MCP server | system |
| 6 | ✅ | 🟢 | **doc-coauthoring** | Draft, edit, polish resumes, reports, proposals | draft, edit, resume, report, proposal, paper | system |
| 7 | ✅ | 🟠 | **file-organization** | Bulk rename, move, categorize, download cleanup | organize files, rename, move, downloads, sort | system |
| 8 | ✅ | 🟡 | **gmail-automation** | Gmail labels, filters, inbox, attachments | Gmail, email, inbox, label, filter, receipt, invoice | system |
| 9 | ✅ | 🟡 | **identity-eraser** | Data broker opt-out (Spokeo, Whitepages, etc.) | privacy, opt out, data broker, Spokeo, BeenVerified | system |
| 10 | ✅ | 🟢 | **internal-comms** | Emails, recruiter replies, LinkedIn messages | draft email, reply, message, LinkedIn message, status | system |
| 11 | ✅ | 🟡 | **local-ai** | LM Studio, Ollama, local model inference | LM Studio, Ollama, local model, localhost:1234 | system |
| 12 | ✅ | 🟡 | **mcp-builder** | Build, fix, test MCP servers and bridges | MCP server, MCP tool, API connector, tool bridge | system |
| 13 | ✅ | 🟢 | **multi-agent-coordination** | Delegate tasks across specialized agents | delegate, coordinate, subagent, assign, orchestrate | system |
| 14 | ✅ | 🟢 | **project-radar** | Project status, task boards, career plans, briefings | project status, radar, briefing, next actions | system |
| 15 | ✅ | 🟠 | **skill-creator** | Create, edit, package new skills | create skill, new skill, skill package | system |
| 16 | ✅ | 🟢 | **skill-simulator** | Test, score, benchmark skills | simulate, test skill, score, benchmark, practice | system |
| 17 | ✅ | 🟠 | **system-cleanup** | Disk cleanup, drivers, updates, device manager | clean up, disk space, drivers, display, Windows Update | system |
| 18 | ✅ | 🟢 | **web-artifacts-builder** | Quick web apps, dashboards, HTML prototypes | build web app, dashboard, HTML, React, landing page | system |
| 19 | ✅ | 🟠 | **windows-automation** | PowerShell, scheduled tasks, system ops | PowerShell, scheduled task, monitor folder, batch | system |
| 20 | ✅ | 🟢 | **workflow-orchestration** | Multi-step trigger → AI → execute → notify chains | workflow, trigger, pipeline, orchestration, automation chain | system |
| 21 | ✅ | 🟢 | **findskills** | Auto-find the best skill for any task | find skill, what skill, which skill, recommend skill | system |

---

## Quick-Reference: Skill by Job Type

| What you want to do | Best skill |
|---------------------|------------|
| Write code / build features | engineer agent → *web-artifacts-builder* |
| Research a topic | research agent → *doc-coauthoring* |
| Organize my files | *file-organization* |
| Clean up my computer | *system-cleanup* |
| Manage Gmail | *gmail-automation* |
| Find a job / apply | *career-ops* + *linkedin-jobs* |
| Write documentation | *doc-coauthoring* |
| Create a skill | *skill-creator* → *skill-simulator* |
| Automate a workflow | *workflow-orchestration* + *windows-automation* |
| Schedule content | *content-scheduling* |
| Design brand assets | *brand-guidelines* |
| Browser automation | *browser-automation* |
| Build MCP server | *mcp-builder* |
| Privacy / opt-out | *identity-eraser* |
| Configure OpenCode | *customize-opencode* |
| Strategic analysis | *reasoning* agent + *project-radar* |
| **Not sure which skill?** | → **findskills** (auto-match) |

---

## Adding a New Skill

```powershell
# 1. Create the skill file
mkdir ~\.config\opencode\skills\my-skill
# Create SKILL.md with frontmatter (see skill-creator)

# 2. Audit it first
# Open skill-store/auditor.html in browser and paste the SKILL.md content

# 3. Register in this index
# Add a row to the table above

# 4. Restart OpenCode
```

## Security Audit Guide

| Risk Level | What It Means | Checks |
|------------|---------------|--------|
| 🟢 Safe | Read-only, no side effects | No file writes, no network, no code exec |
| 🟡 Low Risk | Reads files or calls APIs with user consent | File reads, API calls with confirmation |
| 🟠 Medium Risk | Writes files, executes scripts | File writes, script execution, local changes |
| 🔴 High Risk | System modification, auth tokens, network calls | Registry, env vars, credentials, external requests |

---

*This index is the source of truth for all OpenCode skills. Update it whenever a skill is added, removed, or modified.*
