import requests
import time
import datetime
import os
from pathlib import Path

from dotenv import load_dotenv


file_dir = Path(__file__).parent
load_dotenv(file_dir / '.env')


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable is not set")
LOCATION = "LAGUNA_HILLS"   # Replace with your city name or postal code


def get_time_of_day():
    """Returns 'morning', 'afternoon', or 'evening' based on the current hour.
    
    Morning: 5:00 AM - 11:59 AM
    Afternoon: 12:00 PM - 4:59 PM
    Evening: 5:00 PM - 4:59 AM
    """
    current_hour = datetime.datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    else:
        return "evening"


def get_todays_weather():
    """Fetch current weather data from WeatherAPI.com"""
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}"
        response = requests.get(url)
        data = response.json()
        return data['current']
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "unavailable"  # Fallback if weather data can't be retrieved

