# Titus Personal AI Operator

A safe MVP for a desktop AI personal assistant that connects local models, desktop control, browser launch, business operations, and Claude Code workflows.

## Current MVP Capabilities

- Local model calls through `MODEL-ROUTER-MVP`
- Desktop window inspection through `agent-cu`
- Desktop screenshots through `agent-cu`
- Browser URL launching
- Claude Code Graphify handoff
- Business Ops Experts handoff
- Daily briefing template
- Operation logs

## Quick Start

From this folder:

```powershell
.\Start-PersonalAIOperator.ps1 -Command help
.\Start-PersonalAIOperator.ps1 -Command brief
.\Start-PersonalAIOperator.ps1 -Command ask -Route cheap -Prompt "Give me one focus task for today."
.\Start-PersonalAIOperator.ps1 -Command apps
.\Start-PersonalAIOperator.ps1 -Command open-url -Prompt "https://calendar.google.com"
.\Start-PersonalAIOperator.ps1 -Command business -Prompt "Create a morning briefing for my small business"
```

## Safety Boundaries

The operator will not do these without explicit approval:

- Send email
- Send WhatsApp messages
- Post to social media
- Delete files
- Spend money
- Connect new accounts
- Enable dangerous permissions
- Install heavy applications

## Architecture

```text
User command
→ Start-PersonalAIOperator.ps1
→ Local model router / agent-cu / browser launch / Claude Code handoff
→ Result + log
```

## Existing Integrations

- `agent-cu` for PC/app control
- LM Studio and Ollama through the model router
- Graphify for Claude Code knowledge maps
- Business Ops Experts for small-business department routing
- Claude Code/OpenCode for deeper agentic workflows

## Next Phases

### Phase 2: Voice
- Add speech-to-text for commands
- Add text-to-speech for responses
- Keep push-to-talk first, not always-on recording

### Phase 3: Avatar / Face
- Add a small local HTML dashboard
- Add reactive status states: listening, thinking, acting, waiting for approval
- Optional avatar later

### Phase 4: Browser Agent
- Add Playwright workflows for approved browser tasks
- Examples: research page, open dashboard, summarize visible content

### Phase 5: Daily Life Integrations
- Gmail summaries
- Calendar review
- WhatsApp drafts
- Morning/evening briefing
- File organization

## Recommended Rule

Start with local/private commands. Escalate to Claude Code only when the task needs deep reasoning, code changes, or multi-agent coordination.
