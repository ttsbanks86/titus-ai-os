from app.voice.speak import DEFAULT_PLAYBACK_MODE, Speaker, _console_safe


def test_console_safe_replaces_non_ascii():
    assert _console_safe("Watermelon \U0001f349") == "Watermelon ?"


def test_default_playback_mode_is_hidden():
    # The default must be "hidden" so push-to-talk no longer pops up a media player window.
    assert DEFAULT_PLAYBACK_MODE == "hidden"


def test_speaker_normalizes_invalid_playback_mode_to_hidden():
    speaker = Speaker(playback_mode="bogus-mode")
    assert speaker.playback_mode == "hidden"


def test_speaker_accepts_startfile_mode_for_legacy_fallback():
    speaker = Speaker(playback_mode="startfile")
    assert speaker.playback_mode == "startfile"


def test_speaker_accepts_pygame_mode():
    speaker = Speaker(playback_mode="pygame")
    assert speaker.playback_mode == "pygame"


def test_speaker_empty_playback_mode_falls_back_to_hidden():
    speaker = Speaker(playback_mode="")
    assert speaker.playback_mode == "hidden"
