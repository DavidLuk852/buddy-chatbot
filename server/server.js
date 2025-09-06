const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors()); // Enable CORS

// API Endpoint for Chat
app.post('/api/chat', async (req, res) => {
  const { message } = req.body;
  if (!message) return res.status(400).send('Message is required');

  try {
    const response = await axios.post('http://localhost:5000/api/chat', { message });
    res.json({ response: response.data.response });
  } catch (error) {
    console.error('Error fetching bot response:', error);
    res.status(500).send('Internal server error');
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));