from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import asyncio
from audio_processing import stt, ser

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stt-and-ser", response_model=STTAndSERResponse)
async def route_stt_and_ser(file: UploadFile = File(...)):
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
