import requests
import time
import datetime
import os


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable is not set")
LOCATION = "LAGUNA_HILLS"  # Replace with your city name or postal code


def get_todays_weather():
    # TODO: Implement this
    return {
        "high": 70,
        "low": 50,
        "precipitation": 0.1,
        "wind": 10,
        "cloud_cover": 0.5,
        "humidity": 0.5,
        "sunrise": "07:00",
    }


def get_weather():
    """Fetch current weather data from WeatherAPI.com"""
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}"
        response = requests.get(url)
        data = response.json()
        # Extract the weather condition text
        weather_condition = data['current']['condition']['text']
        return weather_condition
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "unavailable"  # Fallback if weather data can't be retrieved
