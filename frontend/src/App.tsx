import { useState, useEffect, useCallback } from 'react';
import useWebSocket from 'react-use-websocket';
import './App.css';

const SOCKET_URL = 'ws://localhost:8000/ws';

function App() {
  const [message, setMessage] = useState('');
  const [messageHistory, setMessageHistory] = useState<string[]>([]);

  const { sendMessage, lastMessage } = useWebSocket(SOCKET_URL, {
    shouldReconnect: () => true,
  });

  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => [...prev, lastMessage.data]);
    }
  }, [lastMessage, setMessageHistory]);

  const handleSendMessage = useCallback(() => {
    if (message) {
      sendMessage(message);
      setMessage('');
    }
  }, [message, sendMessage]);

  return (
    <div>
      <h1>React WebSocket Chat</h1>
      <div>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
        />
        <button onClick={handleSendMessage} disabled={!message}>
          Send
        </button>
      </div>
      <h2>Message History</h2>
      <ul>
        {messageHistory.map((msg, idx) => (
          <li key={idx}>{msg}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
