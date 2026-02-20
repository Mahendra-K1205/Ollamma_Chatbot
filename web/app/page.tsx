'use client';

import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState('llama3.2:latest');

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: input, 
          model,
          history: messages 
        })
      });

      const data = await res.json();
      
      if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
      } else {
        setMessages(prev => [...prev, { role: 'error', content: data.error }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'error', content: 'Connection failed' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">🤖 Ollama Chatbot</h1>
        
        <div className="mb-4">
          <select 
            value={model} 
            onChange={(e) => setModel(e.target.value)}
            className="bg-gray-800 px-4 py-2 rounded"
          >
            <option value="llama3.2:latest">Llama 3.2</option>
            <option value="mistral:latest">Mistral</option>
            <option value="codellama:latest">CodeLlama</option>
          </select>
        </div>

        <div className="bg-gray-800 rounded-lg p-4 h-96 overflow-y-auto mb-4">
          {messages.map((msg, i) => (
            <div key={i} className={`mb-4 ${msg.role === 'user' ? 'text-blue-400' : msg.role === 'error' ? 'text-red-400' : 'text-green-400'}`}>
              <strong>{msg.role === 'user' ? 'You' : msg.role === 'error' ? 'Error' : 'Bot'}:</strong>
              <p className="mt-1">{msg.content}</p>
            </div>
          ))}
          {loading && <div className="text-yellow-400">Thinking...</div>}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 bg-gray-800 px-4 py-2 rounded"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-blue-600 px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-600"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
