import whisper

model = whisper.load_model("medium.en")
result = model.transcribe("harvard.wav")
print(result["text"])