# Goose Skills Setup

**Date:** 2026-06-07
**Status:** 18 SKILLS INSTALLED

---

## Skills Directory
**Location:** `C:\Users\tbank\.agents\skills\`

---

## Installed Skills

### From OpenCode (14 skills via junction links)
| Skill | Purpose |
|-------|---------|
| browser-automation | Web browsing, form filling, scraping |
| file-organization | File management, renaming, sorting |
| windows-automation | PowerShell, scheduled tasks, system ops |
| workflow-orchestration | Multi-step automation chains |
| gmail-automation | Email management, labels, filters |
| career-ops | Job search, resumes, applications |
| identity-eraser | Data broker opt-outs |
| local-ai | Ollama/LM Studio management |
| mcp-builder | MCP server setup |
| project-radar | Project tracking |
| brand-guidelines | Brand voice and identity |
| doc-coauthoring | Document drafting/editing |
| internal-comms | Professional communications |
| system-cleanup | Windows maintenance |

### Goose-Specific (4 custom skills)
| Skill | Purpose |
|-------|---------|
| review-lead-recovery | Local business lead recovery system |
| identity-credit | Credit repair + identity protection |
| book-launch | Struck Down book launch campaign |
| titus-banks-brand | Master brand guidelines |

---

## How Skills Work

1. **Auto-Discovery:** Goose loads skills from `.agents/skills/` at startup
2. **Relevance Matching:** Goose uses skills when relevant to your request
3. **Instruction Loading:** Skills provide detailed workflows and context
4. **File References:** Skills point to relevant files in your project

---

## Example Usage

### Review & Lead Recovery
```
Find 20 plumbers in Seattle with less than 50 Google reviews
```
Goose loads the review-lead-recovery skill and follows the lead research workflow.

### Book Launch
```
What's the status of the Struck Down book launch?
```
Goose loads the book-launch skill and provides current status.

### Identity & Credit
```
Start the credit dispute process
```
Goose loads the identity-credit skill and guides through Phase 2.

### Brand Guidelines
```
Write a social media post for Titus Banks
```
Goose loads the titus-banks-brand skill and follows voice guidelines.

---

## Skill File Format

Each skill has a `SKILL.md` file with:

```markdown
---
name: skill-name
description: What this skill does
---

# Skill Title

## Overview
Brief description

## Workflow
Step-by-step instructions

## File Locations
Paths to relevant files

## Rules
Important constraints
```

---

## Adding More Skills

### From OpenCode
```powershell
# Create junction to existing skill
New-Item -ItemType Junction -Path "C:\Users\tbank\.agents\skills\skill-name" -Target "C:\Users\tbank\.config\opencode\skills\skill-name"
```

### Custom Skill
1. Create directory: `C:\Users\tbank\.agents\skills\new-skill\`
2. Create `SKILL.md` with frontmatter and instructions
3. Restart Goose to discover the skill

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not loading | Restart Goose Desktop |
| Skill not relevant | Goose decides relevance automatically |
| Wrong skill loaded | Be more specific in your request |
| Skill files missing | Check junction link targets |

---

## Reference

- Skills docs: https://goose-docs.ai/docs/guides/context-engineering/using-skills
- Summon extension: https://goose-docs.ai/docs/mcp/summon-mcp
- OpenCode skills: `C:\Users\tbank\.config\opencode\skills\`
- HyperFrames skills: `C:\Users\tbank\Desktop\Live Cowork\.agents\skills\`

---

**Setup complete.** Goose will now use these skills automatically when relevant to your requests.
