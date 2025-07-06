import React, { useState } from 'react';
import { createTicket } from './api';

export default function TicketForm({ onTicketCreated }: { onTicketCreated: (ticketId: string) => void }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const resp = await createTicket({
        title,
        description,
        customer_name: customerName,
        customer_email: customerEmail,
      });
      onTicketCreated(resp.ticket_id);
      setTitle(''); setDescription(''); setCustomerName(''); setCustomerEmail('');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to submit ticket');
    } finally {
      setLoading(false);
    }
  }

  function populateSample() {
    setTitle('Unable to track my order');
    setDescription('I placed an order last week but the tracking link is not updating. Can you help?');
    setCustomerName('Alex Doe');
    setCustomerEmail('alex.doe@example.com');
  }

  return (
    <form className="ticket-form" onSubmit={handleSubmit}>
      <h2>Submit a Support Ticket</h2>
      <button type="button" onClick={populateSample} style={{ marginBottom: 8 }}>Fill with Sample Data</button>
      <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" required />
      <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Describe your issue" required />
      <input value={customerName} onChange={e => setCustomerName(e.target.value)} placeholder="Your Name (optional)" />
      <input value={customerEmail} onChange={e => setCustomerEmail(e.target.value)} placeholder="Your Email (optional)" type="email" />
      <button type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Submit Ticket'}</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}
