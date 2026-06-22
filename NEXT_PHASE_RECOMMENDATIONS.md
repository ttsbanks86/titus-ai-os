# Next Phase Recommendations

**Date:** 2026-06-21
**Context:** Agent system redesign Phase 1-3 complete (model upgrade, guardrail rewrite, archive cleanup). Architecture now provider-independent — OpenCode is the house, models are replaceable power sources.

---

## 1. Optional: Set Cloud API Keys for Quality Boost

The system works today with local models. Cloud API keys add premium quality for thinking tasks but are **not required** for operation. Every agent has a fallback chain.

### Current State

| Key | Value | Status |
|-----|-------|--------|
| `ANTHROPIC_API_KEY` | `ollama-local` (fake 12-char key) | Falls back to local/secondary |
| `OPENAI_API_KEY` | not set | Falls back to local/secondary |
| `ANTHROPIC_BASE_URL` | `http://localhost:8082` (Ollama proxy) | Blocks direct API access |

### Setup Script (3 commands)

```powershell
# 1. Navigate to project root
cd ~/Desktop/Live\ Cowork

# 2. Edit .env with your real keys
notepad .env

# 3. Load keys
.\Set-CloudApiKeys.ps1
```

The script detects real keys by checking if `ANTHROPIC_API_KEY` starts with `sk-ant-` and if `OPENAI_API_KEY` starts with `sk-proj-`. When both are valid, it removes `ANTHROPIC_BASE_URL` so traffic goes directly to Anthropic instead of the Ollama proxy.

### What Keys Unlock (Quality Boosters, Not Requirements)

- CEO agent → primary model Claude Sonnet 4 (currently falls back to local)
- Engineering/QA → primary model GPT-4o (currently falls back to local)
- Research/Strategy → primary model Claude Sonnet 4 (currently falls back to local)
- Browser/Automation → primary model GPT-4o-mini (currently falls back to local)
- File ops → stays on local qwen2.5-coder regardless (adequate for simple ops)

---

## 2. Model Routing: Provider-Independent Fallback System

**Architecture:** OpenCode is the house. Agents are the rooms. Skills are the tools. Models are replaceable power sources.

**No provider is essential.** Anthropic, OpenAI, DeepSeek, Ollama Cloud, OpenCodeGo, OpenCodeSaying, and local models are all swappable.

**Graceful degradation.** When a premium API is unavailable, the system uses the next available model in the fallback chain. It never stops working.

| Agent | Primary | Secondary | Budget Fallback | Local/Offline Fallback |
|-------|---------|-----------|-----------------|-----------------------|
| CEO orchestrator | Claude Sonnet 4 | GPT-4o | GPT-4o-mini | qwen2.5-coder |
| engineer | GPT-4o | Claude Sonnet 4 | OpenCodeGo | qwen2.5-coder |
| research | Claude Sonnet 4 | GPT-4o | Ollama Cloud | offline (cached) |
| reasoning | Claude Sonnet 4 | GPT-4o | Ollama Cloud | offline (cached) |
| qa | GPT-4o | Claude Sonnet 4 | OpenCodeGo | qwen2.5-coder |
| linkedin-jobs | Claude Sonnet 4 | GPT-4o | GPT-4o-mini | unavailable |
| documentation | Claude Sonnet 4 | GPT-4o | GPT-4o-mini | qwen2.5-coder |
| browser | GPT-4o-mini | OpenCodeGo | Ollama Cloud | unavailable |
| automation | GPT-4o-mini | OpenCodeSaying | Ollama Cloud | PowerShell native |
| github-ops | GPT-4o-mini | OpenCodeGo | Ollama Cloud | git CLI native |
| gmail-ops | GPT-4o-mini | OpenCodeSaying | Ollama Cloud | unavailable |
| file-ops | qwen2.5-coder | qwen2.5-coder | qwen2.5-coder | qwen2.5-coder |
| workflow-orch | GPT-4o-mini | OpenCodeSaying | Ollama Cloud | local scripts |
| kling-agent | GPT-4o-mini | OpenCodeGo | Ollama Cloud | unavailable |

This routing is defined across `opencode.json` agent configs, `ceo.md`, and `CLAUDE.md`. Fallback chains are documented in every agent description.

---

## 3. Proposed Final Agent Hierarchy (Provider-Agnostic)

