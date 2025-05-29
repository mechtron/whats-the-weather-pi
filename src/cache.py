#!/usr/bin/env python3

import datetime
import time
import logging
import os
import glob
from pathlib import Path

from greeting import generate_greeting_text
from text_to_speech import (
    generate,
    generate_filepath,
)


def cache_this_hours_greeting():
    logging.info("Caching this hours greeting..")
    filepath = generate_filepath()
    message = generate_greeting_text()
    generate(message, filepath)


def clean_up_old_greetings():
    """Delete greeting files older than 24 hours from /tmp directory."""
    logging.info("Cleaning up old messages..")
    tmp_dir = Path("/tmp")
    current_time = time.time()
    max_age = 24 * 60 * 60  # 24 hours in seconds
    
    # Find all .wav files with 'greeting' prefix
    pattern = tmp_dir / "greeting*.wav"
    for file_path in glob.glob(str(pattern)):
        file_age = current_time - os.path.getmtime(file_path)
        if file_age > max_age:
            try:
                os.remove(file_path)
                logging.info(f"Deleted old greeting file: {file_path}")
            except OSError as e:
                logging.error(f"Error deleting file {file_path}: {e}")


def main():
    cache_this_hours_greeting()
    clean_up_old_greetings()


if __name__ == "__main__":
    main()
