from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import asyncio
from audio_processing import stt, ser, tts
import os
from tempfile import NamedTemporaryFile

class STTResponse(BaseModel):
    text: str | None = None
    error: str | None = None
    details: str | None = None

class SERResponse(BaseModel):
    emotion: str | None = None
    error: str | None = None
    details: str | None = None

class STTAndSERResponse(BaseModel):
    stt: STTResponse
    ser: SERResponse

class TTSRequest(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stt-and-ser", response_model=STTAndSERResponse)
async def route_stt_and_ser(file: UploadFile = File(...)):
    print("Received file for STT and SER")
    content = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(content)
        tmp.flush()
        tmp.seek(0)

        stt_result, ser_result = await asyncio.gather(
            stt(tmp.name),
            ser(tmp.name),
        )

        print(f"STT Result: {stt_result}")
        print(f"SER Result: {ser_result}")

        return STTAndSERResponse(
            stt=STTResponse(**stt_result),
            ser=SERResponse(**ser_result),
        )

import random

@app.post("/tts")
async def route_tts(request: TTSRequest, background_tasks: BackgroundTasks):
    text = request.text
    print(f"Received text for TTS: {text}")

    # Generate temporary file name using math random
    file_name = f"{tempfile.gettempdir()}/{random.randint(1000, 9999)}.mp3"

    tts(text, file_name)
    print(f"TTS File name: {file_name}")
    if file_name is None:
        raise Exception("TTS failed")
    
    background_tasks.add_task(os.remove, file_name)

    return FileResponse(
        file_name,
        media_type="audio/mpeg",
        filename=os.path.basename(file_name),
    )
