from __future__ import annotations

import subprocess
import shlex
from datetime import datetime, timezone
from dataclasses import dataclass

from app.config import AppConfig


@dataclass(frozen=True)
class OpenClawResult:
    used: bool
    response: str
    error: str | None = None
    selection_reason: str = ""


def handle_openclaw_task(prompt: str, config: AppConfig, selection_reason: str = "") -> OpenClawResult:
    if not config.openclaw_enabled or not config.openclaw_command:
        return OpenClawResult(
            used=False,
            response=(
                "This looks like a coding, debugging, build, or planning task. OpenClaw is available as an "
                "optional tool, but it is not configured yet."
            ),
            selection_reason=selection_reason,
        )

    try:
        command = _build_command(config.openclaw_command, prompt)
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=config.openclaw_timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return OpenClawResult(
            True,
            "OpenClaw was routed correctly, but the local model did not finish before the timeout.",
            "timeout",
            selection_reason,
        )
    except OSError as exc:
        return OpenClawResult(True, "OpenClaw could not be started.", str(exc), selection_reason)

    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    if completed.returncode != 0:
        return OpenClawResult(True, _friendly_error(output), output or f"exit {completed.returncode}", selection_reason)
    clean = _clean_output(output)
    return OpenClawResult(True, clean or "OpenClaw completed without returning output.", selection_reason=selection_reason)


def _build_command(command: str, prompt: str) -> list[str]:
    parts = shlex.split(command, posix=False)
    if not parts:
        raise OSError("empty OpenClaw command")
    if "agent" in parts and "--session-key" not in parts and "--session-id" not in parts:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        insert_at = parts.index("agent") + 1
        parts[insert_at:insert_at] = ["--session-key", f"agent:main:jarvis-{stamp}"]
    return [*parts, prompt]


def _friendly_error(output: str) -> str:
    lowered = output.lower()
    if "invalid_api_key" in lowered or "incorrect api key" in lowered or "authentication failed" in lowered:
        return "OpenClaw is installed and routed, but its model provider authentication is failing. Update OpenClaw's model provider key or model settings."
    if "pass --to" in lowered and "--agent" in lowered:
        return "OpenClaw needs a target agent or session. Configure JARVIS_OPENCLAW_COMMAND with an agent, such as openclaw agent --local --agent main --message."
    return "OpenClaw returned an error."


def _clean_output(output: str, max_chars: int = 1200) -> str:
    lines: list[str] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if line.startswith("["):
            continue
        if line.startswith("raw_params="):
            continue
        lines.append(line)
    cleaned = "\n".join(lines).strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rsplit("\n", 1)[0].strip()
