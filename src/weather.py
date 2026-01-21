import datetime
import logging
import time
import os
from pathlib import Path
import pytz

from dotenv import load_dotenv
import requests


file_dir = Path(__file__).parent
load_dotenv(file_dir / '.env')

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable is not set")
LOCATION = "LAGUNA_HILLS"   # Replace with your city name or postal code


def get_time_of_day():
    """Returns 'morning', 'afternoon', or 'evening' based on the current hour in PST.
    
    Morning: 5:00 AM - 11:59 AM
    Afternoon: 12:00 PM - 4:59 PM
    Evening: 5:00 PM - 4:59 AM
    """
    # Get current time in PST
    pst = pytz.timezone('US/Pacific')
    current_time = datetime.datetime.now(pst)
    current_hour = current_time.hour
    
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    else:
        return "evening"


def get_forecast_weather(days=2):
    """Fetch forecast weather data from WeatherAPI.com"""
    logging.info("Looking up weather forecast..")
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={LOCATION}&days={days}"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching weather forecast: {e}")
        return "unavailable"


def get_todays_weather():
    """Fetch current weather data from WeatherAPI.com"""
    logging.info("Looking up today's weather..")
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "unavailable"  # Fallback if weather data can't be retrieved


def _build_clothing_recommendation(temp_f, condition_text):
    """Create clothing recommendations based on weather"""
    condition_text = (condition_text or "").lower()
    is_raining = 'rain' in condition_text or 'drizzle' in condition_text or 'shower' in condition_text
    is_snowing = 'snow' in condition_text or 'sleet' in condition_text
    is_sunny = 'sunny' in condition_text or 'clear' in condition_text
    
    recommendations = []
    
    # Temperature-based recommendations
    if temp_f is None:
        recommendations.append("something comfortable")
    elif temp_f < 40:
        recommendations.append("a warm coat")
        recommendations.append("long sleeves")
        recommendations.append("pants")
        recommendations.append("warm socks and closed-toe shoes")
    elif temp_f < 55:
        recommendations.append("a light jacket or sweater")
        recommendations.append("long sleeves")
        recommendations.append("pants or leggings")
        recommendations.append("closed-toe shoes")
    elif temp_f < 65:
        recommendations.append("a light jacket or long sleeves")
        recommendations.append("pants or leggings")
        recommendations.append("closed-toe shoes")
    elif temp_f < 75:
        recommendations.append("short sleeves or light layers")
        recommendations.append("pants or shorts")
        recommendations.append("sandals or shoes")
    elif temp_f < 85:
        recommendations.append("short sleeves")
        recommendations.append("shorts or light pants")
        recommendations.append("sandals or shoes")
    else:
        recommendations.append("light, breathable clothes")
        recommendations.append("shorts")
        recommendations.append("sandals or shoes")
    
    # Weather condition adjustments
    if is_raining:
        recommendations.append("a rain jacket")
        recommendations.append("an umbrella")
        recommendations.append("rain boots or water-resistant shoes")
    elif is_snowing:
        recommendations.append("a heavy winter coat")
        recommendations.append("warm boots")
        recommendations.append("a sweater underneath")
    elif is_sunny and temp_f and temp_f > 70:
        recommendations.append("sunscreen")
        recommendations.append("a sun hat")
        recommendations.append("clothes that protect from the sun")
    
    if len(recommendations) > 0:
        rec_text = "Considering the weather, you should wear " + ", ".join(recommendations[:-1])
        if len(recommendations) > 1:
            rec_text += ", and " + recommendations[-1] + "."
        else:
            rec_text += recommendations[-1] + "."
        return rec_text
    else:
        return ""


def get_clothing_recommendation(weather_data):
    """Generate clothing recommendation string based on weather data
    
    Args:
        weather_data: Weather data dictionary
        
    Returns:
        String with clothing recommendations
    """
    if weather_data == "unavailable":
        return "I guess you should wear something comfortable!?"
    
    try:
        current = weather_data['current']
        temp_f = current.get('feelslike_f') or current.get('temp_f')
        condition_text = current['condition']['text']
        return _build_clothing_recommendation(temp_f, condition_text)
            
    except (KeyError, TypeError) as e:
        logging.error(f"Error generating clothing recommendation: {e}")
        return ""


def get_forecast_clothing_recommendation(forecast_data, day_offset=1):
    """Generate clothing recommendations for a forecasted day (defaults to tomorrow)."""
    if forecast_data == "unavailable":
        return "I guess you should wear something comfortable!?"
    
    try:
        forecast_days = forecast_data['forecast']['forecastday']
        if len(forecast_days) <= day_offset:
            raise IndexError("Forecast data does not include requested day offset")
        
        day_data = forecast_days[day_offset]['day']
        temp_f = day_data.get('avgtemp_f') or day_data.get('maxtemp_f') or day_data.get('mintemp_f')
        condition_text = day_data['condition']['text']
        return _build_clothing_recommendation(temp_f, condition_text)
    except (KeyError, TypeError, IndexError) as e:
        logging.error(f"Error generating forecast clothing recommendation: {e}")
        return ""

