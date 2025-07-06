import { useEffect, useState } from 'react';
import TicketForm from './TicketForm';
import ChatPanel from './ChatPanel';
import TicketTable, { type Ticket } from './TicketTable';
import { getTicket } from './api';
import './App.css';

function App() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastCreatedId, setLastCreatedId] = useState<string | null>(null);
  const [chatTicketId, setChatTicketId] = useState<string | null>(null);

  // For MVP, fetch only the last created ticket and append (no full DB fetch API yet)
  useEffect(() => {
    if (lastCreatedId) {
      setLoading(true);
      getTicket(lastCreatedId)
        .then(ticket => {
          setTickets(prev => [ticket, ...prev]);
        })
        .catch(() => setError('Failed to fetch ticket'))
        .finally(() => setLoading(false));
    }
  }, [lastCreatedId]);

  return (
    <div className="container">
      <header>
        <h1>Smart Customer Support</h1>
        <p className="subtitle">AI-powered ticketing & smart response system</p>
      </header>
      <main>
        <div className="form-section">
          <TicketForm onTicketCreated={setLastCreatedId} />
        </div>
        {loading && <div className="loading">Loading ticket...</div>}
        {error && <div className="error">{error}</div>}
        <div className="table-section">
          <TicketTable tickets={tickets} onChat={setChatTicketId} />
        </div>
        {chatTicketId && <ChatPanel ticketId={chatTicketId} onClose={() => setChatTicketId(null)} />}
      </main>
      <footer>
        <p>Built with <b>FastAPI</b>, <b>LangChain</b>, <b>Gemini</b>, <b>ChromaDB</b>, <b>React</b></p>
      </footer>
    </div>
  );
}

export default App;
