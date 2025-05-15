import speech_recognition as sr
from .base import GOOGLE_SPEECH_API_KEYS

recognizer = sr.Recognizer()

async def stt(file_path: str):
    with sr.AudioFile(file_path) as source:
        error_message = ""
        audio_data = recognizer.record(source)

        for i, key in enumerate(GOOGLE_SPEECH_API_KEYS, start=1):
            try:
                text = recognizer.recognize_google_cloud(
                    audio_data, language_code="vi-VN",
                )
                return {"text": text}
            except sr.UnknownValueError:
                return {"error": "SCRAMBLED"}
            except sr.RequestError as e:
                error_message = str(e)
                if "403" in error_message:
                    print(
                        f"Key {i} seems invalid or has exceeded its quota. Retrying another..."
                    )
                    continue
                return {"error": "API_ERROR", "details": f"{e}"}
            except Exception as e:
                return {"error": "INTERNAL_SERVER_ERROR", "details": f"{e}"}

        return {"error": "API_QUOTA_EXCEEDED", "details": error_message}
