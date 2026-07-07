from app.config import AppConfig
from app.router import Router


def make_router(tmp_path):
    vault = tmp_path / "vault"
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "logs" / "audit.jsonl",
        workspace_path=tmp_path / "workspace",
        obsidian_vault_path=vault,
        obsidian_inbox_path=vault / "Inbox",
        allowed_file_roots=(vault,),
        speech_enabled=False,
    )
    return Router(config), config


def test_file_creation_inside_workspace(tmp_path):
    router, config = make_router(tmp_path)

    result = router.handle("Jarvis, create a file called project-notes.md")

    assert result.route == "files"
    assert (config.workspace_path / "project-notes.md").exists()


def test_file_overwrite_requires_approval(tmp_path):
    router, config = make_router(tmp_path)
    config.workspace_path.mkdir(parents=True)
    (config.workspace_path / "project-notes.md").write_text("existing", encoding="utf-8")

    result = router.handle("Jarvis, create a file called project-notes.md")

    assert result.route == "approval"
    assert router.memory.pending_action is not None


def test_file_outside_workspace_is_blocked(tmp_path):
    router, _config = make_router(tmp_path)
    outside = tmp_path / "outside.md"

    result = router.handle(f"Jarvis, create a file called {outside}")

    assert result.route == "files"
    assert result.rejected is True
    assert "Blocked" in result.response


def test_obsidian_note_creation_inside_inbox(tmp_path):
    router, config = make_router(tmp_path)

    result = router.handle("Jarvis, create an Obsidian note about my Jarvis setup")

    assert result.route == "files"
    assert (config.obsidian_inbox_path / "my-Jarvis-setup.md").exists()


def test_append_requires_approval(tmp_path):
    router, config = make_router(tmp_path)
    config.obsidian_inbox_path.mkdir(parents=True)
    (config.obsidian_inbox_path / "project-notes.md").write_text("# Project Notes", encoding="utf-8")

    result = router.handle("Jarvis, append this to my note project-notes.md")

    assert result.route == "approval"
    assert router.memory.pending_action is not None
