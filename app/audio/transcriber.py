import whisper


class SpeechToText:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe(self, audio_path: str) -> str:
        result = self.model.transcribe(
            audio_path,
            language="pt",
        )

        return result["text"].strip()