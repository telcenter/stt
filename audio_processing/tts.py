import os
import time

import edge_tts
from gtts import gTTS  # pip install gTTS


def tts(text: str, file_name: str) -> str | None:
    """
    Convert text to speech using gTTS first,
    fallback to edge-tts if gTTS fails.

    Returns the temporary file name
    """
    start_time = time.time()

    try:
        try:
            tts = gTTS(text=text, lang="vi", slow=False)
            tts.save(file_name)
            print("✅ Đã chuyển đổi thành công bằng gTTS!")
            return
        except Exception as e:
            print(f"⚠️ gTTS bị lỗi: {e}")
            print("🔄 Đang chuyển sang dùng edge-tts...")

            try:
                communicate = edge_tts.Communicate(
                    text=text, voice="vi-VN-HoaiMyNeural"
                )
                communicate.save_sync(file_name)
            except Exception as edge_error:
                print(f"❌ edge-tts cũng bị lỗi: {edge_error}")
                raise edge_error
    finally:
        print(f"⏱️ Thời gian thực hiện: {time.time() - start_time:.2f} giây")


# The API input limit to TTS models is currently 4096 characters
