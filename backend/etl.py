import os
import pandas as pd
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'
TICKETS_CSV = DATA_DIR / 'customer_support_tickets.csv'
KNOWLEDGE_JSON = DATA_DIR / 'company_knowledge_base.json'
DB_PATH = DATA_DIR / 'support.db'

def load_tickets_to_sqlite():
    df = pd.read_csv(TICKETS_CSV)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('tickets', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Tickets loaded to {DB_PATH} (table: tickets)")

def load_knowledge_to_sqlite():
    import json
    with open(KNOWLEDGE_JSON, 'r') as f:
        kb = json.load(f)
    conn = sqlite3.connect(DB_PATH)
    # Flatten policies, products, faqs into a single table for demo
    kb_entries = []
    for section in kb:
        for key, entry in kb[section].items():
            kb_entries.append({
                'section': section,
                'key': key,
                'title': entry.get('title', key),
                'content': entry.get('content', '')
            })
    pd.DataFrame(kb_entries).to_sql('knowledge_base', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Knowledge base loaded to {DB_PATH} (table: knowledge_base)")

if __name__ == '__main__':
    load_tickets_to_sqlite()
    load_knowledge_to_sqlite()
