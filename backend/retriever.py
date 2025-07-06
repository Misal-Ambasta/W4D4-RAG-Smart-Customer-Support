from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from text_preprocessing import preprocess_text
import numpy as np
from typing import List, Tuple
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CHROMA_DIR = os.path.join(DATA_DIR, 'chroma_store')

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
tickets_collection = client.get_or_create_collection('tickets')
kb_collection = client.get_or_create_collection('knowledge')

def retrieve_similar_tickets(query: str, top_k: int = 5) -> List[Tuple[str, float]]:
    query_emb = model.encode([preprocess_text(query)])[0]
    results = tickets_collection.query(query_embeddings=[query_emb], n_results=top_k)
    ids = results['ids'][0]
    scores = results['distances'][0]
    return list(zip(ids, scores))

def retrieve_knowledge_context(query: str, top_k: int = 3) -> List[Tuple[str, float]]:
    query_emb = model.encode([preprocess_text(query)])[0]
    results = kb_collection.query(query_embeddings=[query_emb], n_results=top_k)
    ids = results['ids'][0]
    scores = results['distances'][0]
    return list(zip(ids, scores))

# Example usage:
# print(retrieve_similar_tickets("My order hasn't arrived", 5))
