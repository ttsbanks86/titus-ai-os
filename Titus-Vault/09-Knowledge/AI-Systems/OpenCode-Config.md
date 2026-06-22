# OpenCode Config

## Overview
OpenCode configuration, providers, and agent setup. OpenCode is the canonical runtime for the Titus AI OS — all agents run here.

## Current State
- Config location: `C:\Users\tbank\.config\opencode\opencode.json`
- 16 subagents with fallback chains
- 5 providers: anthropic, openai, ollama-local, ollama-cloud, opencodego
- 12 enabled MCP servers
- CEO agent prompt at `C:\Users\tbank\.config\opencode\agent\ceo.md`

## Provider Architecture
- Primary: anthropic provider (when API key loaded)
- Secondary: openai provider (when API key loaded)
- Budget: opencodego, ollama-cloud
- Local: ollama-local (qwen2.5-coder, gemma2)
- Never hard-coded around any single provider

## Key Config
- Subagents: engineer, research, reasoning, qa, linkedin-jobs, documentation, browser, automation, github-ops, gmail-ops, file-ops, workflow-orchestrator, graphic-artist, kling-agent
- Skills: 76 registered skills under skills section
- CEO agent: orchestrates all work through delegation

## Linked Notes
- [[Model-Routing]]
- [[API-Keys]]
- [[Provider-Architecture]]
- [[08-Agents/Agents-Index]]
- [[09-Knowledge/Knowledge-Index]]

## Active Tasks
- [ ] Add vault integration section to ceo.md
- [ ] Verify all fallback chains work

## Decisions Made
- 2026-06-21: OpenCode centered as canonical runtime. Claude agents frozen and archived.
- 2026-06-21: Architecture shifted from cloud-first to provider-independent.

## References
- [[11-Templates/Master-Note-Template]]
