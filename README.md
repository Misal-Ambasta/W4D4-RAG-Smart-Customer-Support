# W4D4-RAG-Smart-Customer-Support

A Retrieval-Augmented Generation (RAG) Smart Customer Support Ticketing System MVP.

---

## Project Overview
This project is an end-to-end AI-powered customer support ticketing system. It uses FastAPI (Python) for the backend, React (Vite) for the frontend, Google Gemini via LangChain for LLM-powered answers, and ChromaDB for vector search.

Features:
- Submit, classify, and resolve support tickets
- RAG-powered answers using company knowledge base and past tickets
- Conversational chat on each ticket (multi-turn, context-aware)
- Modern, clean UI

## RAG Pipeline Details
- **Embedding:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Store:** ChromaDB
- **LLM:** Google Gemini 1.5 Flash via LangChain
- **Retrieval:** Top-k similar tickets + knowledge docs
- **Prompt:** Merges context with user query (and chat history if in chat mode)

## Setup & Run Instructions
1. Install Python dependencies (see `backend/requirements.txt`)
2. Install Node dependencies in `frontend/`
3. Set up `.env` files for API keys (see `.env.example`)
4. Start backend: `uvicorn main:app --reload` in `/backend`
5. Start frontend: `npm run dev` in `/frontend`

## API Usage Examples
- `POST /tickets` – Create a ticket
- `GET /tickets/{id}` – Get ticket details (with chat history)
- `POST /tickets/{id}/messages` – Chat with the RAG assistant on a ticket
- `GET /tickets/{id}/messages` – Fetch chat history
- `GET /health` – Health check

See [flow.md](./flow.md) for detailed request/response and backend flow diagrams.

## Chat Flow Explanation
- When you submit a ticket, the backend classifies it and generates a RAG answer.
- You can open a chat panel for any ticket and converse with the AI assistant.
- Each chat message is sent to the backend, which includes the full chat history in the RAG prompt for context-aware answers.

## API Contract & Swagger Docs
- All endpoints are documented interactively at `/docs` (FastAPI Swagger UI)
- Each endpoint includes sample requests and responses
- Example:
  - `POST /tickets` expects `{title, description, ...}` and returns `{ticket_id, classification, rag}`
  - `POST /tickets/{id}/messages` expects `{message}` and returns `{answer, confidence}`

---

For full backend flow and diagrams, see [flow.md](./flow.md).