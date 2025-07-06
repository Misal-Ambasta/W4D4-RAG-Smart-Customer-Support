import { useEffect, useState, useRef } from 'react';
import { getMessages, postMessage } from './api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatPanel({ ticketId, onClose }: { ticketId: string; onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getMessages(ticketId).then(setMessages).catch(console.error);
  }, [ticketId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function handleSend() {
    if (!input.trim()) return;
    const userText = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userText }]);
    setLoading(true);
    try {
      const resp = await postMessage(ticketId, userText);
      setMessages(prev => [...prev, { role: 'assistant', content: resp.answer }]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed right-6 bottom-6 w-80 max-h-[80vh] flex flex-col bg-white rounded-lg shadow-lg overflow-hidden z-50">
      <div className="flex items-center justify-between bg-blue-500 text-white px-4 py-2">
        <h3>Conversation for {ticketId}</h3>
        <button onClick={onClose}>✕</button>
      </div>
      <div className="flex-1 overflow-y-auto space-y-2 p-3 bg-gray-50">
        {messages.map((m, idx) => (
          <div key={idx} className={`rounded-lg px-3 py-2 text-sm whitespace-pre-line max-w-[85%] ${m.role === 'user' ? 'bg-blue-100 self-end' : 'bg-green-100 self-start'}`}>{m.content}</div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="flex gap-2 p-2 border-t bg-white">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
          className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button onClick={handleSend} disabled={loading || !input.trim()} className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-400">Send</button>
      </div>
    </div>
  );
}
