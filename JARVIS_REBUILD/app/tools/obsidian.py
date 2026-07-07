from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from app.config import AppConfig


@dataclass(frozen=True)
class VaultHit:
    path: Path
    score: int
    snippet: str
    source: str


def obsidian_response(config: AppConfig, command: str) -> str:
    query = _extract_query(command)
    if not query:
        return "Tell me what to search for in the vault."
    hits = search_vault(config, query)
    if not hits:
        return f"I could not find enough information in the vault about {query}."
    hit = hits[0]
    snippet = _spoken_snippet(hit.snippet)
    return f"I found a matching note.\nNote: {hit.path.stem}\nPath: {hit.path}\nPreview: {snippet}"


def search_vault(config: AppConfig, query: str, limit: int = 5) -> list[VaultHit]:
    vault = config.obsidian_vault_path.resolve()
    if not _is_allowed(vault, config.allowed_file_roots):
        return []
    if not vault.exists():
        return []

    index_hits = _search_index_files(config, vault, query)
    if index_hits:
        return index_hits[:limit]
    return _broad_search(vault, query, limit)


def resolve_wikilink(config: AppConfig, wikilink: str) -> Path | None:
    name = wikilink.strip().strip("[]")
    name = name.split("|", 1)[0].split("#", 1)[0].strip()
    if not name:
        return None
    vault = config.obsidian_vault_path.resolve()
    candidates = [name, f"{name}.md"]
    for path in vault.rglob("*.md"):
        if path.name in candidates or path.stem == name:
            resolved = path.resolve()
            if _is_relative_to(resolved, vault):
                return resolved
    return None


def _search_index_files(config: AppConfig, vault: Path, query: str) -> list[VaultHit]:
    hits: list[VaultHit] = []
    for index_name in config.obsidian_index_files:
        index_path = (vault / index_name).resolve()
        if not _is_relative_to(index_path, vault) or not index_path.exists():
            continue
        text = index_path.read_text(encoding="utf-8", errors="ignore")
        index_score = _score(text, query)
        if index_score:
            hits.append(VaultHit(index_path, index_score + 5, _snippet(text, query), "index"))
        for link in _wikilinks(text):
            linked = resolve_wikilink(config, link)
            if linked is None:
                continue
            linked_text = linked.read_text(encoding="utf-8", errors="ignore")
            linked_score = _score(linked_text + " " + linked.stem, query)
            if linked_score:
                hits.append(VaultHit(linked, linked_score + 3, _snippet(linked_text, query), "index-link"))
    return sorted(hits, key=lambda hit: hit.score, reverse=True)


def _broad_search(vault: Path, query: str, limit: int) -> list[VaultHit]:
    hits: list[VaultHit] = []
    for path in vault.rglob("*.md"):
        if not _is_relative_to(path.resolve(), vault):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        score = _score(text + " " + path.stem, query)
        if score:
            hits.append(VaultHit(path.resolve(), score, _snippet(text, query), "broad"))
    return sorted(hits, key=lambda hit: hit.score, reverse=True)[:limit]


def _extract_query(command: str) -> str:
    text = command.strip()
    patterns = [
        r"search obsidian for (.+)",
        r"find my note about (.+)",
        r"what do i have in my vault about (.+)",
        r"summarize this note (.+)",
        r"open the note about (.+)",
        r"where is this information in my vault(?: about)? (.+)",
    ]
    lower = text.lower().replace("jarvis,", "").strip()
    for pattern in patterns:
        match = re.search(pattern, lower)
        if match:
            return match.group(1).strip(" .?")
    return lower


def _wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", text)


def _score(text: str, query: str) -> int:
    words = [word for word in re.findall(r"\w+", query.lower()) if len(word) > 2]
    lowered = text.lower()
    return sum(lowered.count(word) for word in words)


def _snippet(text: str, query: str, length: int = 220) -> str:
    lowered = text.lower()
    words = re.findall(r"\w+", query.lower())
    start = 0
    for word in words:
        found = lowered.find(word)
        if found >= 0:
            start = max(0, found - 60)
            break
    snippet = re.sub(r"\s+", " ", text[start : start + length]).strip()
    return snippet or "(no readable snippet)"


def _spoken_snippet(snippet: str, length: int = 110) -> str:
    cleaned = re.sub(r"```.*?```", " ", snippet, flags=re.DOTALL)
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", r"\1", cleaned)
    cleaned = re.sub(r"[#>*_`-]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > length:
        cleaned = cleaned[: length - 3].rstrip() + "..."
    return cleaned or "No readable preview."


def _is_allowed(path: Path, roots: tuple[Path, ...]) -> bool:
    resolved = path.resolve()
    return any(_is_relative_to(resolved, root.resolve()) for root in roots)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
