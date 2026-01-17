from deep_translator import GoogleTranslator, single_detection
from django.conf import settings

def translate_to_hindi(text):
    """Translate English text to Hindi using Google Translate."""
    try:
        translation = GoogleTranslator(source='auto', target='hi').translate(text)
        return translation
    except Exception as e:
        print(f"Translation error HI: {e}")
        return text

def translate_to_english(text):
    """Translate Hindi text to English using Google Translate."""
    try:
        translation = GoogleTranslator(source='auto', target='en').translate(text)
        return translation
    except Exception as e:
        print(f"Translation error EN: {e}")
        return text

def detect_language(text):
    """Language detection error: 'GoogleTranslator' object has no attribute 'detect'.
        limit it to en and hi
    """
    try:
        lang_code = single_detection(text, api_key=settings.DETECTLENGUAGE_API_KEY)
        if lang_code not in ['hi', 'bh']:
            return 'hi'
        return 'en'
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'hi'