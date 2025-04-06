import logging
import os
import sys

from gtts import gTTS


def say_this_text(text):
    """Convert text to speech and play it"""
    try:
        # Create a temporary file for the audio
        audio_file = "/tmp/greeting.mp3"
        
        # Generate the speech audio file
        tts = gTTS(text=text, lang='en')
        tts.save(audio_file)
        
        # Play the audio file
        os.system(f"mpg123 {audio_file}")
        
        # Clean up the temporary file
        os.remove(audio_file)
    except Exception as e:
        print(f"Error with text-to-speech: {e}")
