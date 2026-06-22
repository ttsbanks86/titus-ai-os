# Claude Code Model Router MVP

A small local router scaffold for testing free, local, or cheaper OpenAI-compatible model endpoints before wiring them into larger Claude Code/OpenCode workflows.

## Available local providers

### LM Studio
- Base URL: `http://localhost:1234/v1`
- API key placeholder: `lm-studio`
- Models:
  - `qwen2.5-coder-7b-instruct`
  - `mistralai/codestral-22b-v0.1`
  - `deepseek-coder-7b-instruct-v1.5`
  - `text-embedding-nomic-embed-text-v1.5`

### Ollama
- Base URL: `http://localhost:11434/v1`
- API key placeholder: `ollama`
- Models:
  - `deepseek-coder-7b-lmstudio:latest`
  - `qwen2.5-coder-7b-lmstudio:latest`
  - `gemma2:2b`

## Route policy

| Route | Provider | Model | Use |
|---|---|---|---|
| `cheap` | Ollama | `gemma2:2b` | Very simple drafts and low-risk summaries |
| `coding` | LM Studio | `qwen2.5-coder-7b-instruct` | Coding drafts, scripts, refactors |
| `reasoning` | LM Studio | `mistralai/codestral-22b-v0.1` | Harder technical reasoning locally |
| `private` | Ollama | `qwen2.5-coder-7b-lmstudio:latest` | Local/private notes and drafts |
| `deepseek` | LM Studio | `deepseek-coder-7b-instruct-v1.5` | Alternative coding model |
| `embedding` | LM Studio | `text-embedding-nomic-embed-text-v1.5` | Embedding reference, not used by chat test |

## Quick commands

From this folder:

```powershell
.\test-router.ps1
.\test-router.ps1 -Route cheap -Prompt "Summarize this in one sentence: local routing saves premium tokens."
.\test-router.ps1 -Route coding -Prompt "Write a PowerShell function that adds two numbers."
.\test-router.ps1 -Route deepseek -Prompt "Explain what a model router does in 3 bullets."
```

## Safety guardrails

- Do not send secrets, passwords, API keys, private customer data, or sensitive identity data to external models.
- Keep local/private work on `private` or another local-only route.
- Require human approval before sending messages, contacting customers, making financial decisions, or destructive file changes.
- Use premium trusted models for high-stakes reasoning, security-sensitive code, or business-critical decisions.
- Treat this MVP as a routing test scaffold, not a production gateway.

## Next integration steps

1. Add a Claude Code/OpenCode provider entry that points to the preferred local endpoint.
2. Add aliases for common routes.
3. Add a higher-level command like `/route coding "task"`.
4. Add logging for route, provider, model, timestamp, and token/cost estimate.
