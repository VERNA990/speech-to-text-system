import whisper
from pathlib import Path

# Load model once when server starts
print("Loading Whisper model...")
model = whisper.load_model("medium.en")
print("Whisper ready.")

def transcribe(audio_path: Path):
    """
    Convert speech to text using Whisper.
    """

    result = model.transcribe(str(audio_path))

    return result