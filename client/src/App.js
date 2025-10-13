import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState('light'); // New state for theme
  const chatWindowRef = useRef(null);

  // Scroll to the bottom of the chat window when messages change
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  // Load theme from localStorage on mount (optional)
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.className = savedTheme;
  }, []);

  // Handle theme change
  const handleThemeChange = (e) => {
    const selectedTheme = e.target.value;
    setTheme(selectedTheme);
    localStorage.setItem('theme', selectedTheme); // Save theme to localStorage (optional)
    document.documentElement.className = selectedTheme;
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: 'user' };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/chat', { message: input });
      setMessages((prev) => [...prev, { text: response.data.response, sender: 'bot' }]);
    } catch (error) {
      console.error('Error fetching bot response:', error);
      setMessages((prev) => [
        ...prev,
        { text: `Sorry, something went wrong: ${error.message || 'Unknown error'}`, sender: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && e.target.value.trim()) {
      e.preventDefault();
      handleSend();
    } else if (e.key === 'Enter' && e.shiftKey) {
      e.preventDefault();
      setInput(input + '\n');
    }
  };

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className={`app-container ${theme}`}> {/* Apply theme class to app-container */}
      <button
        aria-label="Toggle sidebar"
        className="sidebar-toggle"
        onClick={toggleSidebar}
      >
        ☰
      </button>
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <h2>Settings</h2>
        <ul>
          <li>
            Theme:
            <select value={theme} onChange={handleThemeChange}>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </li>
          <li>Model: Llama-3.1</li>
        </ul>
      </div>
      <div className="chat-container">
        <h1 className="app-header">BUddy: Your AI Guide</h1>
        <div className="chat-window" ref={chatWindowRef}>
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <div className="message-bubble">
                {msg.text.split('\n').map((line, i) => (
                  <div key={i}>{line}</div>
                ))}
              </div>
            </div>
          ))}
          {isLoading && <div className="loading">Thinking...</div>}
        </div>
        <div className="input-area">
          <textarea
            aria-label="Chat input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about HKBU... (Press Shift + Enter for new line)"
            rows="3"
            style={{ resize: 'vertical' }}
          />
          <button onClick={handleSend} aria-label="Send message">
            <img src="Send.png" alt="Send Icon" className="button-icon" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;