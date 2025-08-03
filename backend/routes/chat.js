const express = require('express');
const rateLimit = require('express-rate-limit');
const AIAgent = require('../services/aiAgent');

const router = express.Router();
const aiAgent = new AIAgent();

// Rate limiting
const chatLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Apply rate limiting to all chat routes
router.use(chatLimiter);

// POST /api/chat - Send a message to the AI agent
router.post('/chat', async (req, res) => {
  try {
    const { message, sessionId, model } = req.body;
    
    if (!message || typeof message !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Message is required and must be a string'
      });
    }

    console.log(`Processing message from session ${sessionId || 'new'}:`, message);
    
    const result = await aiAgent.processMessage(message, sessionId, model);
    
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

// GET /api/chat/models - Get available AI models
router.get('/chat/models', (req, res) => {
  try {
    const models = aiAgent.getAvailableModels();
    res.json({
      success: true,
      models,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error getting models:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve available models'
    });
  }
});

// GET /api/chat/history/:sessionId - Get conversation history
router.get('/chat/history/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    const history = aiAgent.getConversationHistory(sessionId);
    
    res.json({
      success: true,
      sessionId,
      history,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error getting conversation history:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve conversation history'
    });
  }
});

// DELETE /api/chat/history/:sessionId - Clear conversation history
router.delete('/chat/history/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    aiAgent.clearConversation(sessionId);
    
    res.json({
      success: true,
      message: 'Conversation history cleared',
      sessionId,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error clearing conversation history:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to clear conversation history'
    });
  }
});

// GET /api/chat/stats/:sessionId - Get conversation statistics
router.get('/chat/stats/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    const stats = aiAgent.getConversationStats(sessionId);
    
    res.json({
      success: true,
      stats,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error getting conversation stats:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve conversation statistics'
    });
  }
});

// Webhook endpoint for external integrations (n8n, etc.)
router.post('/webhook', async (req, res) => {
  try {
    const { message, sessionId, model } = req.body;
    
    if (!message) {
      return res.status(400).json({
        success: false,
        error: 'Message is required'
      });
    }

    console.log(`Processing webhook message from session ${sessionId || 'webhook'}:`, message);
    
    const result = await aiAgent.processMessage(message, sessionId, model);
    
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

module.exports = router; 