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

button = Button(21, pull_up=True, bounce_time=0.2) # light brown wire

# State-based button control
is_playing_audio = False


def button_push():
    global is_playing_audio
    
    # Prevent new button presses if audio is currently playing
    if is_playing_audio:
        logging.info("Button press ignored - audio is currently playing")
        return
    
    logging.info("Maeve pushed the button!")
    rainbow_on()

    # Check for cached greeting
    logging.info("Checking for cached greetings..")
    audio_file_path = generate_filepath()
    if os.path.exists(audio_file_path):
        logging.info("Using cached greeting")
        is_playing_audio = True
        play_audio_file(audio_file_path)
        rainbow_off()
        is_playing_audio = False
        return

    logging.info("No cached greeting found, generating one on-demand")
    is_playing_audio = True
    say_this_text(generate_greeting_text())
    rainbow_off()
    is_playing_audio = False


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
