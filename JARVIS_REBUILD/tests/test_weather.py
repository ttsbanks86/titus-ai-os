from unittest.mock import Mock, patch

from app.config import AppConfig
from app.tools.weather import weather_response


@patch("app.tools.weather.requests.get")
def test_weather_without_api_key_uses_wttr_fallback(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "nearest_area": [{"areaName": [{"value": "Seattle"}], "region": [{"value": "Washington"}]}],
        "current_condition": [
            {
                "temp_F": "62",
                "FeelsLikeF": "61",
                "weatherDesc": [{"value": "Partly cloudy"}],
            }
        ],
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    config = AppConfig(default_location="New Orleans, LA")
    response = weather_response(config)
    assert response == "Right now in Seattle, Washington, it is 62 degrees and partly cloudy, feels like 61."


@patch("app.tools.weather.requests.get")
def test_openweathermap_weather_response(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "name": "New Orleans",
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 78.2, "feels_like": 80.1},
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    config = AppConfig(
        weather_provider="openweathermap",
        weather_api_key="test-key",
        default_location="New Orleans, LA",
    )

    response = weather_response(config)

    assert response == "Right now in New Orleans, it is 78 degrees and clear sky, feels like 80."
    mock_get.assert_called_once()


@patch("app.tools.weather.requests.get")
def test_weatherapi_weather_response(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "location": {"name": "New Orleans"},
        "current": {
            "temp_f": 77.6,
            "feelslike_f": 79.0,
            "condition": {"text": "Partly cloudy"},
        },
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    config = AppConfig(
        weather_provider="weatherapi",
        weather_api_key="test-key",
        default_location="New Orleans, LA",
    )

    response = weather_response(config)

    assert response == "Right now in New Orleans, it is 78 degrees and partly cloudy, feels like 79."
    mock_get.assert_called_once()
