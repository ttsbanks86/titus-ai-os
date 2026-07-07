from unittest.mock import Mock, patch

from app.config import AppConfig
from app.router import Router
from app.tools.llm import llm_response


def test_llm_disabled_gives_setup_response(tmp_path):
    config = AppConfig(project_root=tmp_path, logs_dir=tmp_path / "logs", audit_log_path=tmp_path / "audit.jsonl")

    result = llm_response(config, "Why is the sky blue?")

    assert result.used is False
    assert "LLM is not connected" in result.response


def test_llm_uses_openai_responses_shape(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_api_key="ak_test_secret",
        llm_model="test-model",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"output_text": "Here is a concise answer."}

    with patch("app.tools.llm.requests.post", return_value=response) as post:
        result = llm_response(config, "Why is the sky blue?")

    assert result.used is True
    assert result.response == "Here is a concise answer."
    payload = post.call_args.kwargs["json"]
    assert payload["model"] == "test-model"
    assert "instructions" in payload
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer ak_test_secret"


def test_llm_invalid_key_response_is_clean(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_api_key="ak_test_secret",
    )
    response = Mock()
    response.status_code = 401
    response.json.return_value = {"error": {"message": "Incorrect API key provided: ak_test_secret"}}

    with patch("app.tools.llm.requests.post", return_value=response):
        result = llm_response(config, "hello")

    assert result.used is False
    assert "key was rejected" in result.response
    assert "ak_test_secret" not in result.response


def test_llm_supports_ollama_provider(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="ollama",
        llm_model="llama3.2",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"response": "Local answer."}

    with patch("app.tools.llm.requests.post", return_value=response) as post:
        result = llm_response(config, "hello")

    assert result.used is True
    assert result.response == "Local answer."
    assert post.call_args.kwargs["json"]["model"] == "llama3.2"


def test_router_uses_llm_for_basic_question(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_api_key="ak_test_secret",
    )
    router = Router(config)

    with patch("app.router.llm_response") as mocked:
        mocked.return_value = Mock(response="A basic answer.", used=True, reason="llm fallback")
        result = router.handle("Why is the sky blue?")

    assert result.intent == "basic_chat"
    assert result.route == "llm"
    assert result.response == "A basic answer."


def test_router_keeps_weather_local_when_llm_enabled(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_api_key="ak_test_secret",
    )
    router = Router(config)

    with patch("app.router.llm_response") as mocked:
        result = router.handle("Jarvis, what's the weather today?")

    assert result.route == "weather"
    mocked.assert_not_called()


def test_router_system_question_uses_llm_context(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "MEMORY.md").write_text("Titus prefers direct, practical help.", encoding="utf-8")
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        obsidian_vault_path=vault,
        llm_enabled=True,
        llm_api_key="ak_test_secret",
        user_profile_files=("MEMORY.md",),
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"output_text": "I know you prefer direct, practical help."}

    with patch("app.tools.llm.requests.post", return_value=response):
        result = Router(config).handle("Jarvis, what do you know about me?")

    assert result.route == "llm"
    assert "direct, practical help" in result.response


def test_llm_supports_deepseek_provider(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="ak_test_deepseek",
        llm_model="deepseek-chat",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "choices": [{"message": {"content": "DeepSeek answer."}}]
    }

    with patch("app.tools.llm.requests.post", return_value=response) as post:
        result = llm_response(config, "hello")

    assert result.used is True
    assert result.response == "DeepSeek answer."
    payload = post.call_args.kwargs["json"]
    assert payload["model"] == "deepseek-chat"
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer ak_test_deepseek"
    # DeepSeek uses the chat completions endpoint, not the Responses API
    assert "chat/completions" in post.call_args.args[0]


def test_llm_deepseek_uses_env_fallback_when_no_explicit_key(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ak_env_deepseek")
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="",
        llm_model="deepseek-chat",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "choices": [{"message": {"content": "From env key."}}]
    }

    with patch("app.tools.llm.requests.post", return_value=response) as post:
        result = llm_response(config, "hello")

    assert result.used is True
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer ak_env_deepseek"


def test_llm_deepseek_missing_key_gives_clean_message(tmp_path, monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="",
        obsidian_vault_path=tmp_path / "vault",
    )
    result = llm_response(config, "hello")
    assert result.used is False
    assert "DeepSeek" in result.response
    assert "missing" in result.response.lower()


def test_llm_deepseek_invalid_key_response_is_clean(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="ak_bad_deepseek",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 401
    response.json.return_value = {"error": {"message": "Invalid API key: ak_bad_deepseek"}}

    with patch("app.tools.llm.requests.post", return_value=response):
        result = llm_response(config, "hello")

    assert result.used is False
    assert "DeepSeek key was rejected" in result.response
    assert "ak_bad_deepseek" not in result.response


def test_llm_deepseek_parses_content_list_shape(tmp_path):
    # Some OpenAI-compatible providers return content as a list of pieces.
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="ak_test_deepseek",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "choices": [
            {"message": {"content": [{"text": "Hello "}, {"text": "world."}]}}
        ]
    }

    with patch("app.tools.llm.requests.post", return_value=response):
        result = llm_response(config, "hello")

    assert result.used is True
    assert result.response == "Hello world."
