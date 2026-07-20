from deep_translator import GoogleTranslator

def translate_to_english(text: str) -> str:
    try:
        if not text or not text.strip():
            return text
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        print(f"Translation warning: {e}")
        return text