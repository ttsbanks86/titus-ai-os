"""System control tool — gives Jarvis direct hands on the computer.

Uses agent-cu (accessibility-API based desktop automation) for app control:
- Open any app by name
- Close any app
- List running apps
- Read screen text
- Take screenshots
- Click elements, type text, press keys (all behind approval)

Uses Python directly for file operations:
- Create files and folders anywhere authorized (configurable)
- List directory contents
- Read file contents
- Move and rename files (behind approval)

The authorization boundary is configurable:
- JARVIS_ALLOWED_FILE_ROOTS: semicolon-separated list of allowed roots
- JARVIS_DESKTOP_ACCESS: if true, adds the Desktop folder to allowed roots
- JARVIS_FULL_FILE_ACCESS: if true, allows access to the entire filesystem
  (still behind approval for destructive actions)

agent-cu is used because it uses accessibility APIs (not vision), so it's
deterministic, fast, and has zero token cost. It works with any app that
exposes accessibility elements (which is all standard Windows apps).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import AppConfig
from app.tools.approval import PendingAction


# Actions that always require explicit approval before execution.
APPROVAL_REQUIRED_ACTIONS = {
    "close_app",
    "click_element",
    "type_text",
    "press_key",
    "move_file",
    "rename_file",
    "delete_file",
    "delete_folder",
    "run_powershell",
    "resize_window",
    "move_window",
}

# agent-cu command timeout in seconds
AGENT_CU_TIMEOUT = 30


def _agent_cu_cmd(args: list[str]) -> list[str]:
    """Build an agent-cu command that works on Windows.
    agent-cu is installed as a .cmd/.ps1 wrapper, not a direct .exe, so we
    need to invoke it through cmd /c to ensure Python's subprocess can find it.
    """
    return ["cmd", "/c", "agent-cu", *args]


@dataclass(frozen=True)
class SystemControlResult:
    response: str
    approval_required: bool = False
    blocked: bool = False
    action_type: str = "system_control"


def system_control_response(config: AppConfig, command: str) -> SystemControlResult:
    """Main entry point. Classifies the system control request and routes it."""
    body = _command_body(command)

    # App control via agent-cu
    if _looks_like_open_app(body):
        return _open_app(config, body)
    if _looks_like_close_app(body):
        return _close_app(config, body)
    if _looks_like_list_apps(body):
        return _list_apps(config)
    if _looks_like_screenshot(body):
        return _take_screenshot(config, body)

    # File operations (expanded beyond the basic files.py tool)
    if _looks_like_create_folder(body):
        return _create_folder(config, body)
    if _looks_like_list_files(body):
        return _list_files(config, body)
    if _looks_like_read_file(body):
        return _read_file(config, body)
    if _looks_like_move_file(body):
        return _move_file(config, body, "move")
    if _looks_like_rename_file(body):
        return _move_file(config, body, "rename")

    return SystemControlResult("I can open apps, close apps, list running apps, take screenshots, create files and folders, list files, read files, and move things. What do you need?", blocked=False)


# ---------------------------------------------------------------------------
# App control via agent-cu
# ---------------------------------------------------------------------------


def _open_app(config: AppConfig, body: str) -> SystemControlResult:
    app_name = _extract_app_name(body, "open")
    if not app_name:
        return SystemControlResult("Which app do you want me to open?")
    
    # Skip agent-cu entirely - it hangs on Windows. Go straight to fallback.
    # Search for the app in common locations
    app_path = _find_app_path(app_name)
    if app_path:
        try:
            # Use os.startfile() which is the Windows-native way to open files/shortcuts
            # It handles .lnk files, .exe files, and registered file types automatically
            os.startfile(str(app_path))
            return SystemControlResult(f"Opening {app_name}.")
        except OSError as exc:
            return SystemControlResult(f"I found {app_name} at {app_path} but couldn't launch it: {exc}")
    
    return SystemControlResult(f"I couldn't find {app_name} on your system. Is it installed?")


def _find_app_path(app_name: str) -> Path | None:
    """Search for an app by name in common Windows locations.
    
    Searches:
    - Desktop shortcuts (.lnk files)
    - Start Menu shortcuts
    - PATH environment variable
    - Program Files (top-level only)
    """
    app_lower = app_name.lower().strip()
    
    # Try PATH first (fastest)
    found = shutil.which(app_name)
    if found:
        return Path(found)
    found = shutil.which(f"{app_name}.exe")
    if found:
        return Path(found)
    
    # Search Desktop shortcuts (fast, small directory)
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        for item in desktop.glob("*.lnk"):
            if app_lower in item.stem.lower():
                return item
    
    # Search Start Menu shortcuts (fast, targeted)
    start_menu_dirs = [
        Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        Path("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"),
    ]
    for start_dir in start_menu_dirs:
        if start_dir.exists():
            for item in start_dir.rglob("*.lnk"):
                if app_lower in item.stem.lower():
                    return item
    
    # Search Program Files (top-level only, not recursive)
    program_dirs = [
        Path("C:\\Program Files"),
        Path("C:\\Program Files (x86)"),
    ]
    for prog_dir in program_dirs:
        if prog_dir.exists():
            # Look for app folders at top level
            for item in prog_dir.iterdir():
                if item.is_dir() and app_lower in item.name.lower():
                    # Look for main executable in that folder
                    for exe in item.glob("*.exe"):
                        if app_lower in exe.stem.lower() or exe.stem.lower() == item.name.lower():
                            return exe
                    # If no match, return the first exe we find
                    first_exe = next(item.glob("*.exe"), None)
                    if first_exe:
                        return first_exe
    
    return None


def _close_app(config: AppConfig, body: str) -> SystemControlResult:
    app_name = _extract_app_name(body, "close")
    if not app_name:
        return SystemControlResult("Which app do you want me to close? This requires approval.", approval_required=True)
    return SystemControlResult(
        f"Closing {app_name} requires approval. Say 'yes, approve' to confirm, or 'cancel' to discard.",
        approval_required=True,
        action_type="close_app",
    )


def _list_apps(config: AppConfig) -> SystemControlResult:
    try:
        result = subprocess.run(
            _agent_cu_cmd(["apps"]),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return SystemControlResult("I couldn't list running apps. agent-cu may not be installed.")
    if result.returncode != 0 or not result.stdout.strip():
        return SystemControlResult("I couldn't list running apps right now.")
    try:
        apps = json.loads(result.stdout)
        if isinstance(apps, list):
            names = [app.get("name", "Unknown") for app in apps if isinstance(app, dict)]
            # Filter out system processes
            user_apps = [n for n in names if n and n not in ("Explorer.EXE", "TextInputHost", "SystemSettings", "ShellExperienceHost", "SearchHost", "StartMenuExperienceHost")]
            if not user_apps:
                return SystemControlResult("No user apps are currently running.")
            return SystemControlResult(f"Running apps: {', '.join(user_apps[:10])}.")
    except json.JSONDecodeError:
        pass
    return SystemControlResult("I couldn't parse the app list right now.")


def _take_screenshot(config: AppConfig, body: str) -> SystemControlResult:
    app_name = _extract_app_name(body, "screenshot")
    screenshot_dir = Path(config.workspace_path) / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"screenshot_{_timestamp()}.png"
    cmd = _agent_cu_cmd(["screenshot", "--path", str(screenshot_path)])
    if app_name:
        cmd.extend(["-a", app_name])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=AGENT_CU_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired):
        return SystemControlResult("I couldn't take a screenshot. agent-cu may not be installed.")
    if result.returncode == 0 and screenshot_path.exists():
        return SystemControlResult(f"Screenshot saved to {screenshot_path}.")
    return SystemControlResult("I couldn't take a screenshot right now.")


# ---------------------------------------------------------------------------
# File operations (expanded)
# ---------------------------------------------------------------------------


def _create_folder(config: AppConfig, body: str) -> SystemControlResult:
    folder_name = _extract_folder_name(body)
    if not folder_name:
        return SystemControlResult("What should I name the folder?")
    # Determine the target location
    target_dir = _resolve_target_dir(config, body)
    if not target_dir:
        return SystemControlResult("I can't create folders outside the authorized locations.", blocked=True)
    target_path = target_dir / folder_name
    if target_path.exists():
        return SystemControlResult(f"A folder named {folder_name} already exists at {target_path}.")
    try:
        target_path.mkdir(parents=True, exist_ok=False)
    except OSError as exc:
        return SystemControlResult(f"I couldn't create the folder: {exc}")
    return SystemControlResult(f"Created folder {folder_name} at {target_path}.")


def _list_files(config: AppConfig, body: str) -> SystemControlResult:
    target_dir = _resolve_target_dir(config, body)
    if not target_dir:
        return SystemControlResult("I can't list files outside the authorized locations.", blocked=True)
    if not target_dir.exists():
        return SystemControlResult(f"The folder {target_dir} doesn't exist.")
    try:
        entries = sorted(target_dir.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except OSError:
        return SystemControlResult(f"I couldn't read the contents of {target_dir}.")
    if not entries:
        return SystemControlResult(f"The folder {target_dir} is empty.")
    folders = [e.name for e in entries if e.is_dir()]
    files = [e.name for e in entries if e.is_file()]
    parts = []
    if folders:
        parts.append(f"Folders: {', '.join(folders[:15])}")
    if files:
        parts.append(f"Files: {', '.join(files[:15])}")
    if len(folders) + len(files) > 15:
        parts.append(f"And {len(folders) + len(files) - 15} more.")
    return SystemControlResult(f"In {target_dir.name}: {' '.join(parts)}")


def _read_file(config: AppConfig, body: str) -> SystemControlResult:
    file_path = _extract_file_path_from_command(body, config)
    if not file_path:
        return SystemControlResult("Which file do you want me to read?")
    if not _is_path_allowed(config, file_path):
        return SystemControlResult("I can't read files outside the authorized locations.", blocked=True)
    if not file_path.exists():
        return SystemControlResult(f"The file {file_path} doesn't exist.")
    if not file_path.is_file():
        return SystemControlResult(f"{file_path} is not a file.")
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return SystemControlResult(f"I couldn't read the file: {exc}")
    # Cap content for voice output
    if len(content) > 500:
        content = content[:497].rstrip() + "..."
    return SystemControlResult(f"Contents of {file_path.name}: {content}")


def _move_file(config: AppConfig, body: str, action: str) -> SystemControlResult:
    return SystemControlResult(
        f"Moving and renaming files requires approval. Say 'yes, approve' to confirm, or 'cancel' to discard.",
        approval_required=True,
        action_type="move_file" if action == "move" else "rename_file",
    )


# ---------------------------------------------------------------------------
# Authorization boundary
# ---------------------------------------------------------------------------


def _resolve_target_dir(config: AppConfig, body: str) -> Path | None:
    """Determine the target directory for file operations based on the command
    and the authorization configuration. Returns None if not authorized.
    """
    lowered = body.lower()
    # Check if the user specified a location
    if "desktop" in lowered:
        desktop = Path.home() / "Desktop"
        if _is_path_allowed(config, desktop):
            return desktop
        return None
    if "vault" in lowered or "obsidian" in lowered:
        return config.obsidian_vault_path.resolve()
    if "workspace" in lowered:
        return config.workspace_path.resolve()
    if "downloads" in lowered:
        downloads = Path.home() / "Downloads"
        if _is_path_allowed(config, downloads):
            return downloads
        return None
    # Default to the workspace
    return config.workspace_path.resolve()


def _is_path_allowed(config: AppConfig, path: Path) -> bool:
    """Check if a path is within the allowed file roots."""
    # Full file access mode allows everything
    if _has_full_file_access(config):
        return True
    path = path.resolve()
    # Check configured allowed roots
    allowed_roots = list(config.allowed_file_roots) + [
        config.workspace_path.resolve(),
        config.obsidian_inbox_path.resolve(),
        config.obsidian_vault_path.resolve(),
    ]
    # If desktop access is enabled, add it
    if _has_desktop_access(config):
        allowed_roots.append((Path.home() / "Desktop").resolve())
    if _has_downloads_access(config):
        allowed_roots.append((Path.home() / "Downloads").resolve())
    for root in allowed_roots:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def _has_full_file_access(config: AppConfig) -> bool:
    return getattr(config, "full_file_access", False)


def _has_desktop_access(config: AppConfig) -> bool:
    return getattr(config, "desktop_access", False) or _has_full_file_access(config)


def _has_downloads_access(config: AppConfig) -> bool:
    return getattr(config, "downloads_access", False) or _has_full_file_access(config)


# ---------------------------------------------------------------------------
# Intent detection helpers
# ---------------------------------------------------------------------------


def _looks_like_open_app(text: str) -> bool:
    phrases = ("open app", "open the app", "launch app", "start app", "open notepad", "open spotify", "open calculator", "open vscode", "open vs code", "open word", "open excel", "open powerpoint", "open outlook", "open discord", "open slack", "open notion", "open terminal", "open cmd", "open powershell", "open settings")
    if any(phrase in text for phrase in phrases):
        return True
    # Generic "open X" where X is not a browser or website
    import re

    match = re.search(r"\bopen\s+([a-z][a-z\s]+?)\.?\s*$", text)
    if match:
        app = match.group(1).strip()
        # Exclude browser and website commands (handled by browser tool)
        browser_words = ("chrome", "browser", "firefox", "edge", "website", "url", "tab", "web")
        if not any(w in app for w in browser_words):
            return True
    return False


def _looks_like_close_app(text: str) -> bool:
    phrases = ("close app", "close the app", "close notepad", "close spotify", "close calculator", "close vscode", "close vs code", "close word", "close excel", "close powerpoint", "close outlook", "close discord", "close slack", "close notion", "close terminal", "close cmd", "close powershell", "quit app", "kill app")
    return any(phrase in text for phrase in phrases)


def _looks_like_list_apps(text: str) -> bool:
    phrases = ("what apps are running", "list running apps", "what's running", "whats running", "show running apps", "running apps")
    return any(phrase in text for phrase in phrases)


def _looks_like_screenshot(text: str) -> bool:
    return "screenshot" in text or "screen shot" in text or "capture screen" in text


def _looks_like_create_folder(text: str) -> bool:
    # This handles folder creation on the desktop or downloads folder.
    # The files.py tool handles workspace/vault folder creation.
    if "desktop" not in text and "downloads" not in text:
        return False
    folder_indicators = (
        "create folder",
        "create a folder",
        "create a new folder",
        "make folder",
        "make a folder",
        "make a new folder",
        "new folder",
    )
    return any(phrase in text for phrase in folder_indicators)


def _looks_like_list_files(text: str) -> bool:
    phrases = ("list files", "show files", "what's in", "whats in", "what is in", "list folder", "show folder", "what's on my desktop", "whats on my desktop", "list desktop", "show desktop", "list my downloads", "show downloads")
    return any(phrase in text for phrase in phrases)


def _looks_like_read_file(text: str) -> bool:
    phrases = ("read file", "read the file", "show file", "what's in the file", "whats in the file", "file contents", "show me the file")
    return any(phrase in text for phrase in phrases)


def _looks_like_move_file(text: str) -> bool:
    return "move file" in text or "move the file" in text


def _looks_like_rename_file(text: str) -> bool:
    return "rename file" in text or "rename the file" in text or "rename folder" in text


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------


def _extract_app_name(body: str, action: str) -> str:
    """Extract the app name from a command like 'open Notepad' or 'close Spotify'."""
    import re

    # Try "open/close X" pattern
    patterns = [
        rf"\b{action}\s+(?:the\s+)?(?:app\s+)?([a-z][a-z\s]*?)(?:\.|$)",
        rf"\b{action}\s+(?:the\s+)?([a-z][a-z\s]*?)(?:\.|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Clean up common false matches
            if name in ("it", "that", "this", "the", "a", "an", "browser", "chrome", "web", "website"):
                continue
            return name.title()
    return ""


def _extract_folder_name(body: str) -> str:
    import re

    match = re.search(r"(?:called|named|name it|call it)\s+(.+?)(?:\s+on\s+(?:the\s+)?desktop|\s+in\s+(?:the\s+)?downloads|\.|$)", body, re.IGNORECASE)
    if match:
        return _safe_name(match.group(1).strip(" .\"'"))
    match = re.search(r"folder\s+(?:for|for the name)\s+(.+?)(?:\s+on\s+(?:the\s+)?desktop|\s+in\s+(?:the\s+)?downloads|\.|$)", body, re.IGNORECASE)
    if match:
        return _safe_name(match.group(1).strip(" .\"'"))
    return ""


def _extract_file_path_from_command(body: str, config: AppConfig) -> Path | None:
    import re

    # Try to extract a file path or name
    match = re.search(r"file\s+(?:called|named)?\s*([a-z0-9_\-\.]+\.\w+)", body, re.IGNORECASE)
    if match:
        filename = match.group(1).strip()
        # Try workspace first
        candidate = config.workspace_path / filename
        if candidate.exists():
            return candidate
        # Try desktop
        candidate = Path.home() / "Desktop" / filename
        if candidate.exists() and _is_path_allowed(config, candidate):
            return candidate
    return None


def _safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._\-\s]+", "-", value).strip("-")
    return value or "New Folder"


def _command_body(command: str) -> str:
    text = command.lower().replace("jarvis,", "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _timestamp() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y%m%d_%H%M%S")