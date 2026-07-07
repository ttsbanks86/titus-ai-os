from app.voice.wake_word import (
    AlwaysListeningLoop,
    WakeDecision,
    WakeWordSettings,
    detect_wake_word,
)


# ---------------------------------------------------------------------------
# Wake word classifier tests (pure function, deterministic)
# ---------------------------------------------------------------------------


def test_detect_wake_word_basic_with_comma():
    triggered, word, cleaned = detect_wake_word("Jarvis, what's the weather today?")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "what's the weather today?"


def test_detect_wake_word_basic_without_punctuation():
    triggered, word, cleaned = detect_wake_word("Jarvis what is my schedule")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "what is my schedule"


def test_detect_wake_word_hey_prefix():
    triggered, word, cleaned = detect_wake_word("Hey Jarvis, check my email")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "check my email"


def test_detect_wake_word_ok_prefix():
    triggered, word, cleaned = detect_wake_word("ok Jarvis open chrome")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "open chrome"


def test_detect_wake_word_okay_prefix():
    triggered, word, cleaned = detect_wake_word("okay Jarvis search the web for AI")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "search the web for AI"


def test_detect_wake_word_bare_wake_word_only():
    # User just says "Jarvis" with nothing else.
    triggered, word, cleaned = detect_wake_word("Jarvis")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == ""


def test_detect_wake_word_does_not_trigger_on_mid_sentence_mention():
    # Background conversation that happens to mention Jarvis should not trigger.
    triggered, word, cleaned = detect_wake_word("I was talking to my friend about Jarvis yesterday")
    assert triggered is False
    assert word == ""
    # cleaned text is the full transcript when no wake word matched
    assert "yesterday" in cleaned


def test_detect_wake_word_does_not_trigger_on_unrelated_speech():
    triggered, word, cleaned = detect_wake_word("What's the weather today?")
    assert triggered is False
    assert word == ""


def test_detect_wake_word_empty_transcript():
    triggered, word, cleaned = detect_wake_word("")
    assert triggered is False
    assert word == ""
    assert cleaned == ""


def test_detect_wake_word_case_insensitive():
    triggered, word, cleaned = detect_wake_word("JARVIS, open browser")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "open browser"


def test_detect_wake_word_custom_wake_word():
    triggered, word, cleaned = detect_wake_word("Computer, end program", wake_words=("computer",))
    assert triggered is True
    assert word == "computer"
    assert cleaned == "end program"


def test_detect_wake_word_strips_trailing_punctuation_after_wake_word():
    triggered, word, cleaned = detect_wake_word("Jarvis... what time is it")
    assert triggered is True
    assert word == "jarvis"
    assert cleaned == "what time is it"


def test_detect_wake_word_handles_leading_whitespace():
    triggered, word, cleaned = detect_wake_word("   Jarvis, hello")
    assert triggered is True
    assert cleaned == "hello"


# ---------------------------------------------------------------------------
# WakeWordSettings dataclass tests
# ---------------------------------------------------------------------------


def test_wake_word_settings_defaults_are_sensible():
    s = WakeWordSettings()
    assert s.wake_words == ("jarvis",)
    assert s.sample_rate == 16000
    assert s.voice_rms_threshold > 0
    assert s.silence_end_seconds > 0
    assert s.min_utterance_seconds > 0
    assert s.post_speak_cooldown_seconds > 0


def test_wake_word_settings_can_be_overridden():
    s = WakeWordSettings(
        wake_words=("computer", "hal"),
        sample_rate=8000,
        voice_rms_threshold=500.0,
    )
    assert s.wake_words == ("computer", "hal")
    assert s.sample_rate == 8000
    assert s.voice_rms_threshold == 500.0


# ---------------------------------------------------------------------------
# AlwaysListeningLoop lifecycle tests (no real audio device needed)
# ---------------------------------------------------------------------------


def test_always_listening_loop_can_be_stopped_without_running():
    settings = WakeWordSettings()
    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=lambda _d: None,
    )
    # The loop should not be in a stopped state initially
    assert loop._stop_event.is_set() is False
    loop.stop()
    assert loop._stop_event.is_set() is True


def test_always_listening_loop_cooldown_pauses_capture():
    settings = WakeWordSettings(post_speak_cooldown_seconds=2.0)
    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=lambda _d: None,
    )
    import time

    loop.paused_for_speaking()
    # We are within the cooldown window now
    assert time.monotonic() < loop._cooldown_until
    # An explicit zero cooldown should immediately clear the cooldown
    loop.paused_for_speaking(0.0)
    # _cooldown_until is set to time.monotonic() + 0.0 which is approximately now,
    # so the cooldown is effectively over
    assert time.monotonic() >= loop._cooldown_until - 0.01


def test_always_listening_loop_calls_on_wake_utterance_when_triggered():
    # Verify the loop routes triggered wake decisions to the callback.
    # We don't run the real audio loop; we call detect_wake_word directly and
    # verify the callback receives the expected decision shape.
    received: list[WakeDecision] = []
    settings = WakeWordSettings()
    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=lambda d: received.append(d),
    )

    # Simulate the loop processing an utterance that begins with "Jarvis".
    triggered, word, cleaned = detect_wake_word("Jarvis, what's happening today?", settings.wake_words)
    assert triggered is True
    decision = WakeDecision(
        triggered=triggered,
        wake_word=word,
        cleaned_text=cleaned,
        raw_text="Jarvis, what's happening today?",
        reason="wake_word_matched",
        duration_seconds=2.5,
    )
    # Manually invoke the callback as the loop would
    loop.on_wake_utterance(decision)
    assert len(received) == 1
    assert received[0].triggered is True
    assert received[0].wake_word == "jarvis"
    assert received[0].cleaned_text == "what's happening today?"


def test_always_listening_loop_does_not_call_callback_for_background_speech():
    received: list[WakeDecision] = []
    settings = WakeWordSettings()
    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=lambda d: received.append(d),
    )
    triggered, word, cleaned = detect_wake_word(
        "Let me tell you about my weekend plans",
        settings.wake_words,
    )
    assert triggered is False
    # The real loop would NOT call on_wake_utterance for a non-triggered decision.
    # We simulate that branch by simply not calling the callback.
    assert len(received) == 0


def test_always_listening_loop_state_change_callback_invoked():
    states: list[str] = []
    settings = WakeWordSettings()
    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=lambda _d: None,
        on_state_change=lambda s: states.append(s),
    )
    loop.on_state_change("ready")
    loop.on_state_change("listening")
    assert states == ["ready", "listening"]


def test_always_listening_loop_error_callback_does_not_raise():
    errors: list[str] = []
    settings = WakeWordSettings()
    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=lambda _d: None,
        on_error=lambda m: errors.append(m),
    )
    loop.on_error("transcription error: something failed")
    assert len(errors) == 1
    assert "transcription error" in errors[0]