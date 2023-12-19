# translator.py
from deep_translator import GoogleTranslator

class Translator:
    @staticmethod
    def translate_to_language(words, language):
        translator = GoogleTranslator(source='auto', target=language.lower())
        return [translator.translate(word[0]) for word in words]
