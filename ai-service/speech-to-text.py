import whisper

print("Loading Whisper model...")

model = whisper.load_model("medium.en")
print("Model loaded, Transcribing...")
result = model.transcribe("samples/harvard.wav")

print("\nTRANSCRIPTION:")
print(result["text"])