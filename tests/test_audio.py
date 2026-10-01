from app.audio.transcriber import SpeechToText


transcriber = SpeechToText()

text = transcriber.transcribe("quero.mp3")

print("Transcription:")
print(text)