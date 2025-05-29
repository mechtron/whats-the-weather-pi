#!/usr/bin/env python3

import time
import logging
import os

from gpiozero import (
    Button,
    PWMLED,
)
from signal import pause

from greeting import generate_greeting_text
from text_to_speech import (
    generate_filepath,
    play_audio_file,
    say_this_text,
)


button = Button(12, pull_up=True)                   # purple wire
button_led_red = PWMLED(16, active_high=False)      # blue wire
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


def button_push():
    logging.info("Maeve pushed the button")
    button_leds_pink()

    # Check for cached message
    audio_file_path = generate_filepath()
    if os.path.exists(audio_file_path):
        logging.info("Using cached message")
        play_audio_file(audio_file_path)
        return

    say_this_text(generate_greeting_text())


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
