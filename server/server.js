const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Store conversation history (in production, use a database)
const conversationHistory = new Map();

// AI Agent Logic
class PropAIAgent {
  constructor() {
    this.context = "You are PropAI, a helpful AI assistant. You can help with various tasks including coding, analysis, and general questions.";
  }

  async processMessage(message, sessionId) {
    try {
      // Simple response logic - in production, integrate with OpenAI or other AI service
      const response = await this.generateResponse(message, sessionId);
      return {
        success: true,
        response: response,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error processing message:', error);
      return {
        success: false,
        response: "I'm sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date().toISOString()
      };
    }
  }

  async generateResponse(message, sessionId) {
    // Get conversation history for context
    const history = conversationHistory.get(sessionId) || [];
    
    // Simple response logic - replace with actual AI integration
    const responses = [
      "I understand you're asking about that. Let me help you with that.",
      "That's an interesting question. Here's what I can tell you about that.",
      "I can help you with that. Let me provide some information.",
      "Thanks for your message. I'm here to assist you with that.",
      "I appreciate your question. Let me address that for you."
    ];

    // Add context-aware responses based on message content
    if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
      return "Hello! I'm PropAI, your AI assistant. How can I help you today?";
    }
    
    if (message.toLowerCase().includes('help')) {
      return "I'm here to help! I can assist with various tasks including answering questions, providing information, and helping with analysis. What would you like to know?";
    }
    
    if (message.toLowerCase().includes('code') || message.toLowerCase().includes('programming')) {
      return "I can help you with programming questions! What programming language or framework are you working with?";
    }

    // Default response
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    
    // Store in conversation history
    history.push({
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    });
    
    history.push({
      role: 'assistant',
      content: randomResponse,
      timestamp: new Date().toISOString()
    });

    // Keep only last 10 messages for context
    if (history.length > 10) {
      history.splice(0, history.length - 10);
    }
    
    conversationHistory.set(sessionId, history);
    
    return randomResponse;
  }
}

// Initialize AI Agent
const agent = new PropAIAgent();

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'PropAI Server is running!',
    version: '1.0.0',
    endpoints: {
      chat: '/api/chat',
      health: '/api/health'
    }
  });
});

app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Main chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message, sessionId = 'default-session' } = req.body;
    
    if (!message || typeof message !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Message is required and must be a string'
      });
    }

    console.log(`Processing message from session ${sessionId}:`, message);
    
    const result = await agent.processMessage(message, sessionId);
    
    res.json(result);
  } catch (error) {
    console.error('Error in chat endpoint:', error);
    res.status(500).json({
      success: false,
      response: "Internal server error. Please try again.",
      timestamp: new Date().toISOString()
    });
  }
});

// Webhook endpoint for n8n integration
app.post('/api/webhook', async (req, res) => {
  try {
    const { message, sessionId = 'webhook-session' } = req.body;
    
    if (!message) {
      return res.status(400).json({
        success: false,
        error: 'Message is required'
      });
    }

    console.log(`Processing webhook message from session ${sessionId}:`, message);
    
    const result = await agent.processMessage(message, sessionId);
    
    res.json(result);
  } catch (error) {
    console.error('Error in webhook endpoint:', error);
    res.status(500).json({
      success: false,
      response: "Internal server error. Please try again.",
      timestamp: new Date().toISOString()
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    response: "An unexpected error occurred. Please try again.",
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 PropAI Server running on port ${PORT}`);
  console.log(`📡 Health check: http://localhost:${PORT}/api/health`);
  console.log(`💬 Chat endpoint: http://localhost:${PORT}/api/chat`);
  console.log(`🔗 Webhook endpoint: http://localhost:${PORT}/api/webhook`);
});

module.exports = app; 