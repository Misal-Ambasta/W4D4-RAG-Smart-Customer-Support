import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export async function createTicket(ticket: {
  title: string;
  description: string;
  customer_name?: string;
  customer_email?: string;
}) {
  const res = await axios.post(`${API_BASE}/tickets`, ticket);
  return res.data;
}

export async function getTicket(ticket_id: string) {
  const res = await axios.get(`${API_BASE}/tickets/${ticket_id}`);
  return res.data;
}

export async function getMessages(ticketId: string) {
  const res = await axios.get(`${API_BASE}/tickets/${ticketId}/messages`);
  return res.data;
}

export async function postMessage(ticketId: string, message: string) {
  const res = await axios.post(`${API_BASE}/tickets/${ticketId}/messages`, { message });
  return res.data;
}

export async function getHealth() {
  const res = await axios.get(`${API_BASE}/health`);
  return res.data;
}
