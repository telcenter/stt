from dotenv import load_dotenv

load_dotenv()
import os

GOOGLE_SPEECH_API_KEYS = os.getenv("GOOGLE_SPEECH_API_KEYS", [None]) or [None]
if type(GOOGLE_SPEECH_API_KEYS) == str:
    GOOGLE_SPEECH_API_KEYS = [*GOOGLE_SPEECH_API_KEYS.split(";"), None]
elif type(GOOGLE_SPEECH_API_KEYS) != list:
    raise ValueError(
        "GOOGLE_SPEECH_API_KEYS must be a string containing a list of keys separated by semicolons ; got: %s"
        % GOOGLE_SPEECH_API_KEYS
    )
