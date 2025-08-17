import base64
import datetime
import logging
import mimetypes
import os
from pathlib import Path
import platform
import re
import struct
import pytz

from dotenv import load_dotenv
from google import genai
from google.genai import types


file_dir = Path(__file__).parent
load_dotenv(file_dir / '.env')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")


def get_wav_audio_player():
    logging.info("Looking up OS audio player..")
    """
    Returns the appropriate audio player command based on the operating system.
    """
    system = platform.system().lower()
    if system == 'darwin':  # macOS
        return 'afplay'
    elif system == 'linux':
        return 'aplay'
    else:
        raise OSError(f"Unsupported operating system: {system}")


def save_binary_file(file_name, data):
    logging.info(f"Saving file to {file_name}..")
    f = open(file_name, "wb")
    f.write(data)
    f.close()


def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys. Values will be
        integers if found, otherwise None.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the WAV file header.
    """
    logging.info("Converting to WAV file..")
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data


def generate(text, audio_file_path):
    try:
        logging.info("Generating text to speech using Gemini..")
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-2.5-flash-preview-tts"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=text),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1.3,
            response_modalities=[
                "audio",
            ],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            ),
        )

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            if chunk.candidates[0].content.parts[0].inline_data:
                file_name = audio_file_path
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                data_buffer = inline_data.data
                file_extension = mimetypes.guess_extension(inline_data.mime_type)
                if file_extension is None:
                    file_extension = ".wav"
                    data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
                save_binary_file(audio_file_path, data_buffer)
            else:
                print(chunk.text)
    except Exception as e:
        logging.error(f"Error generating text to speech: {e}")


def generate_filepath():
    """
    Generates a filepath with an epoch timestamp suffix (in hours).
    The filename will be in the format 'greeting_17167000.wav'.
    """
    pst = pytz.timezone('US/Pacific')
    now_pst = datetime.datetime.now(pst)
    epoch_seconds = int(now_pst.timestamp())
    epoch_hours = epoch_seconds // 3600 # integer division to get whole hours
    return f"/tmp/greeting_{epoch_hours}.wav"


def play_audio_file(audio_file_path):
    logging.info("Playing audio file..")
    audio_player = get_wav_audio_player()
    os.system(f"{audio_player} {audio_file_path}")


def say_this_text(text):
    audio_file_path = generate_filepath()
    generate(text, audio_file_path)
    play_audio_file(audio_file_path)

