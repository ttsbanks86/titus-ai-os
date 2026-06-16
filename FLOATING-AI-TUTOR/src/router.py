#!/usr/bin/env python3
"""Model Router — routes questions to the right AI model based on complexity."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".floating-ai-tutor"
ROUTER_CONFIG_FILE = DATA_DIR / "router_config.json"

DEFAULT_ROUTER_CONFIG = {
    "tiers": {
        "local": {
            "name": "Local Ollama",
            "base_url": "http://localhost:11434",
            "model": "llama3.2",
            "timeout": 60,
            "cost_per_1k": 0.0,
        },
        "mid": {
            "name": "DeepSeek",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
            "api_key": "",
            "timeout": 30,
            "cost_per_1k": 0.00027,
        },
        "high": {
            "name": "Claude / GPT",
            "base_url": "",
            "model": "",
            "api_key": "",
            "timeout": 30,
            "cost_per_1k": 0.003,
        },
    },
    "routing_rules": {
        "simple_explanation": "local",
        "basic_question": "local",
        "code_explanation": "mid",
        "technical_deep_dive": "mid",
        "lesson_planning": "mid",
        "complex_reasoning": "high",
        "study_guide": "high",
    },
    "default_tier": "local",
}


def load_router_config() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if ROUTER_CONFIG_FILE.exists():
        try:
            cfg = json.loads(ROUTER_CONFIG_FILE.read_text(encoding="utf-8"))
            return {**DEFAULT_ROUTER_CONFIG, **cfg}
        except Exception:
            pass
    return DEFAULT_ROUTER_CONFIG.copy()


def save_router_config(cfg: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ROUTER_CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def classify_complexity(text: str, question: str = "") -> str:
    """Classify the complexity of a question to route to the right model."""
    combined = (text + " " + question).lower()

    # High complexity indicators
    high_indicators = [
        "explain in detail", "comprehensive", "architecture",
        "design pattern", "best practice", "compare and contrast",
        "evaluate", "analyze", "synthesize", "research",
        "study guide", "learning plan", "curriculum",
    ]
    for indicator in high_indicators:
        if indicator in combined:
            return "high"

    # Mid complexity indicators
    mid_indicators = [
        "explain this code", "how does this work", "debug",
        "function", "class", "algorithm", "lesson",
        "teach me", "step by step", "break down",
    ]
    for indicator in mid_indicators:
        if indicator in combined:
            return "mid"

    # Length-based heuristic
    if len(text) > 2000:
        return "mid"
    if len(question) > 100:
        return "mid"

    return "local"


def call_model(prompt: str, system_prompt: str = "", tier: str = "local") -> Optional[str]:
    """Call an AI model at the specified tier."""
    cfg = load_router_config()
    tier_cfg = cfg["tiers"].get(tier)
    if not tier_cfg:
        return None

    if tier == "local":
        return _call_ollama(prompt, system_prompt, tier_cfg)
    elif tier == "mid":
        return _call_openai_compatible(prompt, system_prompt, tier_cfg)
    elif tier == "high":
        return _call_openai_compatible(prompt, system_prompt, tier_cfg)

    return None


def _call_ollama(prompt: str, system_prompt: str, cfg: dict) -> Optional[str]:
    """Call local Ollama model."""
    url = f"{cfg['base_url']}/api/generate"
    payload = {
        "model": cfg["model"],
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_ctx": 4096},
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=cfg["timeout"]) as resp:
            result = json.loads(resp.read())
            return result.get("response", "").strip()
    except Exception:
        return None


def _call_openai_compatible(prompt: str, system_prompt: str, cfg: dict) -> Optional[str]:
    """Call an OpenAI-compatible API (DeepSeek, GPT, Claude via API)."""
    if not cfg.get("api_key") or not cfg.get("base_url"):
        return None

    url = f"{cfg['base_url']}/chat/completions"
    payload = {
        "model": cfg["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 2048,
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg['api_key']}",
        }
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=cfg["timeout"]) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def smart_explain(text: str, question: str = "", context: str = "") -> str:
    """Route to the best model and explain."""
    tier = classify_complexity(text, question)
    cfg = load_router_config()

    system_prompt = (
        "You are a patient, clear AI tutor. Explain concepts step by step. "
        "Use simple language first, then add technical detail. "
        "Always include a concrete example."
    )

    prompt = text.strip()
    if context:
        prompt = f"Previous conversation:\n{context}\n\n{prompt}"
    if question:
        prompt = f"{prompt}\n\nUser question: {question}\n\nExplain this clearly."
    else:
        prompt = f"{prompt}\n\nExplain what this is and how it works. Break it down step by step."

    # Try the classified tier first
    result = call_model(prompt, system_prompt, tier)
    if result:
        return f"[{cfg['tiers'][tier]['name']}] {result}"

    # Fall back to local
    if tier != "local":
        result = call_model(prompt, system_prompt, "local")
        if result:
            return f"[Local Ollama] {result}"

    # Final fallback
    return (
        f"I couldn't reach any AI model. The question was classified as '{tier}' complexity.\n\n"
        "To enable cloud models, add API keys in:\n"
        f"{ROUTER_CONFIG_FILE}\n\n"
        "For now, make sure Ollama is running for local explanations."
    )


def get_available_models() -> dict:
    """Check which models are available."""
    cfg = load_router_config()
    available = {}

    # Check local
    try:
        url = f"{cfg['tiers']['local']['base_url']}/api/tags"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            available["local"] = [m["name"] for m in data.get("models", [])]
    except Exception:
        available["local"] = []

    # Check mid
    available["mid"] = bool(cfg["tiers"]["mid"].get("api_key"))

    # Check high
    available["high"] = bool(cfg["tiers"]["high"].get("api_key"))

    return available
