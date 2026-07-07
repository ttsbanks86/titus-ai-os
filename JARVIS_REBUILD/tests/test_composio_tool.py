from unittest.mock import Mock, patch

from app.config import AppConfig
from app.doctor import doctor_report
from app.tools.composio_tool import composio_status, read_only_response
from app.tools.email import email_response


def test_composio_config_missing():
    status = composio_status(AppConfig(composio_enabled=True))
    assert status.configured is False
    assert status.error == "missing api key or user id"


@patch("app.tools.composio_tool.list_auth_config_toolkits")
@patch("app.tools.composio_tool.list_connected_toolkits")
def test_composio_config_present(mock_list, mock_auth_configs):
    mock_list.return_value = ["gmail", "notion"]
    mock_auth_configs.return_value = ["gmail", "googlecalendar", "notion"]
    config = AppConfig(composio_enabled=True, composio_api_key="ak_test", composio_user_id="titus")

    status = composio_status(config)

    assert status.configured is True
    assert status.connected_accounts == ("gmail", "notion")
    assert status.auth_configs == ("gmail", "googlecalendar", "notion")


def test_connector_mode_direct_uses_gmail_direct_placeholder():
    response = email_response(AppConfig(connector_mode="direct"), "Jarvis, check my email")
    assert "Email access is not connected yet" in response


def test_connector_mode_composio_uses_composio_setup_response():
    response = email_response(AppConfig(connector_mode="composio"), "Jarvis, check my email")
    assert "Composio is not connected yet" in response


@patch("app.tools.composio_tool.list_connected_toolkits")
def test_composio_read_only_connected(mock_list):
    mock_list.return_value = ["gmail"]
    config = AppConfig(
        connector_mode="composio",
        composio_enabled=True,
        composio_api_key="ak_test",
        composio_user_id="titus",
    )

    response = read_only_response(config, "gmail", "Jarvis, check my email")

    assert response == "Gmail is connected through Composio in read-only mode."


@patch("app.tools.composio_tool.list_auth_config_toolkits")
@patch("app.tools.composio_tool.list_connected_toolkits")
def test_composio_auth_config_without_connected_account(mock_list, mock_auth_configs):
    mock_list.return_value = []
    mock_auth_configs.return_value = ["gmail"]
    config = AppConfig(
        connector_mode="composio",
        composio_enabled=True,
        composio_api_key="ak_test",
        composio_user_id="titus",
    )

    response = read_only_response(config, "gmail", "Jarvis, check my email")

    assert "auth config" in response
    assert "no active connected account" in response


@patch("app.doctor.composio_status")
def test_doctor_reports_auth_config_separately(mock_status):
    mock_status.return_value = Mock(
        configured=True,
        error="",
        connected_accounts=(),
        auth_configs=("googlecalendar", "notion"),
    )

    _, report = doctor_report(
        AppConfig(
            connector_mode="composio",
            composio_enabled=True,
            composio_api_key="ak_test",
            composio_user_id="titus",
        )
    )

    assert "Google Calendar: auth config enabled, no active connected account visible" in report
    assert "Notion: auth config enabled, no active connected account visible" in report


def test_composio_write_request_stays_blocked():
    config = AppConfig(
        connector_mode="composio",
        composio_enabled=True,
        composio_api_key="ak_test",
        composio_user_id="titus",
    )

    response = read_only_response(config, "gmail", "send email to Sam")

    assert "require Jarvis approval" in response
