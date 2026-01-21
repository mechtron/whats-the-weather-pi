import datetime
import logging
import pytz

from weather import (
    get_todays_weather,
    get_clothing_recommendation,
    get_forecast_weather,
    get_forecast_clothing_recommendation,
)


def get_time_of_day():
    """Returns 'morning', 'afternoon', or 'evening' based on the current hour in PST.
    
    Morning: 5:00 AM - 11:59 AM
    Afternoon: 12:00 PM - 4:59 PM
    Evening: 5:00 PM - 4:59 AM
    """
    pst = pytz.timezone('US/Pacific')
    current_time = datetime.datetime.now(pst)
    current_hour = current_time.hour
    
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    else:
        return "evening"


def _use_tomorrow_forecast(now_pst: datetime.datetime) -> bool:
    """Return True when we should speak about tomorrow (6-9pm PST)."""
    return 18 <= now_pst.hour < 21


def generate_greeting_text():
    logging.info("Generating greeting text..")
    time_of_day = get_time_of_day()
    pst = pytz.timezone('US/Pacific')
    now_pst = datetime.datetime.now(pst)
    today_weekday = now_pst.strftime("%A")
    weather_text = "the weather is unknown"
    clothing_rec = ""
    greeting_day_text = f"Today is {today_weekday}"
    
    if _use_tomorrow_forecast(now_pst):
        forecast_weather = get_forecast_weather(days=2)
        clothing_rec = get_forecast_clothing_recommendation(forecast_weather)
        
        tomorrow = now_pst + datetime.timedelta(days=1)
        tomorrow_weekday = tomorrow.strftime("%A")
        greeting_day_text = f"Tomorrow is {tomorrow_weekday}"
        
        try:
            forecast_day = forecast_weather["forecast"]["forecastday"][1]["day"]
            avg_temp = forecast_day.get("avgtemp_f") or forecast_day.get("maxtemp_f") or forecast_day.get("mintemp_f")
            condition = forecast_day["condition"]["text"]
            if avg_temp is not None:
                weather_text = f"and weather tomorrow will be {condition} with an average temperature of {int(avg_temp)} degrees Fahrenheit"
            else:
                weather_text = f"and the weather tomorrow will be {condition}"
        except (KeyError, IndexError, TypeError):
            weather_text = "tomorrow's weather is unknown. Oh technology!"
    else:
        todays_weather = get_todays_weather()
        clothing_rec = get_clothing_recommendation(todays_weather)
        
        if todays_weather == "unavailable":
            weather_text = "the weather is unknown"
        else:
            weather_text = f"the weather is {todays_weather['current']['condition']['text']} and the temperature is {int(todays_weather['current']['feelslike_f'])} degrees Fahrenheit"
    
    return f"""
    Good {time_of_day} Maeve! {greeting_day_text} and {weather_text}. {clothing_rec} 
    We love you so much Maevey! We are proud of you. You are so cute and talented, 
    and you are perfect just the way you are! Love, Mommy and Daddy.
    """
