# Titus Banks Model Registry

**Last updated:** 2026-06-09  
**Purpose:** Single source of truth for all AI models, their capabilities, costs, and use cases.

---

## LOCAL MODELS (Ollama - Free, Runs on Your Computer)

These are labeled `[LOCAL]` in the OpenCode model picker. They run on your RTX 3080 Laptop (4GB VRAM) and 32GB RAM. No internet required, no API costs.

### Tier 1: Default (Best for Multi-Agent Work)

| Model | Size | Context | Speed | Reasoning | Vision | Best For |
|-------|------|---------|-------|-----------|--------|----------|
| `nemotron-3-nano:latest` | 24GB | 1M tokens | Slow (loads in RAM) | Excellent | No | Primary agent, complex reasoning, multi-step tasks |

### Tier 2: Fast (Good for Quick Tasks)

| Model | Size | Context | Speed | Reasoning | Vision | Best For |
|-------|------|---------|-------|-----------|--------|----------|
| `llama3.2:3b` | 2GB | 128K | Fast | Good | No | Quick answers, simple tasks, small_model default |
| `gemma2:2b` | 1.6GB | 8K | Very Fast | Basic | No | Lightweight tasks, small_model alt |

### Tier 3: Specialized

| Model | Size | Context | Speed | Reasoning | Vision | Best For |
|-------|------|---------|-------|-----------|--------|----------|
| `deepseek-r1:14b` | 9GB | 128K | Medium | Excellent (thinking) | No | Deep reasoning, math, logic |
| `qwen2.5-coder:14b` | 9GB | 32K | Medium | Good | No | Code generation, debugging, technical writing |
| `qwen2.5:14b` | 9GB | 32K | Medium | Good | No | General purpose, multilingual, tools |

---

## CLOUD MODELS (Fallback - When Local Models Reset)

### OpenAI (Paid API - You Have Subscription)

| Model | Type | Cost | Best For |
|-------|------|------|----------|
| `gpt-5.5` | Chat | $$ | Advanced reasoning, long context, general tasks |
| `gpt-image-2.0` | Image Generation | $$ | Creating images from text prompts |

### OpenCode Zen (Built-in Provider)

| Model | Type | Best For |
|-------|------|----------|
| (Check OpenCode UI for current list) | Various | Fast cloud inference, fallback when local is down |

### OpenCode Go (Built-in Provider)

| Model | Type | Best For |
|-------|------|----------|
| (Check OpenCode UI for current list) | Various | Lightweight cloud tasks, quick fallback |

---

## CURRENT DEFAULTS

```json
{
  "model": "ollama-local/nemotron-3-nano:latest",
  "small_model": "ollama-local/gemma2:2b"
}
```

All 15 agents use `nemotron-3-nano:latest` as primary model.

---

## DISABLED MODELS (Removed)

These were removed from Ollama to clean up the model list:

- `deepseek-coder-7b-lmstudio` (4GB, weak, LM Studio import)
- `qwen2.5-coder-7b-lmstudio` (4.7GB, weak, LM Studio import)

---

## USAGE GUIDELINES

**When to use LOCAL (default):**
- Normal development work
- Multi-agent coordination
- Code generation and review
- Research and analysis
- When you have 5+ hours of work ahead

**When to use CLOUD (fallback):**
- Local Ollama models are in 5-hour reset cooldown
- You need image generation (use `gpt-image-2.0`)
- You need a specific cloud-only model for a task
- Quick one-off questions when local is slow to load

**How to switch models in OpenCode:**
1. Press `Ctrl+P` (or `/model` command)
2. Type to filter: `ollama-local/`, `openai/`, etc.
3. Select the model you want

---

## FALLBACK STRATEGY (When Local Models Reset)

If you're in the middle of work and `nemotron-3-nano` is in cooldown:

1. **First try:** `ollama-local/llama3.2:3b` (fast, in RAM)
2. **If you need reasoning:** `ollama-local/deepseek-r1:14b` (thinking model)
3. **If local is completely down:** Use `openai/gpt-5.5` (cloud fallback)

---

## NOTES

- **Nemotron 3 Super (86GB)** was rejected - too large for your system
- **Nemotron 3 Nano (24GB)** chosen - best fit for multi-agent work
- **LM Studio** uninstalled - models were too weak/slow
- **5-hour reset** applies to some Ollama cloud models, not local models
- Local Ollama models don't have a 5-hour limit - they run as long as your computer is on
