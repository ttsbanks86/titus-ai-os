from app.config import AppConfig
from app.tools.obsidian import obsidian_response, resolve_wikilink, search_vault


def test_vault_index_detection(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "VAULT-INDEX.md").write_text("[[Jarvis System]]\n", encoding="utf-8")
    (vault / "Jarvis System.md").write_text("# Jarvis System\nAI agent command center.", encoding="utf-8")
    config = AppConfig(obsidian_vault_path=vault, allowed_file_roots=(vault,), obsidian_index_files=("VAULT-INDEX.md",))

    hits = search_vault(config, "Jarvis system")

    assert hits
    assert hits[0].source in {"index", "index-link"}


def test_vault_wikilink_resolution(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "AI Agents.md"
    note.write_text("# AI Agents", encoding="utf-8")
    config = AppConfig(obsidian_vault_path=vault, allowed_file_roots=(vault,))

    assert resolve_wikilink(config, "[[AI Agents]]") == note.resolve()


def test_vault_search_inside_allowed_path(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "VAULT-INDEX.md").write_text("Marketing index", encoding="utf-8")
    (vault / "Marketing.md").write_text("AI agents and marketing automation.", encoding="utf-8")
    config = AppConfig(obsidian_vault_path=vault, allowed_file_roots=(vault,), obsidian_index_files=("VAULT-INDEX.md",))

    hits = search_vault(config, "AI agents")

    assert hits
    assert all(str(hit.path).startswith(str(vault.resolve())) for hit in hits)


def test_blocked_access_outside_vault(tmp_path):
    vault = tmp_path / "vault"
    outside = tmp_path / "outside"
    vault.mkdir()
    outside.mkdir()
    config = AppConfig(obsidian_vault_path=outside, allowed_file_roots=(vault,))

    assert search_vault(config, "anything") == []


def test_clean_obsidian_response_format(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "AI Agents.md"
    note.write_text(
        "# AI Agents\n\n" + "AI agents coordinate tools and memory. " * 20,
        encoding="utf-8",
    )
    config = AppConfig(obsidian_vault_path=vault, allowed_file_roots=(vault,), obsidian_index_files=())

    response = obsidian_response(config, "Jarvis, search Obsidian for AI agents")

    assert response.startswith("I found a matching note.")
    assert "\nNote: AI Agents\n" in response
    assert f"\nPath: {note.resolve()}\n" in response
    assert "Preview:" in response
    assert len(response.split("Preview:", 1)[1].strip()) <= 110
