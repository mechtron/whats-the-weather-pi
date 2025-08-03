import datetime
import logging
import pytz

from weather import get_todays_weather


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


def generate_greeting_text():
    logging.info("Generating greeting text..")
    time_of_day = get_time_of_day()
    pst = pytz.timezone('US/Pacific')
    today = datetime.datetime.now(pst)
    weekday = today.strftime("%A")
    todays_weather = get_todays_weather()
    return f"""
    Good {time_of_day} Maeve! Today is {weekday} and the weather 
    is {todays_weather['condition']['text']} and the temperature is 
    {int(todays_weather['feelslike_f'])} degrees Fahrenheit. We love you 
    so much Maevey! We are proud of you. You are so cute and talented, 
    and you are perfect just the way you are! Love, Mommy and Daddy.
    """
