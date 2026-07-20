import speech_recognition as sr

LANGUAGES_MAP = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Italian": "it-IT",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Chinese": "zh-CN",
    "Russian": "ru-RU",
    "Portuguese": "pt-PT",
    "Arabic": "ar-SA"
}

def listen(language="English") -> str:
    r = sr.Recognizer()
    lang_code = LANGUAGES_MAP.get(language, "en-IN")
    try:
        import pyaudio
    except ImportError:
        return "Error: PyAudio dependencies are missing. Please check your system's PortAudio configurations."

    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1.0)
            print(f"Listening (timeout 8s, language: {language})...")
            audio = r.listen(source, timeout=8.0, phrase_time_limit=8.0)
        print("Recognizing content...")
        text = r.recognize_google(audio, language=lang_code)
        return text
    except sr.WaitTimeoutError:
        return "Error: Speech recognition timed out. No speech was detected."
    except sr.UnknownValueError:
        return "Error: Speech recognition was unable to understand your input."
    except Exception as e:
        return f"Error: {e}"