#!/usr/bin/env python3

import datetime
import time
import logging
import os

from gpiozero import (
    Button,
    PWMLED,
)
from signal import pause

from text_to_speech import say_this_text
from weather import get_todays_weather


button = Button(12, pull_up=True)   # blue
button_led_red = PWMLED(16)         # purple
button_led_green = PWMLED(20)       # grey
button_led_blue = PWMLED(21)        # white


def button_leds_off():
    # Button LEDs are active low, .on() means LEDs off
    button_led_red.on()
    button_led_green.on()
    button_led_blue.on()


def button_leds_pink():
    button_led_red.value = 0.0     # 100% red
    button_led_green.value = 1.0   # 0% green
    button_led_blue.value = 0.7    # 30% blue


import requests
import time
import datetime
import os
from pathlib import Path

from dotenv import load_dotenv

file_dir = Path(__file__).parent
load_dotenv(file_dir / '.env')


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


def button_push():
    logging.info("Maeve pushed the button")
    button_leds_pink()
    time_of_day = get_time_of_day()
    todays_weather = get_todays_weather()
    say_this_text(
        f"""
        Good {time_of_day} Maeve!
        The weather today is {todays_weather['condition']['text']} and the 
        temperature is {todays_weather['feelslike_f']} degrees Fahrenheit.
        I love you so much. I am so proud of you. You are so cute and talented,
        and you are perfect just the way you are. Love, Daddy.
        """
    )


def button_release():
    logging.info("Maeve released the button")
    time.sleep(1)
    button_leds_off()


def setup():
    logging.basicConfig(level=logging.INFO)
    '''Setup button'''
    button.when_pressed = button_push
    button.when_released = button_release
    '''Setup button LEDs'''
    button_leds_off()
    logging.info("Sound Box initialized! Press the button to hear a personalized greeting.")


def main():
    try:
        setup()
        print("Sound box is running. Press CTRL+C to exit.")
        pause()
        # today = datetime.datetime.now()
        # weekday = today.weekday()
        # logging.info("Today is {}".format(today))
        # single_button_push()
        # while True: # Keep the program running
        #     time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program")
    finally:
        # GPIO.cleanup()  # Clean up GPIO on exit
        pass


if __name__ == "__main__":
    main()
