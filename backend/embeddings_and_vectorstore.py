from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'
DB_PATH = DATA_DIR / 'support.db'
TICKETS_CSV = DATA_DIR / 'customer_support_tickets.csv'
KNOWLEDGE_JSON = DATA_DIR / 'company_knowledge_base.json'
CHROMA_DIR = DATA_DIR / 'chroma_store'

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up Chroma
client = chromadb.Client(Settings(
    persist_directory=str(CHROMA_DIR)
))

# Utility: load and preprocess text
import json
from text_preprocessing import preprocess_text

def load_ticket_texts():
    df = pd.read_csv(TICKETS_CSV)
    return df['description'].tolist(), df['ticket_id'].tolist()

def load_knowledge_texts():
    with open(KNOWLEDGE_JSON, 'r') as f:
        kb = json.load(f)
    docs = []
    ids = []
    for section in kb:
        for key, entry in kb[section].items():
            docs.append(entry.get('content', ''))
            ids.append(f'{section}:{key}')
    return docs, ids

def compute_and_store_embeddings():
    # Tickets
    ticket_texts, ticket_ids = load_ticket_texts()
    ticket_texts = [preprocess_text(t) for t in ticket_texts]
    ticket_embs = model.encode(ticket_texts, show_progress_bar=True)
    # Knowledge
    kb_texts, kb_ids = load_knowledge_texts()
    kb_texts = [preprocess_text(t) for t in kb_texts]
    kb_embs = model.encode(kb_texts, show_progress_bar=True)
    # Store in Chroma
    tickets_collection = client.get_or_create_collection('tickets')
    tickets_collection.upsert(list(zip(ticket_ids, ticket_embs.tolist())))
    kb_collection = client.get_or_create_collection('knowledge')
    kb_collection.upsert(list(zip(kb_ids, kb_embs.tolist())))
    print("Embeddings computed and stored in Chroma DB.")

if __name__ == '__main__':
    compute_and_store_embeddings()
