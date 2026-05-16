from pyannote.audio import Pipeline
from app.config import HF_TOKEN

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=HF_TOKEN
)

def diarize(audio_path):
    diarization = pipeline(audio_path)
    return diarization