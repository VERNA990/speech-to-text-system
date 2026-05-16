from app.services.transcription_service import transcribe
from app.services.diarization_service import diarize

def align(transcripts, speakers):

    final = []

    for segment in transcripts:
        speaker = "Unknown"

        for spk in speakers:
            if spk["start"] <= segment["start"] <= spk["end"]:
                speaker = spk["speaker"]
                break

        final.append({
            "speaker": speaker,
            "text": segment["text"],
            "start": segment["start"],
            "end": segment["end"]
        })

    return final


def process_audio(audio_path):

    print("Running diarization...")
    speakers = diarize(audio_path)

    print("Running transcription...")
    transcripts = transcribe(audio_path)

    print("Aligning...")
    result = align(transcripts, speakers)

    return result