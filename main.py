from dotenv import load_dotenv
load_dotenv()
import os
import speech_recognition as sr

GOOGLE_SPEECH_API_KEYS = os.getenv("GOOGLE_SPEECH_API_KEYS", [None]) or [None]
if type(GOOGLE_SPEECH_API_KEYS) == str:
    GOOGLE_SPEECH_API_KEYS = [*GOOGLE_SPEECH_API_KEYS.split(";"), None]
elif type(GOOGLE_SPEECH_API_KEYS) != list:
    raise ValueError("GOOGLE_SPEECH_API_KEYS must be a string containing a list of keys separated by semicolons ; got: %s" % GOOGLE_SPEECH_API_KEYS)

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile

class STTResponse(BaseModel):
    text: str | None = None
    error: str | None = None
    details: str | None = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/stt', response_model=STTResponse)
async def stt(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    content = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(content)
        tmp.flush()
        tmp.seek(0)

        with sr.AudioFile(tmp.name) as source:
            error_message = ""
            audio_data = recognizer.record(source)

            for i, key in enumerate(GOOGLE_SPEECH_API_KEYS, start=1):
                try:
                    text = recognizer.recognize_google(audio_data, language="vi-VN", key=key)
                    return { "text": text }
                except sr.UnknownValueError:
                    return { "error": "SCRAMBLED" }
                except sr.RequestError as e:
                    error_message = str(e)
                    if "403" in error_message:
                        print(f"Key {i} seems invalid or has exceeded its quota. Retrying another...")
                        continue
                    return { "error": "API_ERROR", "details": f"{e}" }
                except Exception as e:
                    return { "error": "INTERNAL_SERVER_ERROR", "details": f"{e}" }
            
            return { "error": "API_QUOTA_EXCEEDED", "details": error_message }
