import os
from pathlib import Path

from dotenv import load_dotenv

file_dir = Path(__file__).parent
load_dotenv(file_dir / ".env")

# API keys (set in .env on each Pi)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Per-sound-box settings
CHILD_NAME = os.getenv("CHILD_NAME", "Maeve")
VOICE_NAME = os.getenv("VOICE_NAME", "Kore")
LOCATION = os.getenv("LOCATION", "LAGUNA_HILLS")
CLOSING_MESSAGE = os.getenv(
    "CLOSING_MESSAGE",
    "We love you so much Maevey! We are proud of you. You are so cute and talented, "
    "and you are perfect just the way you are! Love, Mommy and Daddy.",
)


def validate_api_keys():
    if not WEATHER_API_KEY:
        raise ValueError("WEATHER_API_KEY environment variable is not set")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set")
