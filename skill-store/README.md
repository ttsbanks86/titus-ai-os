# ⚡ OpenCode Skill Store

A complete skill management system for your AI brain.

## What's Here

| File | Purpose |
|------|---------|
| `index.html` | **Skill Store Dashboard** — browse, search, find, and install skills |
| `auditor.html` | **Security Auditor** — paste skill content to check for risks |
| `SKILL-INDEX.md` | **Master Index** — catalog of all 21 skills with metadata |
| `install-skill.ps1` | **One-Click Installer** — installs skills from files or URLs |

## Quick Start

```powershell
# Open the Skill Store Dashboard
start C:\Users\tbank\Desktop\Live\ Cowork\skill-store\index.html

# Or install a skill from a file
.\install-skill.ps1 -Name "my-skill" -Source "C:\path\to\SKILL.md"

# Or install from a URL
.\install-skill.ps1 -Name "my-skill" -Url "https://example.com/skill.md"

# Preview without installing (dry run)
.\install-skill.ps1 -Name "my-skill" -Url "https://example.com/skill.md" -DryRun
```

## How It Works

```
                    ┌─────────────────────┐
                    │   Skill Store       │
                    │   index.html        │
                    └────────┬────────────┘
                             │ browse / search
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ SKILL-INDEX│  │  Auditor   │  │  Installer │
     │  Master   │  │ auditor.html│  │ install.ps1│
     │  Catalog  │  │ (check     │  │ (one-click)│
     │           │  │  safety)   │  │            │
     └────────────┘  └────────────┘  └────────────┘
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌─────────────────────┐
                    │  ~/.config/opencode │
                    │  /skills/           │
                    └─────────────────────┘
```

## Workflow

1. **Find** → Use the FindSkills router or browse the dashboard
2. **Audit** → Paste into `auditor.html` to check for security risks
3. **Install** → Use `install-skill.ps1` to install the skill
4. **Test** → Use `skill-simulator` to verify it works
5. **Use** → Restart OpenCode and trigger the skill

## The FindSkills Router

A dedicated skill (`findskills/SKILL.md`) is installed that auto-matches any task description to the best skill. Just describe what you want to do, and FindSkills returns the best match with confidence score.

Say: *"find a skill for organizing files"* or *"what skill should I use for email?"*
