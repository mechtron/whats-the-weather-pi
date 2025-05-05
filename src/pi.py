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


button = Button(22, pull_up=True)  # GPIO22 with internal pull-up
button_led_red = PWMLED(16)
button_led_green = PWMLED(20)
button_led_blue = PWMLED(21)


def button_leds_off():
    # Note: button LEDs are active low, .on() means LEDs off
    button_led_red.on()
    button_led_green.on()
    button_led_blue.on()


def button_leds_pink():
    button_led_red.value = 0.0     # 100% red
    button_led_green.value = 1.0   # 0% green
    button_led_blue.value = 0.7    # 30% blue


def button_push():
    logging.info("Maeve pushed the button")
    button_leds_pink()
    # todays_weather = get_todays_weather()
    # say_this_text(
    #     f"""
    #     Hi Maeve, how are you today? 
    #     The weather today is {todays_weather['cloud_cover']} 
    #     with a high of {todays_weather['high']} 
    #     and a low of {todays_weather['low']}.
    #     I love you so much. I am so proud of you. 
    #     You are so smart and talented. 
    #     You are perfect just the way you are.
    #     Love, Daddy.
    #     """
    # )


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
