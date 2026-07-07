from __future__ import annotations

from dataclasses import dataclass

import requests

from app.config import AppConfig


@dataclass(frozen=True)
class WeatherReport:
    location: str
    description: str
    temperature_f: float
    feels_like_f: float | None = None


def weather_response(config: AppConfig) -> str:
    provider = (config.weather_provider or "").strip().lower()
    api_key = (config.weather_api_key or "").strip()
    location = (config.default_location or "").strip()

    if provider in {"wttr", "wttr.in", "auto"} or (not provider and not api_key):
        try:
            report = _wttr_current(location)
        except requests.RequestException:
            return "I could not reach the weather service right now."
        except (KeyError, IndexError, TypeError, ValueError):
            return "The weather service returned data I could not read."
        return _format_report(report)

    if not provider or not api_key or not location:
        return (
            "Weather is not connected yet. Set JARVIS_WEATHER_PROVIDER, "
            "JARVIS_WEATHER_API_KEY, and JARVIS_DEFAULT_LOCATION, or set JARVIS_WEATHER_PROVIDER=wttr."
        )

    try:
        if provider in {"openweathermap", "openweather", "owm"}:
            report = _openweathermap_current(api_key, location)
        elif provider in {"weatherapi", "weatherapi.com"}:
            report = _weatherapi_current(api_key, location)
        else:
            return "Weather provider is not supported yet. Use openweathermap or weatherapi."
    except requests.RequestException:
        return "I could not reach the weather service right now."
    except (KeyError, TypeError, ValueError):
        return "The weather service returned data I could not read."

    return _format_report(report)


def _openweathermap_current(api_key: str, location: str) -> WeatherReport:
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": location, "appid": api_key, "units": "imperial"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    description = str(data["weather"][0]["description"])
    main = data["main"]
    return WeatherReport(
        location=str(data.get("name") or location),
        description=description,
        temperature_f=float(main["temp"]),
        feels_like_f=float(main["feels_like"]) if "feels_like" in main else None,
    )


def _weatherapi_current(api_key: str, location: str) -> WeatherReport:
    response = requests.get(
        "https://api.weatherapi.com/v1/current.json",
        params={"key": api_key, "q": location},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    current = data["current"]
    condition = current["condition"]
    return WeatherReport(
        location=str(data.get("location", {}).get("name") or location),
        description=str(condition["text"]).lower(),
        temperature_f=float(current["temp_f"]),
        feels_like_f=float(current["feelslike_f"]) if "feelslike_f" in current else None,
    )


def _wttr_current(location: str) -> WeatherReport:
    target = location or ""
    url = f"https://wttr.in/{target}" if target else "https://wttr.in"
    response = requests.get(url, params={"format": "j1"}, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current_condition"][0]
    area = data.get("nearest_area", [{}])[0]
    area_name = ""
    if area.get("areaName"):
        area_name = str(area["areaName"][0].get("value") or "")
    region = ""
    if area.get("region"):
        region = str(area["region"][0].get("value") or "")
    resolved = ", ".join(part for part in (area_name, region) if part) or location or "your area"
    description = str(current["weatherDesc"][0]["value"]).strip().lower()
    return WeatherReport(
        location=resolved,
        description=description,
        temperature_f=float(current["temp_F"]),
        feels_like_f=float(current["FeelsLikeF"]) if "FeelsLikeF" in current else None,
    )


def _format_report(report: WeatherReport) -> str:
    feels = ""
    if report.feels_like_f is not None:
        feels = f", feels like {round(report.feels_like_f)}"
    return f"Right now in {report.location}, it is {round(report.temperature_f)} degrees and {report.description}{feels}."
