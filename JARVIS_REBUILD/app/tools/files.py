from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from app.config import AppConfig


@dataclass(frozen=True)
class FileToolResult:
    response: str
    approval_required: bool = False
    blocked: bool = False
    action_type: str = "file_create"


def file_creation_response(config: AppConfig, command: str) -> FileToolResult:
    if not config.file_editing_enabled:
        return FileToolResult("File editing is disabled. Set JARVIS_FILE_EDITING_ENABLED=true to enable it.", blocked=True)

    requested = _extract_filename(command)
    target_root = _target_root(config, command)
    if not requested:
        requested = "jarvis-note.md"
    requested_path = Path(requested)
    target = requested_path.resolve() if requested_path.is_absolute() else (target_root / requested).resolve()

    if not _is_inside_permitted_create_root(config, target):
        return FileToolResult("Blocked: that file is outside the approved workspace and Obsidian inbox roots.", blocked=True)
    if target.exists():
        return FileToolResult(f"{target} already exists. Overwriting it requires approval.", approval_required=True, action_type="file_overwrite")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_initial_markdown(command), encoding="utf-8")
    return FileToolResult(f"Created {target}.")


def file_append_response(config: AppConfig, command: str) -> FileToolResult:
    if not config.file_editing_enabled:
        return FileToolResult("File editing is disabled. Set JARVIS_FILE_EDITING_ENABLED=true to enable it.", blocked=True, action_type="file_append")

    target = _extract_append_target(config, command)
    if target is None:
        return FileToolResult("I need the note or file path before I can prepare an append.", blocked=True, action_type="file_append")
    if not _is_inside_allowed_roots(config, target):
        return FileToolResult("Blocked: I cannot edit files outside the allowed roots.", blocked=True, action_type="file_append")
    return FileToolResult(f"Appending to {target} requires approval.", approval_required=True, action_type="file_append")


def _target_root(config: AppConfig, command: str) -> Path:
    lowered = command.lower()
    if "obsidian" in lowered or "in my vault" in lowered:
        return config.obsidian_inbox_path.resolve()
    return config.workspace_path.resolve()


def _extract_filename(command: str) -> str:
    text = command.strip()
    # Pattern: "and call it X" / "and name it X"
    match = re.search(r"and\s+call\s+it\s+(.+)$", text, re.IGNORECASE)
    if match:
        return _clean_requested_path(match.group(1).strip(" .\"'"))
    match = re.search(r"and\s+name\s+it\s+(.+)$", text, re.IGNORECASE)
    if match:
        return _clean_requested_path(match.group(1).strip(" .\"'"))
    # Pattern: "called X" / "named X"
    match = re.search(r"(?:called|named)\s+(.+)$", text, re.IGNORECASE)
    if match:
        return _clean_requested_path(match.group(1).strip(" .\"'"))
    # Pattern: "for the name X" / "for name X"
    match = re.search(r"for\s+(?:the\s+)?name\s+(.+)$", text, re.IGNORECASE)
    if match:
        return _clean_requested_path(match.group(1).strip(" .\"'"))
    # Pattern: "with the name X"
    match = re.search(r"with\s+the\s+name\s+(.+)$", text, re.IGNORECASE)
    if match:
        return _clean_requested_path(match.group(1).strip(" .\"'"))
    # Pattern: "for X" (short, e.g. "create a file for Bett")
    match = re.search(r"(?:create|make)\s+a\s+(?:file|folder)\s+for\s+(.+)$", text, re.IGNORECASE)
    if match:
        return _clean_requested_path(match.group(1).strip(" .\"'"))
    # Pattern: "(obsidian) note about X"
    match = re.search(r"(?:obsidian )?note about\s+(.+)", text, re.IGNORECASE)
    if match:
        return _safe_name(match.group(1).strip(" .\"'")) + ".md"
    if "save this in my vault" in text.lower():
        return "jarvis-vault-note.md"
    if "markdown file" in text.lower():
        return "jarvis-note.md"
    return ""


def _extract_append_target(config: AppConfig, command: str) -> Path | None:
    match = re.search(r"append this to(?: my)? note\s+(.+)$", command, re.IGNORECASE)
    if not match:
        match = re.search(r"append this to\s+(.+)$", command, re.IGNORECASE)
    if not match:
        return None
    requested = match.group(1).strip(" .\"'")
    path = Path(requested)
    if path.is_absolute():
        return path.resolve()
    candidate = (config.obsidian_inbox_path / _clean_requested_path(requested)).resolve()
    if candidate.suffix:
        return candidate
    return candidate.with_suffix(".md")


def _initial_markdown(command: str) -> str:
    title = Path(_extract_filename(command) or "Jarvis Note").stem.replace("-", " ").title()
    return f"# {title}\n\nCreated by Jarvis.\n"


def _clean_requested_path(value: str) -> str:
    if ":" in value or "/" in value or "\\" in value:
        return value
    return _safe_name(value)


def _safe_name(value: str) -> str:
    value = value.replace("\\", "/").split("/")[-1]
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return value or "jarvis-note.md"


def _is_inside_permitted_create_root(config: AppConfig, path: Path) -> bool:
    roots = (config.workspace_path.resolve(), config.obsidian_inbox_path.resolve())
    return any(_is_relative_to(path, root) for root in roots)


def _is_inside_allowed_roots(config: AppConfig, path: Path) -> bool:
    roots = tuple(root.resolve() for root in config.allowed_file_roots) + (
        config.workspace_path.resolve(),
        config.obsidian_inbox_path.resolve(),
    )
    return any(_is_relative_to(path, root) for root in roots)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
