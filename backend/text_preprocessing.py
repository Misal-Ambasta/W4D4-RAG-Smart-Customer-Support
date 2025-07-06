import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from typing import List
import re

nlp = spacy.load('en_core_web_sm')

def clean_text(text: str) -> str:
    # Basic cleaning: lower, remove special chars, collapse spaces
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_and_remove_stopwords(text: str) -> List[str]:
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

def detect_language(text: str) -> str:
    # spaCy doesn't support language detection out of the box; stub for extension
    return 'en'

def preprocess_text(text: str) -> str:
    cleaned = clean_text(text)
    tokens = tokenize_and_remove_stopwords(cleaned)
    return ' '.join(tokens)

# Example usage:
# print(preprocess_text("My order hasn't arrived!"))
