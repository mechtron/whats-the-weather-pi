#!/usr/bin/env python3

import datetime
import time
import logging
import os

import RPi.GPIO as GPIO

from text_to_speech import say_this_text
from weather import get_todays_weather


BUTTON_PIN = 17  # BCM pin numbering (physical pin 11)


def single_button_push():
    logging.info("Maeve pushed the button once")
    todays_weather = get_todays_weather()
    say_this_text(
        f"""
        Hi Maeve, how are you today? 
        The weather today is {todays_weather['cloud_cover']} 
        with a high of {todays_weather['high']} 
        and a low of {todays_weather['low']}.
        I love you so much. I am so proud of you. 
        You are so smart and talented. 
        You are perfect just the way you are.
        Love, Daddy.
        """
    )


def button_callback(channel):
    """Function called when button is pressed"""
    print("Button pressed! Creating greeting...")
    single_button_push()


def setup():
    logging.basicConfig(level=logging.INFO)
    """Initialize GPIO and other settings"""
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Set up button pin as input with pull-down resistor
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Sound Box initialized! Press the button to hear a personalized greeting.")


def main():
    try:
        setup()
        # Add event detection for button press
        GPIO.add_event_detect(
            BUTTON_PIN, 
            GPIO.RISING, 
            callback=button_callback, 
            bouncetime=2000, # Debounce of 2 seconds
        )
        print("Sound box is running. Press CTRL+C to exit.")
        today = datetime.datetime.now()
        weekday = today.weekday()
        logging.info("Today is {}".format(today))
        single_button_push()
        while True: # Keep the program running
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit


if __name__ == "__main__":
    main()
