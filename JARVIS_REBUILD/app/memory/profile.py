from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import AppConfig


@dataclass(frozen=True)
class UserProfile:
    summary: str
    sources: tuple[str, ...]


def load_user_profile(config: AppConfig, *, max_chars: int = 6000) -> UserProfile:
    if not config.user_profile_enabled:
        return UserProfile("", ())

    chunks: list[str] = []
    sources: list[str] = []
    for relative in config.user_profile_files:
        path = _safe_vault_path(config.obsidian_vault_path, relative)
        if path is None or not path.exists() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
        except OSError:
            continue
        if not text:
            continue
        remaining = max_chars - sum(len(chunk) for chunk in chunks)
        if remaining <= 0:
            break
        chunks.append(f"[{relative}]\n{text[:remaining]}")
        sources.append(str(path))

    return UserProfile("\n\n".join(chunks), tuple(sources))


def _safe_vault_path(root: Path, relative: str) -> Path | None:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate
