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
from pi_rbg_led import (
    rainbow_on,
    rainbow_off,
    cleanup,
)
from text_to_speech import (
    generate_filepath,
    play_audio_file,
    say_this_text,
)


button = Button(24, pull_up=True, bounce_time=0.3) # light brown wire


def button_push():    
    logging.info("Maeve pushed the button!")
    rainbow_on()

    # Check for cached greeting
    logging.info("Checking for cached greetings..")
    audio_file_path = generate_filepath()
    if os.path.exists(audio_file_path):
        logging.info("Using cached greeting")
        play_audio_file(audio_file_path)
        rainbow_off()
        return

    logging.info("No cached greeting found, generating one on-demand")
    say_this_text(generate_greeting_text())
    rainbow_off()


def setup():
    logging.basicConfig(level=logging.INFO)
    button.when_pressed = button_push
    logging.info("Sound Box initialized! Press the button to hear a personalized greeting.")


def main():
    try:
        setup()
        print("Sound box is running. Press CTRL+C to exit.")
        pause()
    except KeyboardInterrupt:
        print("\nExiting program")
    finally:
        button.close()
        cleanup()


if __name__ == "__main__":
    main()
