from langchain_google_genai import GoogleGenerativeAI
from retriever import retrieve_similar_tickets, retrieve_knowledge_context
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

llm = GoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=GEMINI_API_KEY
)

def get_rag_answer(ticket_text: str, history: list[dict] | None = None):
    # Retrieve context from tickets and knowledge base
    similar_tickets = retrieve_similar_tickets(ticket_text, top_k=3)
    knowledge_context = retrieve_knowledge_context(ticket_text, top_k=2)
    context_docs = [doc_id for doc_id, _ in similar_tickets + knowledge_context]
    # Compose context string (in prod, fetch doc text by id)
    context = "\n".join(context_docs)
        # Include prior messages in context if provided
    history_context = ""
    if history:
        for msg in history[-6:]:  # include last 6 exchanges max
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_context += f"\n{role.title()}: {content}"

    # Compose RAG prompt
    prompt = f"""
    Conversation so far:{history_context}

Customer Query: {ticket_text}
    Context:
    {context}
    Provide a helpful, accurate, and concise response based on the above context.
    """
    answer = llm(prompt)
    # Confidence scoring (stub: based on LLM output length)
    confidence = min(1.0, max(0.5, len(answer) / 200))
    return {
        'answer': answer,
        'confidence': confidence,
        'context_ids': context_docs
    }

# Example usage:
# print(get_rag_answer("My payment failed but money deducted"))
