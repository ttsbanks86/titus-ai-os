# Model Routing

## Overview
Which model to use for which task. Routing rules, fallback chains, and cost-aware model selection for the Titus AI OS.

## Philosophy
1. Use the best available model for the task within budget
2. Prefer lower-cost models for execution, agentic loops, file ops, automation, bulk processing, and simple coding
3. Use premium models only for high-value reasoning, planning, architecture, deep research, and final review
4. Every agent has a fallback chain: primary → secondary → budget → local/offline
5. When a premium API is unavailable, degrade gracefully — never stop working

## Agent Routing Table
| Agent | Primary | Secondary | Budget | Local |
|---|---|---|---|---|
| engineer | GPT-4o | Claude Sonnet 4 | OpenCodeGo | qwen2.5-coder |
| research | Claude Sonnet 4 | GPT-4o | Ollama Cloud | offline cached |
| reasoning | Claude Sonnet 4 | GPT-4o | Ollama Cloud | offline cached |
| qa | GPT-4o | Claude Sonnet 4 | OpenCodeGo | qwen2.5-coder |
| linkedin-jobs | Claude Sonnet 4 | GPT-4o | GPT-4o-mini | unavailable |
| documentation | Claude Sonnet 4 | GPT-4o | GPT-4o-mini | qwen2.5-coder |
| browser | GPT-4o-mini | OpenCodeGo | Ollama Cloud | unavailable |
| automation | GPT-4o-mini | OpenCodeSaying | Ollama Cloud | PowerShell native |
| file-ops | qwen2.5-coder | qwen2.5-coder | qwen2.5-coder | qwen2.5-coder |
| graphic-artist | GPT-4o-mini | OpenCodeGo | Ollama Cloud | unavailable |

## Current Status
- No premium cloud APIs loaded: ANTHROPIC_KEY, OPENAI_KEY, OPENCODE_KEY are placeholders
- System currently runs on Ollama local/free models via fallback
- KIE API key is loaded for graphic-artist agent

## Linked Notes
- [[OpenCode-Config]]
- [[API-Keys]]
- [[Provider-Architecture]]
- [[08-Agents/Agents-Index]]
- [[09-Knowledge/Knowledge-Index]]

## Active Tasks
- [ ] Run routing verification after API keys are loaded
- [ ] Generate MODEL_VALUE_REPORT.md

## References
- `C:\Users\tbank\.config\opencode\opencode.json`
