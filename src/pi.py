#!/usr/bin/env python3

import datetime
import time
import logging

from gpiozero import (
    Button,
    PWMLED,
)
from signal import pause

from text_to_speech import say_this_text
from weather import get_todays_weather


button = Button(12, pull_up=True)                   # blue wire
button_led_red = PWMLED(16, active_high=False)      # purple wire
button_led_green = PWMLED(20, active_high=False)    # grey wire
button_led_blue = PWMLED(21, active_high=False)     # white wire


def button_leds_off():
    button_led_red.off()
    button_led_green.off()
    button_led_blue.off()


def button_leds_pink():
    button_led_red.value = 1.0     # 100% red
    button_led_green.value = 0.0   # 0% green
    button_led_blue.value = 0.3    # 30% blue


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
    today = datetime.datetime.now()
    weekday = today.strftime("%A")
    todays_weather = get_todays_weather()
    say_this_text(
        f"""
        Good {time_of_day} Maeve! Today is {weekday} and the weather 
        is {todays_weather['condition']['text']} and the temperature is 
        {int(todays_weather['feelslike_f'])} degrees Fahrenheit. We love you 
        so much Maevey! We are proud of you. You are so cute and talented, 
        and you are perfect just the way you are! Love, Mommy and Daddy.
        """
    )


def button_release():
    logging.info("Maeve released the button")
    time.sleep(1)
    button_leds_off()


def setup():
    logging.basicConfig(level=logging.INFO)
    button.when_pressed = button_push
    button.when_released = button_release
    button_leds_off()
    logging.info("Sound Box initialized! Press the button to hear a personalized greeting.")


def main():
    try:
        setup()
        print("Sound box is running. Press CTRL+C to exit.")
        pause()
    except KeyboardInterrupt:
        print("\nExiting program")
    finally:
        # GPIO.cleanup()  # Clean up GPIO on exit
        pass


if __name__ == "__main__":
    main()
