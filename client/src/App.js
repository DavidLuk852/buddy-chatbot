import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState('light');
  const [fontSize, setFontSize] = useState(14);
  const [linksOpen, setLinksOpen] = useState(false);
  const chatWindowRef = useRef(null);

  // Scroll to the bottom of the chat window when messages change
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
      console.log("Scrolled to bottom");
    }
  }, [messages]);

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.className = savedTheme;
  }, []);

  // Handle theme change
  const handleThemeChange = (e) => {
    const selectedTheme = e.target.value;
    setTheme(selectedTheme);
    localStorage.setItem('theme', selectedTheme);
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

  const toggleLinks = () => setLinksOpen(prev => !prev);

  
  // Slider handler – clamp between 12px and 22px
  const handleFontSizeChange = (e) => {
    const newSize = Number(e.target.value);
    setFontSize(newSize);
  };

  // Useful links data
  const usefulLinks = [
    {
      title: 'BUniPort',
      url: "https://buniport.hkbu.edu.hk",
    },
    {
      title: 'HKBU Moodle',
      url: "https://chtl-bu.hkbu.edu.hk/elearning",
    },
    {
      title: 'HKBU Library Opening Hours',
      url: 'https://library.hkbu.edu.hk/using-the-library/opening-hours/regular-service-hours/',
    },
    {
      title: 'HKBU Course Add/Drop',
      url: 'https://ar.hkbu.edu.hk/student-services/new-student-orientation/study/course-add-drop-for-new-students',
    },
    {
      title: 'HKBU Course Pre-registration',
      url: 'https://ar.hkbu.edu.hk/student-services/course-registration/pre-registration',
    },
    {
      title: 'HKBU Academic Calendar',
      url: 'https://ar.hkbu.edu.hk/academic-calendar/monthly',
    },
    {
      title: 'HKBU Bad Weather Arrangement',
      url: 'https://ar.hkbu.edu.hk/student-services/useful-information/bad-weather-arrangement',
    },
    {
      title: 'HKBU Campus Map',
      url: "https://aao.hkbu.edu.hk/homecoming2018/filemanager/content/HKBU_campus_map.pdf",
    },
    {
      title: 'Applications and Forms (Current Students)',
      url: 'https://ar.hkbu.edu.hk/student-services/useful-information/applications-and-forms-student-services',
    },
    {
      title: 'Follow-U-Print Printing Services',
      url: 'https://ito.hkbu.edu.hk/services/printing-services.html',
    },
    {
      title: 'Wi-Fi & Network Access',
      url: 'https://ito.hkbu.edu.hk/services/wi-fi-network-access.html',
    },
  ];

  return (
    <div className={`app-container ${theme} ${sidebarOpen ? 'sidebar-open' : ''}`}>
      <button
        aria-label="Toggle sidebar"
        className="sidebar-toggle"
        onClick={toggleSidebar}
      >
        ☰
      </button>

      {/* ---------- TOGGLE BUTTON FOR USEFUL LINKS ---------- */}
      <button
        aria-label="Toggle useful links"
        className="links-toggle"
        onClick={toggleLinks}
      >
        <span className="icon-arrow-left"></span>
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
      
      <div className={`links-sidebar ${linksOpen ? 'open' : ''}`}>
        <h2>Useful Links</h2>
        <ul>
          {usefulLinks.map((link, index) => (
            <li key={index}>
              <a href={link.url} target="_blank" rel="noopener noreferrer">
                {link.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
      
      <div className="main-content-wrapper">
        <div className="centered-chat">
          <div className="main-content">
            <div className="chat-container">
              <div className="header-wrapper">
                <h1 className="app-header">BUddy: Your AI Guide</h1>
              </div>
              <div
                className="chat-window"
                ref={chatWindowRef}
               style={{ '--chat-font-size': `${fontSize}px` }}
              >
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


              {/* ---------- FONT SIZE SLIDER (bottom-left) ---------- */}
              <div className="font-size-control">
                <label htmlFor="fontSizeSlider" className="sr-only">
                  Adjust chat font size
                </label>
                <input
                  id="fontSizeSlider"
                  type="range"
                  min="12"
                  max="22"
                  step="1"
                  value={fontSize}
                  onChange={handleFontSizeChange}
                  aria-valuemin="12"
                  aria-valuemax="22"
                  aria-valuenow={fontSize}
                />
                <span className="font-size-label">{fontSize}px</span>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;