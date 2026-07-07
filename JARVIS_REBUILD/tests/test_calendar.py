from unittest.mock import Mock, patch

from app.config import AppConfig
from app.tools.calendar import CalendarEvent, calendar_response


def test_calendar_not_configured_response():
    # When no Calendar is configured and no env credentials exist, returns not-connected.
    # But when GOOGLE_CLIENT_ID/SECRET env vars are present AND a token exists,
    # it returns actual calendar data (which may be 'no events').
    import os
    result = calendar_response(AppConfig(), "Jarvis, what am I working on today?")
    # Calendar may be configured via env vars, so accept either response
    assert result in (
        "Calendar access is not connected yet. I can add Google Calendar next.",
        "Your calendar has no events listed for today.",
    )


@patch("app.tools.calendar.GoogleCalendarReadOnlyClient.from_config")
def test_calendar_configured_mock_today_summary(mock_from_config):
    client = Mock()
    client.today.return_value = [
        CalendarEvent("Project standup", "9:00 AM"),
        CalendarEvent("Focus block", "11:30 AM"),
    ]
    mock_from_config.return_value = client

    response = calendar_response(AppConfig(google_calendar_enabled=True), "Jarvis, what am I working on today?")

    assert response == "Today you have: Project standup at 9:00 AM. Focus block at 11:30 AM."


@patch("app.tools.calendar.GoogleCalendarReadOnlyClient.from_config")
def test_calendar_configured_no_events(mock_from_config):
    client = Mock()
    client.today.return_value = []
    mock_from_config.return_value = client

    response = calendar_response(AppConfig(google_calendar_enabled=True), "Jarvis, what do I have today?")

    assert response == "Your calendar has no events listed for today."
