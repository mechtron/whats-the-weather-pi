import logging
import os
import platform
import sys

from gtts import gTTS


def get_audio_player(format="wav"):
    logging.info("Looking up OS audio player..")
    """Returns the appropriate audio player command based on the operating system.
    """
    system = platform.system().lower()
    if system == 'darwin':  # macOS
        return 'afplay'
    elif system == 'linux':
        if format == "wav":
            return 'aplay'
        else:
            return 'mpg123'
    else:
        raise OSError(f"Unsupported operating system: {system}")


def say_this_text(text):
    logging.info("Converting text to speech..")
    """Convert text to speech and play it"""
    try:
        # Create a temporary file for the audio
        audio_file = "/tmp/greeting.mp3"
        
        # Generate the speech audio file
        tts = gTTS(text=text, lang='en')
        tts.save(audio_file)
        
        # Play the audio file
        logging.info("Playing audio file..")
        audio_player = get_audio_player()
        os.system(f"{audio_player} {audio_file}")
        
        # Clean up the temporary file
        os.remove(audio_file)
    except Exception as e:
        print(f"Error with text-to-speech: {e}")
