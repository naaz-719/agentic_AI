
from langchain.tools import tool
import requests

@tool
def weather_lookup_tool(latitude: float, longitude: float):
    """Get real-time weather from Open-Meteo API"""

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current_weather=true"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )

    data = requests.get(url, timeout=10).json()

    return {
        "current_temperature": data["current_weather"]["temperature"],
        "wind_speed": data["current_weather"]["windspeed"],
        "max_temp": data["daily"]["temperature_2m_max"][0],
        "min_temp": data["daily"]["temperature_2m_min"][0]
    }
