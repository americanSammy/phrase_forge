# utils.py
import re

def extract_words_from_text(text):
    if text:
        return re.findall(r"\b(?:[a-zA-Z]{2,}(?:'\w{1,2})?)\b", text.lower())
    return []
