import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from textblob import TextBlob
import joblib
from text_preprocessing import preprocess_text

# Load tickets  
tickets = pd.read_csv('data/customer_support_tickets.csv')

# Train classifier for category
tickets['clean_text'] = tickets['description'].apply(preprocess_text)
X = tickets['clean_text']
y = tickets['category']

vectorizer = TfidfVectorizer()
clf = LogisticRegression(max_iter=200)
pipeline = make_pipeline(vectorizer, clf)
pipeline.fit(X, y)

# Save model
joblib.dump(pipeline, 'data/ticket_classifier.joblib')

def classify_ticket(text):
    clean = preprocess_text(text)
    category = pipeline.predict([clean])[0]
    return category

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return 'positive'
    elif polarity < -0.2:
        return 'negative'
    else:
        return 'neutral'

def compute_priority(category, sentiment):
    # Example: escalate negative/high-impact categories
    if sentiment == 'negative' or category in ['Payment', 'Shipping']:
        return 'High'
    return 'Medium'

def classify_and_score(text):
    category = classify_ticket(text)
    sentiment = analyze_sentiment(text)
    priority = compute_priority(category, sentiment)
    return {
        'category': category,
        'sentiment': sentiment,
        'priority': priority
    }

# Example usage:
# print(classify_and_score("My payment failed but money deducted"))
