

export interface Ticket {
  ticket_id: string;
  title: string;
  description: string;
  category: string;
  sentiment: string;
  priority: string;
  status: string;
  resolution: string;
  confidence: number;
}

export default function TicketTable({ tickets, onChat }: { tickets: Ticket[]; onChat: (id: string) => void }) {
  return (
    <div className="ticket-table-wrapper">
      <h2>All Tickets</h2>
      <table className="ticket-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Category</th>
            <th>Sentiment</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Confidence</th>
            <th>Resolution</th>
            <th>Chat</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map(ticket => (
            <tr key={ticket.ticket_id}>
              <td>{ticket.ticket_id}</td>
              <td>{ticket.title}</td>
              <td>{ticket.category}</td>
              <td>{ticket.sentiment}</td>
              <td>{ticket.priority}</td>
              <td>{ticket.status}</td>
              <td>{(ticket.confidence * 100).toFixed(1)}%</td>
              <td style={{ maxWidth: 300, whiteSpace: 'pre-line' }}>{ticket.resolution}</td>
              <td><button onClick={() => onChat(ticket.ticket_id)}>Chat</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
