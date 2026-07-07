from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_dotenv(path: Path = PROJECT_ROOT / ".env", *, override: bool = True) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppConfig:
    project_root: Path = PROJECT_ROOT
    logs_dir: Path = PROJECT_ROOT / "app" / "logs"
    audio_debug_dir: Path = PROJECT_ROOT / "app" / "logs" / "audio_debug"
    audit_log_path: Path = PROJECT_ROOT / "app" / "logs" / "command_audit.jsonl"
    assistant_name: str = "Jarvis"
    weather_provider: str = ""
    weather_api_key: str = ""
    default_location: str = ""
    gmail_credentials_path: Path | None = None
    gmail_token_path: Path | None = None
    gmail_max_results: int = 5
    notion_api_token: str = ""
    browser_path: Path | None = None
    default_browser: str = "chrome"
    google_calendar_enabled: bool = False
    google_calendar_credentials_path: Path | None = None
    google_calendar_token_path: Path | None = None
    composio_enabled: bool = False
    composio_api_key: str = ""
    composio_user_id: str = ""
    composio_allowed_tools: tuple[str, ...] = ("gmail", "googlecalendar", "googledrive", "notion")
    connector_mode: str = "direct"
    llm_enabled: bool = False
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4.1-mini"
    llm_base_url: str = "https://api.openai.com/v1/responses"
    llm_timeout_seconds: int = 30
    llm_max_output_tokens: int = 450
    user_profile_enabled: bool = True
    user_profile_files: tuple[str, ...] = (
        "MEMORY.md",
        "01-Dashboard/Personal-Context.md",
        "01-Dashboard/My-Goals.md",
        "01-Dashboard/My-Rules.md",
        "01-Dashboard/My-Voice.md",
        "08-Agents/System-Constitution.md",
        "09-Knowledge/Technology/Jarvis-Mission-Control-Integration.md",
    )
    api_host: str = "127.0.0.1"
    api_port: int = 8765
    mission_control_api_key: str = ""
    obsidian_vault_path: Path = Path(r"C:\Users\tbank\Desktop\Live Cowork\Titus-Vault")
    obsidian_inbox_path: Path = Path(r"C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\02-Daily-Notes")
    obsidian_index_files: tuple[str, ...] = ("VAULT-INDEX.md", "09-Knowledge/Knowledge-Index.md", "08-Agents/Agents-Index.md")
    allowed_file_roots: tuple[Path, ...] = (Path(r"C:\Users\tbank\Desktop\Live Cowork\Titus-Vault"),)
    workspace_path: Path = PROJECT_ROOT / "workspace"
    file_editing_enabled: bool = True
    openclaw_enabled: bool = False
    openclaw_command: str = ""
    openclaw_timeout_seconds: int = 30
    speech_enabled: bool = True
    tts_engine: str = "edge-tts"
    tts_voice: str = "en-GB-RyanNeural"
    tts_rate: str = "+10%"
    tts_volume: float = 1.0
    tts_pitch: str = "-20Hz"
    tts_playback_mode: str = "hidden"
    # ElevenLabs TTS settings
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Rachel (default ElevenLabs voice)
    elevenlabs_model: str = "eleven_multilingual_v2"
    elevenlabs_stability: float = 0.5
    elevenlabs_similarity_boost: float = 0.75
    tts_playback_mode: str = "hidden"
    self_speech_window_seconds: float = 8.0
    push_to_talk_key: str = "right ctrl"
    min_record_seconds: float = 0.35
    sample_rate: int = 16000
    record_start_padding_ms: int = 250
    record_end_padding_ms: int = 500
    transcribe_provider: str = "speechrecognition"
    debug_audio_enabled: bool = False
    # Always-listening mode
    always_listening_enabled: bool = False
    wake_words: tuple[str, ...] = ("jarvis",)
    wake_word_voice_rms_threshold: float = 350.0
    wake_word_silence_end_seconds: float = 1.2
    wake_word_max_utterance_seconds: float = 12.0
    wake_word_min_utterance_seconds: float = 0.4
    wake_word_post_speak_cooldown_seconds: float = 1.5
    wake_word_pre_roll_seconds: float = 0.6
    wake_word_sleep_phrase: str = "jarvis, go to sleep"
    # Host/show persona mode
    jarvis_persona: str = "companion"  # "companion" (default) or "host" (show/audience mode)
    # Sound effects
    thinking_sound_path: str = ""  # Path to a sound file played while Jarvis is processing
    thinking_sound_enabled: bool = False
    # System control / file access boundaries
    desktop_access: bool = True  # Allow Jarvis to create files/folders on the Desktop
    downloads_access: bool = True  # Allow Jarvis to access the Downloads folder
    full_file_access: bool = False  # Allow Jarvis to access the entire filesystem (dangerous)


