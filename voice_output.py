import threading
import tempfile
import os
import re
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import pyttsx3

GTTS_LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Russian": "ru",
    "Portuguese": "pt",
    "Arabic": "ar"
}

def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)  # Strip HTML tags
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Strip Markdown links
    text = re.sub(r'[*_`#~]', '', text)  # Strip formatting marks
    text = re.sub(r'https?://\S+', '', text)  # Strip URLs
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)  # Strip unusual characters
    return text.strip()[:500]

def speak_sync(text: str, language: str = "English"):
    cleaned = clean_text(text)
    if not cleaned:
        return

    # Translate if target language is not English
    if language != "English":
        try:
            target_code = GTTS_LANG_CODES.get(language, "en")
            cleaned = GoogleTranslator(source="auto", target=target_code).translate(cleaned)
        except Exception as e:
            print(f"Translation warning: {e}")

    # Generate and run with gTTS
    try:
        lang_code = GTTS_LANG_CODES.get(language, "en")
        tts = gTTS(text=cleaned, lang=lang_code, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
        tts.save(temp_path)
        playsound.playsound(temp_path)
        try:
            os.remove(temp_path)
        except Exception:
            pass
        return
    except Exception as e:
        print(f"gTTS or playsound issue: {e}. Redirecting to system fallback (pyttsx3).")

    # Final fallback: pyttsx3
    try:
        engine = pyttsx3.init()
        engine.say(cleaned)
        engine.runAndWait()
    except Exception as py_err:
        print(f"pyttsx3 fallback also failed: {py_err}")

def speak(text: str, language: str = "English"):
    t = threading.Thread(target=speak_sync, args=(text, language))
    t.daemon = True
    t.start()