```
┌──────────────────────────────────────────────────────────────┐
│                    CEO Agent                                  │
│  Primary orchestrator. Routes tasks, reviews outputs,         │
│  delivers results. Never does specialized work directly.      │
│  Primary: Sonnet 4 → GPT-4o → GPT-4o-mini → qwen2.5-coder   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  STRATEGY & ANALYSIS         ENGINEERING & CODE               │
│  ┌─────────────────────┐    ┌──────────────────────┐          │
│  │ research            │    │ engineer              │          │
│  │ reasoning           │    │ qa                    │          │
│  │ linkedin-jobs       │    │ file-ops (local)     │          │
│  │ documentation       │    │ github-ops           │          │
│  └─────────────────────┘    └──────────────────────┘          │
│                                                               │
│  AUTOMATION & INTEGRATION   CONTENT & CAREER                  │
│  ┌─────────────────────┐    ┌──────────────────────┐          │
│  │ browser             │    │ kling-agent          │          │
│  │ automation          │    │ gmail-ops            │          │
│  │ workflow-orch       │    │ (future: content)    │          │
│  └─────────────────────┘    └──────────────────────┘          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

Each agent has a fallback chain. Models are not shown in the hierarchy because **they are replaceable** — the agent structure stays the same regardless of which provider powers it.

**14 agents total** — already defined and configured.

---

## 4. Provider Independence Rules

1. **Never require a specific provider.** Every agent has a fallback path that works without any single cloud API.
2. **Environment variables for keys.** API keys are user-level env vars, never in config files.
3. **Graceful degradation.** If a key is unset, the agent uses its secondary or budget fallback. The system keeps running.
4. **Local-first where possible.** File-ops, automation, and bulk processing work with local models only.
5. **Cost-aware routing.** Default to the cheapest model that meets quality requirements. Only escalate to premium when warranted.

---

## 5. Remaining Duplicate Definitions (Low Priority)

These are still duplicated across runtimes but are **not worth archiving** — they're small, local, and tied to specific tools:

| Duplicate | Locations | Notes |
|-----------|-----------|-------|
| `findskills` skill | OpenCode + Claude | Both reference different SKILL-INDEX formats |
| `gsap-core` skill | OpenCode + Claude | OpenCode is canonical; Claude copy harmless |
| `book-access-workflow` | OpenCode + workspace .agents | Workspace .agents already archived |
| Career Source of Truth files | Live Cowork dir | User-managed, intentionally duplicated |

**Recommendation:** Leave these. The storage cost is negligible and removing them would break references in active configs.

---

## 6. Next Steps

### Phase 4 (Current, ~15 min)

1. **Optional: Set API keys** — run `Set-CloudApiKeys.ps1` for premium quality boost
2. **Configure OpenCodeGo/OpenCodeSaying** — need endpoint details from user
3. **Test fallback routing** — verify each agent degrades gracefully when premium APIs are unavailable
4. **Test one research workflow** — "Research current BA job market trends"
5. **Test one content workflow** — "Draft a LinkedIn post about AI in business"
6. **Test one coding workflow** — "Write a Python script to analyze a CSV"

### Phase 5 (After Keys Verified)

7. **Remove `ANTHROPIC_BASE_URL` from settings** — script handles this automatically
8. **Test Claude cache** — long research sessions benefit from prompt caching
9. **Benchmark quality delta** — run identical prompts through local vs cloud to measure if premium is worth cost
10. **Generate MODEL_VALUE_REPORT.md** — compare cost vs quality across providers

---

## 7. What Not To Do

- **Do not** hard-code the system around any single provider — agents must remain swappable
- **Do not** create new agents yet — 14 is sufficient for current workflows
- **Do not** archive more items — cleanup is complete
- **Do not** add MCP servers — 15 is already generous; validate existing ones first
- **Do not** make the system dependent on cloud APIs being available — it must work offline

---

## Summary

```
Priority 1: Configure OpenCodeGo/OpenCodeSaying endpoints (need user input)
Priority 2: Set optional API keys for premium quality boost
Priority 3: Verify fallback routing works end-to-end
Priority 4: Test real workflows (research → content → code)
Priority 5: Benchmark local vs cloud quality to decide if premium is worth cost
```

The archive removed clutter. The provider-independent architecture ensures the system keeps working regardless of which APIs are available. Cloud keys add quality but are not required.
