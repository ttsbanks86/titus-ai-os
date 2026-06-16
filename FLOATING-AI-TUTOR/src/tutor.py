#!/usr/bin/env python3
"""AI Tutor engine — generates explanations from captured screen content."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".floating-ai-tutor"
CONFIG_FILE = DATA_DIR / "tutor_config.json"

DEFAULT_CONFIG = {
    "model": "llama3.2",
    "base_url": "http://localhost:11434",
    "fallback_mode": "local",
    "system_prompt": (
        "You are a patient, clear AI tutor. Explain concepts step by step. "
        "Use simple language first, then add technical detail. "
        "Always include a concrete example. "
        "If the user shares code, explain what it does line by line. "
        "If the user shares a diagram or text, explain the key takeaways."
    ),
}


def load_config() -> dict:
    """Load tutor configuration."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return {**DEFAULT_CONFIG, **cfg}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict):
    """Save tutor configuration."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def explain_with_ollama(text: str, question: str = "", config: dict | None = None, context: str = "") -> Optional[str]:
    """Generate explanation using local Ollama model."""
    cfg = config or load_config()
    url = f"{cfg['base_url']}/api/generate"

    prompt = text.strip()
    if context:
        prompt = f"Previous conversation:\n{context}\n\n" + prompt
    if question:
        prompt = f"{prompt}\n\nUser question: {question}\n\nExplain this clearly."
    else:
        prompt = f"{prompt}\n\nExplain what this is and how it works. Break it down step by step."

    payload = {
        "model": cfg["model"],
        "prompt": prompt,
        "system": cfg["system_prompt"],
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_ctx": 4096,
        },
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result.get("response", "").strip()
    except Exception:
        return None


def explain_with_fallback(text: str, question: str = "") -> str:
    """Generate a helpful response when no AI model is available."""
    lines = text.strip().split("\n")
    preview = "\n".join(lines[:8])
    if len(lines) > 8:
        preview += f"\n... ({len(lines)} total lines)"

    response = f"📋 **Captured Content ({len(lines)} lines):**\n\n```\n{preview}\n```\n\n"
    response += "💡 **To get AI-powered explanations, install Ollama:**\n\n"
    response += "1. Download from https://ollama.com\n"
    response += "2. Run: `ollama pull llama3.2`\n"
    response += "3. Restart AI Tutor\n\n"
    response += "For now, I've captured your screen content above. "
    response += "Once Ollama is running, I'll provide detailed explanations automatically."

    if question:
        response += f"\n\nYour question was: *{question}*"

    return response


def explain(text: str, question: str = "", context: str = "") -> str:
    """Generate explanation — tries Ollama first, falls back gracefully."""
    if not text or not text.strip():
        return "I couldn't extract any text from the selected area. Try selecting a region with more visible text, or check that OCR is working."

    result = explain_with_ollama(text, question, context=context)
    if result:
        return result

    return explain_with_fallback(text, question)


def check_ollama() -> bool:
    """Check if Ollama is running and accessible."""
    cfg = load_config()
    try:
        url = f"{cfg['base_url']}/api/tags"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            return len(models) > 0
    except Exception:
        return False
