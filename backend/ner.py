import spacy
from typing import List, Dict

nlp = spacy.load('en_core_web_sm')

# Example entity types: ORG, PRODUCT, GPE, DATE, etc.
def extract_named_entities(text: str) -> List[Dict]:
    doc = nlp(text)
    return [
        {'text': ent.text, 'label': ent.label_}
        for ent in doc.ents
    ]

# Example usage:
# print(extract_named_entities("Order #12345 for Apple MacBook shipped on July 5th to New York."))
