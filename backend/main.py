from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import uuid
import os
from dotenv import load_dotenv
from text_preprocessing import preprocess_text
from ticket_classifier import classify_and_score
from rag_pipeline import get_rag_answer

load_dotenv()

app = FastAPI()

# CORS middleware for frontend-backend integration (allow all for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory ticket store for MVP (replace with DB in prod)
tickets_df = pd.read_csv('data/customer_support_tickets.csv')
TICKET_ID_FIELD = 'ticket_id'

class TicketCreate(BaseModel):
    title: str
    description: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None

@app.post('/tickets')
def create_ticket(ticket: TicketCreate):
    # Preprocess
    text = ticket.description
    classification = classify_and_score(text)
    rag = get_rag_answer(text)
    # Generate new ticket ID
    new_id = f"TK-{uuid.uuid4().hex[:8].upper()}"
    ticket_data = {
        TICKET_ID_FIELD: new_id,
        'title': ticket.title,
        'description': ticket.description,
        'customer_name': ticket.customer_name,
        'customer_email': ticket.customer_email,
        'category': classification['category'],
        'sentiment': classification['sentiment'],
        'priority': classification['priority'],
        'status': 'Open',
        'resolution': rag['answer'],
        'confidence': rag['confidence']
    }
    global tickets_df
    tickets_df = pd.concat([tickets_df, pd.DataFrame([ticket_data])], ignore_index=True)
        # Initialize chat history
    messages_store[new_id] = [
        {"role": "user", "content": text},
        {"role": "assistant", "content": rag['answer']}
    ]
    return {'ticket_id': new_id, 'classification': classification, 'rag': rag}

# In-memory chat history {ticket_id: [ {role, content, timestamp} ] }
messages_store: dict[str, list[dict]] = {}

@app.get('/tickets/{ticket_id}')
def get_ticket(ticket_id: str):
    ticket = tickets_df[tickets_df[TICKET_ID_FIELD] == ticket_id]
    if ticket.empty:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # Convert single row to dict and sanitize values
    raw_record = ticket.iloc[0].to_dict()
    import math
    cleaned = {}
    for key, val in raw_record.items():
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            cleaned[key] = None
        else:
            cleaned[key] = val
    cleaned["messages"] = messages_store.get(ticket_id, [])
    return cleaned

@app.post('/tickets/{ticket_id}/messages')
def post_message(ticket_id: str, payload: dict):
    user_msg = payload.get('message')
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message required")
    if ticket_id not in tickets_df[TICKET_ID_FIELD].values:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # Append user message
    history = messages_store.setdefault(ticket_id, [])
    history.append({"role": "user", "content": user_msg})
    # Generate RAG reply
    rag = get_rag_answer(user_msg, history)
    history.append({"role": "assistant", "content": rag['answer']})
    return {"answer": rag['answer'], "confidence": rag['confidence']}

@app.get('/tickets/{ticket_id}/messages')
def get_messages(ticket_id: str):
    if ticket_id not in messages_store:
        raise HTTPException(status_code=404, detail="No messages for ticket")
    return messages_store[ticket_id]

@ app.get('/health')
def health():
    return {'status': 'ok'}
