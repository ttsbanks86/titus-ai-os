from app.config import AppConfig
from app.router import Router


def make_router(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "logs" / "audit.jsonl",
        speech_enabled=False,
    )
    return Router(config)


def test_risky_action_requires_approval(tmp_path):
    router = make_router(tmp_path)

    result = router.handle("Send an email to Sam about the meeting")

    assert result.route == "approval"
    assert result.intent == "approval_required"
    assert "Say 'yes, approve'" in result.response
    assert router.memory.pending_action is not None


def test_approve_pending_action(tmp_path):
    router = make_router(tmp_path)
    router.handle("Delete files in the temp folder")

    result = router.handle("yes, approve")

    assert result.route == "approval"
    assert result.intent == "approval_confirmed"
    assert "Execution is not connected yet" in result.response
    assert router.memory.pending_action is None


def test_cancel_pending_action(tmp_path):
    router = make_router(tmp_path)
    router.handle("Move files from downloads to archive")

    result = router.handle("cancel")

    assert result.route == "approval"
    assert result.intent == "approval_canceled"
    assert "Canceled:" in result.response
    assert router.memory.pending_action is None


def test_pending_action_requires_exact_approval_phrase(tmp_path):
    router = make_router(tmp_path)
    router.handle("Run terminal command dir")

    result = router.handle("yes")

    assert result.route == "approval"
    assert result.intent == "approval_pending"
    assert router.memory.pending_action is not None


def test_openclaw_execute_changes_requires_approval(tmp_path):
    router = make_router(tmp_path)

    result = router.handle("Connect OpenClaw to execute changes")

    assert result.route == "approval"
    assert result.intent == "approval_required"
    assert result.used_openclaw is False
