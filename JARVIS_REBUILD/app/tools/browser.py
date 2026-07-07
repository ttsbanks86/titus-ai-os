from __future__ import annotations

import re
import subprocess
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus

from app.config import AppConfig


def browser_response(config: AppConfig, command: str) -> str:
    body = _command_body(command)
    if "close browser" in body:
        return _close_browser(config)
    if "search the web for" in body:
        query = body.split("search the web for", 1)[1].strip(" .?")
        if not query:
            return "Tell me what to search the web for."
        return _open_url(config, f"https://www.google.com/search?q={quote_plus(query)}", f"Searching the web for {query}.")
    if "open website" in body or "open this website" in body:
        url = _extract_url(body)
        if not url:
            return "Tell me which website to open."
        return _open_url(config, url, f"Opening {url}.")
    if "open chrome" in body or "open browser" in body or "use openclaw to open chrome" in body:
        return _open_browser(config)
    return "Tell me which browser action to take."


def _open_browser(config: AppConfig) -> str:
    target = _browser_target(config)
    try:
        full_path = _resolve_browser_path(target)
        if full_path:
            subprocess.Popen([full_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            webbrowser.open("about:blank")
    except OSError:
        try:
            webbrowser.open("about:blank")
        except Exception:
            return "I could not open the browser. Set JARVIS_BROWSER_PATH to the browser executable."
    return f"Opening {config.default_browser or 'browser'}."


def _close_browser(config: AppConfig) -> str:
    process = _browser_process_name(config)
    try:
        subprocess.run(["taskkill", "/IM", process, "/F"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return f"I could not close {config.default_browser or 'the browser'}."
    return f"Closing {config.default_browser or 'browser'}."


def _open_url(config: AppConfig, url: str, response: str) -> str:
    target = _browser_target(config)
    try:
        full_path = _resolve_browser_path(target)
        if full_path:
            subprocess.Popen([full_path, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            webbrowser.open(url)
    except OSError:
        try:
            webbrowser.open(url)
        except Exception:
            return "I could not open the website. Set JARVIS_BROWSER_PATH to the browser executable."
    return response


def _resolve_browser_path(target) -> str:
    """Resolve a browser target (which may be a bare name like 'chrome') to
    the full executable path. Returns empty string if not found.
    This fixes the Chrome rerouting error where a bare 'chrome' name causes
    subprocess to fall back to the OS handler, which may reroute to Edge.
    """
    import shutil

    target_str = str(target)
    # If target is already a full path that exists, use it directly
    if Path(target_str).exists():
        return target_str
    # Try shutil.which (checks PATH)
    exe_name = target_str if target_str.endswith(".exe") else f"{target_str}.exe"
    found = shutil.which(exe_name) or shutil.which(target_str)
    if found:
        return found
    # Try known Windows install locations
    known_paths = {
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "msedge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ],
        "firefox": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ],
    }
    paths = known_paths.get(target_str.lower(), [])
    for path in paths:
        if Path(path).exists():
            return path
    return ""


def _browser_target(config: AppConfig) -> str | Path:
    if config.browser_path:
        return config.browser_path
    browser = (config.default_browser or "chrome").strip().lower()
    aliases = {
        "chrome": "chrome",
        "edge": "msedge",
        "firefox": "firefox",
    }
    return aliases.get(browser, browser)


def _browser_process_name(config: AppConfig) -> str:
    if config.browser_path:
        return config.browser_path.name
    browser = (config.default_browser or "chrome").strip().lower()
    names = {
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "firefox": "firefox.exe",
    }
    return names.get(browser, f"{browser}.exe")


def _extract_url(text: str) -> str:
    match = re.search(r"(https?://\S+|www\.\S+|[a-z0-9-]+\.[a-z]{2,}\S*)", text)
    if not match:
        return ""
    url = match.group(1).strip(" .?")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def _command_body(command: str) -> str:
    body = command.lower().replace("jarvis,", "").strip()
    return re.sub(r"\s+", " ", body)
