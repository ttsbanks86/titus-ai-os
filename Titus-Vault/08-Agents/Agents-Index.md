# Agents Index

Master index of all active agents in the Titus AI OS. OpenCode is the canonical runtime.

## OpenCode Agents (Active)

| Agent | Primary Model | Role |
|---|---|---|
| [[CEO-Agent]] | anthropic/claude-sonnet-4 | Orchestrator. Delegates to subagents. |
| [[Engineer-Agent-OC]] | openai/gpt-4o | Coding, debugging, technical implementation |
| [[QA-Agent]] | openai/gpt-4o | Testing, code review, quality assurance |
| [[Research-Agent]] | anthropic/claude-sonnet-4 | Web research, competitive analysis, synthesis |
| [[Browser-Agent]] | openai/gpt-4o-mini | Playwright browser automation |
| [[Automation-Agent]] | openai/gpt-4o-mini | PowerShell scripts, scheduled tasks |
| [[GitHub-Agent]] | openai/gpt-4o-mini | Git operations, PRs, issues |
| [[Gmail-Agent]] | openai/gpt-4o-mini | Email management, labels, filters |
| [[LinkedIn-Agent]] | anthropic/claude-sonnet-4 | Job search, LinkedIn automation |
| [[Reasoning-Agent]] | anthropic/claude-sonnet-4 | Complex analysis, strategic planning |
| [[File-Agent]] | qwen2.5-coder:14b | File organization, renaming, cleanup |
| [[Workflow-Agent]] | openai/gpt-4o-mini | Multi-step automation workflows |
| [[Documentation-Agent]] | anthropic/claude-sonnet-4 | READMEs, technical docs, guides |
| [[Graphic-Agent]] | openai/gpt-4o-mini | KIE-powered image and video generation |

## Hermes Agent (Active)

[[Hermes-Agent]] — Goose-compatible personal assistant. deepseek-v4-flash via OpenRouter. Access to terminal, browser, file system, desktop automation. Uses the same Titus-Vault as OpenCode.

## Claude Agents (Archived)

All 10 Claude agents (architect, code-reviewer, database-reviewer, docs-lookup, marketing-agent, performance-optimizer, planner, security-reviewer, seo-specialist, tdd-guide) are archived. OpenCode is the canonical runtime.

## Agent Rules
- Each agent reads relevant vault notes before acting
- Each agent reports to CEO for daily note integration
- No agent creates standalone memory files
- All knowledge lives in Titus-Vault
