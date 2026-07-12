---
owner: Titus
domain: JARVIS
status: Active
priority: Medium
project: JARVIS
area: Agents
created:
updated: 2026-07-12
reviewed: 2026-07-12
related:
  - "[[JARVIS Hub]]"
tags:
  - jarvis
  - agents
---
# Hermes Agent — Vault-Based Context

**Version:** 2.0
**Replaces:** HERMES-ONBOARDING.md (which read 90+ files at startup)
**Date:** 2026-06-21

## Startup Instructions

When Hermes starts a session, read this file. Do not read HERMES-ONBOARDING.md (it is deprecated and will be archived).

### Step 1: Read the Vault Dashboard

Read exactly one file:
```
C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\01-Dashboard\Home.md
```

### Step 2: Follow Wiki-Links

From Home.md, follow wiki-links only for what is relevant to the current task. For example:
- If the task is job search: read [[Job-Search]], [[Resume]], [[Career]]
- If the task is a project: read the specific project note from [[Projects]]
- If the task requires a process: check [[SOPs-Index]] for the relevant SOP

### Step 3: Do Not Read Everything

The vault replaces the old behavior where Hermes read the entire Career_Source_of_Truth directory (90+ files) and OBSIDIAN-AI-OS at every startup. That is over. You now start from Home.md and follow links on demand.

## Key Files (Read on Demand, Not at Startup)

| Purpose | Vault Location |
|---|---|
| Personal context | `Titus-Vault\01-Dashboard\Personal-Context.md` |
| Rules for agents | `Titus-Vault\01-Dashboard\My-Rules.md` |
| Goals | `Titus-Vault\01-Dashboard\My-Goals.md` |
| Voice definition | `Titus-Vault\01-Dashboard\My-Voice.md` |
| Career master | `Titus-Vault\05-Career\Career.md` |
| Job search | `Titus-Vault\05-Career\Job-Search.md` |
| Resume system | `Titus-Vault\05-Career\Resume.md` |
| All SOPs | `Titus-Vault\07-SOPs\SOPs-Index.md` |
| Today's log | `Titus-Vault\02-Daily-Notes\YYYY-MM-DD.md` |

## Career Source of Truth

The Career_Source_of_Truth directory remains at `C:\Users\tbank\Career_Source_of_Truth`. But you no longer read the entire directory at startup. Instead:
- When a job search task starts, read `Titus-Vault\05-Career\Job-Search.md` first
- That note links to the specific CSOT files needed for the task
- Only then read those specific files

## Hermes Configuration

- **Config:** `C:\Users\tbank\AppData\Local\hermes\config.yaml`
- **Env:** `C:\Users\tbank\AppData\Local\hermes\.env`
- **Model:** deepseek-v4-flash via OpenRouter
- **Memory:** 2200 char limit (unchanged)
- **WebUI:** `http://100.94.43.29:8787` (Tailscale)

## Active State (2026-06-21)

- **Current Focus:** Vault migration in progress
- **OpenCode:** Primary runtime. 16 agents. 76 skills.
- **Claude:** Frozen. Skills and agents archived.
- **Vault:** Titus-Vault at `C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\`

## Rules (Unchanged from Original)

- Never modify `Career_Source_of_Truth\07_BA_Resume_System\BA_Base_Resume\BA_MASTER_RESUME.md`
- Always score jobs before applying (minimum 75/100)
- Never auto-post, auto-send, auto-apply, or auto-spend without approval
- Archive, never delete
- Read vault notes before acting. Write to vault after acting.

## TKOS Connections

- [[JARVIS Hub]]
