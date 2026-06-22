# Provider Architecture

## Overview
How providers connect, how fallback chains work, and the architecture of model routing in the Titus AI OS.

## Architecture
OpenCode is configured with 5 providers:
- **anthropic**: Anthropic API (Claude Sonnet 4)
- **openai**: OpenAI API (GPT-4o, GPT-4o-mini)
- **ollama-local**: Local models (qwen2.5-coder, gemma2)
- **ollama-cloud**: Ollama Cloud hosted models
- **opencodego**: OpenCodeGo provider

## Fallback Chain Design
Every agent has: Primary → Secondary → Budget → Local/Offline
When a provider API call fails, the request cascades to the next provider in the chain.

## Provider Independence
- No single provider is essential
- System works on local models when cloud APIs are unavailable
- Premium models are optional quality boosters, not required dependencies

## Linked Notes
- [[OpenCode-Config]]
- [[Model-Routing]]
- [[API-Keys]]
- [[08-Agents/Agents-Index]]
- [[09-Knowledge/Knowledge-Index]]

## Active Tasks
- [ ] Validate fallback chain works end-to-end
- [ ] Document common failure modes and resolutions

## References
- `C:\Users\tbank\.config\opencode\opencode.json`
