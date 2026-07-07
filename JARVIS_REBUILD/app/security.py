from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any


SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?([^'\"\s,;]+)"),
    re.compile(r"\b(?:ak|sk|pk|rk)_[A-Za-z0-9_\-]{12,}\b"),
    re.compile(r"\bya29\.[A-Za-z0-9_\-\.]+\b"),
)


def redact_secrets(value: Any) -> Any:
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, Mapping):
        redacted: dict[Any, Any] = {}
        for key, item in value.items():
            if _secretish_key(str(key)):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_secrets(item)
        return redacted
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [redact_secrets(item) for item in value]
    return value


def _redact_string(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda match: f"{match.group(1)}=[REDACTED]" if match.lastindex and match.lastindex >= 2 else "[REDACTED]", redacted)
    return redacted


def _secretish_key(key: str) -> bool:
    lowered = key.lower()
    return any(part in lowered for part in ("api_key", "apikey", "token", "secret", "password"))