def load_config() -> AppConfig:
    load_dotenv()
    vault_path = Path(os.getenv("JARVIS_OBSIDIAN_VAULT_PATH", r"C:\Users\tbank\Desktop\Live Cowork\Titus-Vault"))
    return AppConfig(
        weather_provider=os.getenv("JARVIS_WEATHER_PROVIDER", ""),
        weather_api_key=os.getenv("JARVIS_WEATHER_API_KEY", ""),
        default_location=os.getenv("JARVIS_DEFAULT_LOCATION", ""),
        gmail_credentials_path=_env_optional_path("JARVIS_GMAIL_CREDENTIALS_PATH"),
        gmail_token_path=_env_optional_path("JARVIS_GMAIL_TOKEN_PATH"),
        gmail_max_results=int(os.getenv("JARVIS_GMAIL_MAX_RESULTS", "5")),
        notion_api_token=os.getenv("NOTION_API_TOKEN", "") or os.getenv("JARVIS_NOTION_API_TOKEN", ""),
        browser_path=_env_optional_path("JARVIS_BROWSER_PATH"),
        default_browser=os.getenv("JARVIS_DEFAULT_BROWSER", "chrome"),
        google_calendar_enabled=_env_bool("JARVIS_GOOGLE_CALENDAR_ENABLED", False),
        google_calendar_credentials_path=_env_optional_path("JARVIS_GOOGLE_CALENDAR_CREDENTIALS_PATH"),
        google_calendar_token_path=_env_optional_path("JARVIS_GOOGLE_CALENDAR_TOKEN_PATH"),
        composio_enabled=_env_bool("JARVIS_COMPOSIO_ENABLED", False),
        composio_api_key=os.getenv("JARVIS_COMPOSIO_API_KEY", ""),
        composio_user_id=os.getenv("JARVIS_COMPOSIO_USER_ID", ""),
        composio_allowed_tools=_env_tuple(
            "JARVIS_COMPOSIO_ALLOWED_TOOLS",
            ("gmail", "googlecalendar", "googledrive", "notion"),
        ),
        connector_mode=os.getenv("JARVIS_CONNECTOR_MODE", "direct").strip().lower() or "direct",
        llm_enabled=_env_bool("JARVIS_LLM_ENABLED", bool(os.getenv("OPENAI_API_KEY"))),
        llm_provider=os.getenv("JARVIS_LLM_PROVIDER", "openai").strip().lower() or "openai",
        llm_api_key=_resolve_llm_api_key(),
        llm_model=os.getenv("JARVIS_LLM_MODEL", "gpt-4.1-mini"),
        llm_base_url=os.getenv("JARVIS_LLM_BASE_URL", "").strip(),
        llm_timeout_seconds=int(os.getenv("JARVIS_LLM_TIMEOUT_SECONDS", "30")),
        llm_max_output_tokens=int(os.getenv("JARVIS_LLM_MAX_OUTPUT_TOKENS", "450")),
        user_profile_enabled=_env_bool("JARVIS_USER_PROFILE_ENABLED", True),
        user_profile_files=_env_tuple(
            "JARVIS_USER_PROFILE_FILES",
            (
                "MEMORY.md",
                "01-Dashboard/Personal-Context.md",
                "01-Dashboard/My-Goals.md",
                "01-Dashboard/My-Rules.md",
                "01-Dashboard/My-Voice.md",
                "08-Agents/System-Constitution.md",
                "09-Knowledge/Technology/Jarvis-Mission-Control-Integration.md",
            ),
        ),
        api_host=os.getenv("JARVIS_API_HOST", "127.0.0.1"),
        api_port=int(os.getenv("JARVIS_API_PORT", "8765")),
        mission_control_api_key=os.getenv("JARVIS_MISSION_CONTROL_API_KEY", ""),
        obsidian_vault_path=vault_path,
        obsidian_inbox_path=Path(os.getenv("JARVIS_OBSIDIAN_INBOX_PATH", str(vault_path / "02-Daily-Notes"))),
        obsidian_index_files=_env_tuple(
            "JARVIS_OBSIDIAN_INDEX_FILES",
            ("VAULT-INDEX.md", "09-Knowledge/Knowledge-Index.md", "08-Agents/Agents-Index.md"),
        ),
        allowed_file_roots=_env_paths("JARVIS_ALLOWED_FILE_ROOTS", (vault_path,)),
        workspace_path=Path(os.getenv("JARVIS_WORKSPACE_PATH", str(PROJECT_ROOT / "workspace"))),
        file_editing_enabled=_env_bool("JARVIS_FILE_EDITING_ENABLED", True),
        openclaw_enabled=_env_bool("JARVIS_OPENCLAW_ENABLED", False),
        openclaw_command=os.getenv("JARVIS_OPENCLAW_COMMAND", ""),
        openclaw_timeout_seconds=int(os.getenv("JARVIS_OPENCLAW_TIMEOUT_SECONDS", "30")),
        speech_enabled=_env_bool("JARVIS_SPEECH_ENABLED", True),
        tts_engine=os.getenv("JARVIS_TTS_ENGINE", "edge-tts"),
        tts_voice=os.getenv("JARVIS_TTS_VOICE", "en-GB-RyanNeural"),
        tts_rate=os.getenv("JARVIS_TTS_RATE", "+10%"),
        tts_volume=float(os.getenv("JARVIS_TTS_VOLUME", "1.0")),
        tts_pitch=os.getenv("JARVIS_TTS_PITCH", "-20Hz"),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", ""),
        elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
        elevenlabs_model=os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
        elevenlabs_stability=float(os.getenv("ELEVENLABS_STABILITY", "0.5")),
        elevenlabs_similarity_boost=float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.75")),
        tts_playback_mode=(os.getenv("JARVIS_TTS_PLAYBACK_MODE", "hidden")).strip().lower() or "hidden",
        push_to_talk_key=os.getenv("JARVIS_PUSH_TO_TALK_KEY", "right ctrl"),
        min_record_seconds=float(os.getenv("JARVIS_MIN_RECORD_SECONDS", "0.35")),
        sample_rate=int(os.getenv("JARVIS_SAMPLE_RATE", "16000")),
        record_start_padding_ms=int(os.getenv("JARVIS_RECORD_START_PADDING_MS", "250")),
        record_end_padding_ms=int(os.getenv("JARVIS_RECORD_END_PADDING_MS", "500")),
        transcribe_provider=os.getenv("JARVIS_TRANSCRIBE_PROVIDER", "speechrecognition"),
        debug_audio_enabled=_env_bool("JARVIS_DEBUG_AUDIO", False),
        always_listening_enabled=_env_bool("JARVIS_ALWAYS_LISTENING", False),
        wake_words=_env_tuple("JARVIS_WAKE_WORDS", ("jarvis",)),
        wake_word_voice_rms_threshold=float(os.getenv("JARVIS_WAKE_WORD_VOICE_RMS_THRESHOLD", "350")),
        wake_word_silence_end_seconds=float(os.getenv("JARVIS_WAKE_WORD_SILENCE_END_SECONDS", "1.2")),
        wake_word_max_utterance_seconds=float(os.getenv("JARVIS_WAKE_WORD_MAX_UTTERANCE_SECONDS", "12")),
        wake_word_min_utterance_seconds=float(os.getenv("JARVIS_WAKE_WORD_MIN_UTTERANCE_SECONDS", "0.4")),
        wake_word_post_speak_cooldown_seconds=float(os.getenv("JARVIS_WAKE_WORD_POST_SPEAK_COOLDOWN_SECONDS", "1.5")),
        wake_word_pre_roll_seconds=float(os.getenv("JARVIS_WAKE_WORD_PRE_ROLL_SECONDS", "0.6")),
        wake_word_sleep_phrase=(os.getenv("JARVIS_WAKE_WORD_SLEEP_PHRASE", "jarvis, go to sleep")).strip().lower(),
        jarvis_persona=(os.getenv("JARVIS_PERSONA", "companion")).strip().lower() or "companion",
        thinking_sound_path=os.getenv("JARVIS_THINKING_SOUND_PATH", ""),
        thinking_sound_enabled=_env_bool("JARVIS_THINKING_SOUND_ENABLED", False),
        desktop_access=_env_bool("JARVIS_DESKTOP_ACCESS", True),
        downloads_access=_env_bool("JARVIS_DOWNLOADS_ACCESS", True),
        full_file_access=_env_bool("JARVIS_FULL_FILE_ACCESS", False),
    )


def _env_tuple(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    value = os.getenv(name)
    if not value:
        return default
    return tuple(part.strip() for part in value.split(";") if part.strip())


def _env_paths(name: str, default: tuple[Path, ...]) -> tuple[Path, ...]:
    value = os.getenv(name)
    if not value:
        return default
    return tuple(Path(part.strip()) for part in value.split(";") if part.strip())


def _env_optional_path(name: str) -> Path | None:
    value = os.getenv(name)
    if not value:
        return None
    return Path(value)


def _resolve_llm_api_key() -> str:
    """Resolve the LLM API key with provider-aware fallback.

    Priority:
    1. JARVIS_LLM_API_KEY (explicit user override, used for any provider)
    2. Provider-specific fallback:
       - openai -> OPENAI_API_KEY
       - deepseek -> DEEPSEEK_API_KEY
       - ollama -> (no key needed, returns empty)
    """
    explicit = os.getenv("JARVIS_LLM_API_KEY", "").strip()
    if explicit:
        return explicit
    provider = (os.getenv("JARVIS_LLM_PROVIDER", "openai") or "openai").strip().lower()
    if provider == "deepseek":
        return os.getenv("DEEPSEEK_API_KEY", "").strip()
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY", "").strip()
    return ""
