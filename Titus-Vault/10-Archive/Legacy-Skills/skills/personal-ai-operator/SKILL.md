---
name: personal-ai-operator
description: "Use when operating the Titus Personal AI Operator: desktop assistant, PC control, browser launch, local model routing, daily briefings, business ops handoff, Graphify handoff, voice/avatar roadmap, or agentic workflow command center."
origin: Titus Banks AI Operating System
version: 0.1.0
---

# Personal AI Operator

This skill controls and explains the local Personal AI Operator MVP.

## Project Path

`C:\Users\tbank\Desktop\Live Cowork\PERSONAL-AI-OPERATOR`

## Main Command

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\tbank\Desktop\Live Cowork\PERSONAL-AI-OPERATOR\Start-PersonalAIOperator.ps1" -Command help
```

## Capabilities

- Local AI calls through `MODEL-ROUTER-MVP`
- Desktop app/window awareness through `agent-cu`
- Browser URL launch
- Daily briefing template
- Business Ops Experts handoff
- Claude Code Graphify handoff
- Local logs

## Safe Commands

```powershell
# Help
.\Start-PersonalAIOperator.ps1 -Command help

# Ask a local model
.\Start-PersonalAIOperator.ps1 -Command ask -Route cheap -Prompt "Give me one focus task."

# Morning briefing
.\Start-PersonalAIOperator.ps1 -Command brief

# List desktop windows
.\Start-PersonalAIOperator.ps1 -Command apps

# Take screenshot
.\Start-PersonalAIOperator.ps1 -Command screenshot

# Open URL
.\Start-PersonalAIOperator.ps1 -Command open-url -Prompt "https://calendar.google.com"

# Business ops handoff
.\Start-PersonalAIOperator.ps1 -Command business -Prompt "Create a morning briefing"
```

## Safety Rules

Require explicit user approval before:
- sending email
- sending WhatsApp
- posting to social
- deleting files
- spending money
- connecting accounts
- enabling dangerous permissions
- installing heavy apps

## Voice / Avatar Status

Voice and avatar are roadmap-only right now. Do not enable always-on microphone, camera, or external avatar services without approval.
