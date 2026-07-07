from __future__ import annotations

from dataclasses import dataclass

from app.intents import normalize_text, strip_assistant_name


APPROVAL_PHRASE = "yes approve"
CANCEL_PHRASES = {"cancel", "nevermind", "never mind", "discard"}


@dataclass(frozen=True)
class PendingAction:
    action_type: str
    summary: str
    raw_text: str


RISKY_ACTION_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("send_email", ("send email", "send an email", "reply to email", "reply to this email", "email them", "email him", "email her")),
    ("delete_files", ("delete file", "delete files", "remove file", "remove files")),
    ("move_files", ("move file", "move files", "rename file", "relocate file")),
    ("append_files", ("append to file", "append this to", "append this to my note")),
    ("overwrite_files", ("overwrite file", "overwrite files", "replace file", "replace contents")),
    ("run_terminal_command", ("run command", "terminal command", "powershell", "cmd ", "shell command")),
    ("spend_money", ("buy ", "purchase ", "spend ", "pay for", "subscribe")),
    ("update_calendar", ("update calendar", "schedule a", "schedule an", "schedule meeting", "reschedule", "cancel meeting", "create event")),
    (
        "openclaw_execute_changes",
        (
            "openclaw execute",
            "openclaw change",
            "openclaw modify",
            "openclaw to delete",
            "openclaw to move",
            "openclaw to run",
            "use openclaw to delete",
            "use openclaw to move",
            "use openclaw to run",
            "connect openclaw",
        ),
    ),
)


def detect_pending_action(text: str) -> PendingAction | None:
    body = strip_assistant_name(text)
    for action_type, patterns in RISKY_ACTION_PATTERNS:
        if any(pattern in body for pattern in patterns):
            return PendingAction(action_type=action_type, summary=_summarize(action_type, text), raw_text=text)
    return None


def is_approval(text: str) -> bool:
    return normalize_text(text).replace(",", "") == APPROVAL_PHRASE


def is_cancel(text: str) -> bool:
    body = strip_assistant_name(text)
    return body in CANCEL_PHRASES


def approval_prompt(action: PendingAction) -> str:
    return f"I need approval before I {action.summary}. Say 'yes, approve' to approve, or 'cancel' to discard."


def approved_response(action: PendingAction) -> str:
    return f"Approved: {action.summary}. Execution is not connected yet."


def canceled_response(action: PendingAction) -> str:
    return f"Canceled: {action.summary}."


def _summarize(action_type: str, text: str) -> str:
    labels = {
        "send_email": "send an email",
        "delete_files": "delete files",
        "move_files": "move files",
        "append_files": "append to files",
        "overwrite_files": "overwrite files",
        "run_terminal_command": "run a terminal command",
        "spend_money": "spend money",
        "update_calendar": "update the calendar",
        "openclaw_execute_changes": "connect OpenClaw to execute changes",
    }
    return f"{labels[action_type]} requested by: {text.strip()}"
