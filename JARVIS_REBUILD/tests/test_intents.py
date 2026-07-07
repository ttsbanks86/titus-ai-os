from app.intents import (
    BASIC_CHAT,
    BROWSER,
    CALENDAR,
    CAPABILITIES,
    GREETING,
    NOISE,
    OPENCLAW,
    SELF_SPEECH,
    SYSTEM_QUESTION,
    WEATHER,
    classify_intent,
)


def test_capabilities_intent():
    assert classify_intent("Jarvis, what are your capabilities?").name == CAPABILITIES


def test_partial_capabilities_intents():
    phrases = [
        "what are your",
        "what can you",
        "what do you",
        "tell me your capabilities",
        "what are you able to do",
    ]
    for phrase in phrases:
        assert classify_intent(phrase).name == CAPABILITIES


def test_noise_rejection_phrase():
    intent = classify_intent("I'll see you in the next one.")
    assert intent.name == NOISE
    assert intent.reason == "known background phrase"


def test_greeting_intent():
    assert classify_intent("Hello Jarvis").name == GREETING


def test_weather_intent():
    assert classify_intent("Jarvis, what's the weather today?").name == WEATHER


def test_open_chrome_intent_routes_to_browser():
    phrases = [
        "open Chrome",
        "could you open Chrome",
        "open browser",
        "close browser",
        "open website",
        "search the web for AI agents",
        "use OpenClaw to open Chrome",
    ]
    for phrase in phrases:
        assert classify_intent(phrase).name == BROWSER


def test_today_schedule_intent_routes_to_calendar():
    phrases = [
        "what am I working on today?",
        "what is on my schedule today?",
        "what do I have today?",
        "what are my tasks today?",
    ]
    for phrase in phrases:
        assert classify_intent(phrase).name == CALENDAR


def test_openclaw_intent_for_debugging():
    assert classify_intent("Help me debug this Python script").name == OPENCLAW


def test_system_question_intent():
    assert classify_intent("Jarvis, what tools are connected?").name == SYSTEM_QUESTION
    assert classify_intent("Jarvis, what do you know about me?").name == SYSTEM_QUESTION


def test_basic_chat_intent():
    assert classify_intent("Why is the sky blue?").name == BASIC_CHAT
    assert classify_intent("Tell me how to think about my day").name == BASIC_CHAT


def test_self_speech_rejection():
    assert classify_intent("Hello. I'm here.", recent_assistant_speech="Hello. I'm here.").name == SELF_SPEECH
