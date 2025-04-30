from dotenv import load_dotenv
load_dotenv()
import os
import speech_recognition as sr

GOOGLE_SPEECH_API_KEY = os.getenv("GOOGLE_SPEECH_API_KEY", None) or None

class StreamedAudio(sr.AudioSource):
    def __init__(self):
        print("OK")

def listen_forever(stop_word: str = "tắt mô hình"):
    r = sr.Recognizer()

    with sr.Microphone() as source:
    # with StreamedAudio() as source:
        print("🔊 Đang chỉnh mic, đợi xíu nghen:))))")
        r.adjust_for_ambient_noise(source, duration=1)
        print("✅ Mời bạn nói:")

        while True:
            try:
                print("🎙️ Mời bạn nói")
                audio = r.listen(source, timeout=None)

                text = r.recognize_google(audio, language="vi-VN", key=GOOGLE_SPEECH_API_KEY)
                print("👤 Bạn -->", text)

                if stop_word.lower() in text.lower():
                    print("🛑 Phát hiện từ khóa dừng. Dừng chương trình.")
                    break

            except sr.UnknownValueError:
                print("🥹 Xin lỗi, tôi không nghe rõ. Bạn có thể nói lại khum ")
            except sr.RequestError as e:
                print(f"❌ Lỗi khi gọi dịch vụ (API) nhận dạng: {e}")


listen_forever()

# Bẻ từng file audio thành nhiều đoạn nhỏ hơn 1 phút

# Giới hạn thời lượng 1 file audio là 1 phút, nếu dài hơn sẽ bị lỗi
# 5 phút cần reconnect 1 lần
# tối đa 60p / tháng
