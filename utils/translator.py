from deep_translator import GoogleTranslator

def translate_to_hindi(text):
    """Translate English text to Hindi using Google Translate."""
    try:
        translation = GoogleTranslator(source='en', target='hi').translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return text