const { openai, agentConfig, availableModels } = require('../config/ai');
const { v4: uuidv4 } = require('uuid');

class AIAgent {
  constructor() {
    this.conversations = new Map();
    this.model = agentConfig.responseSettings;
  }

  // Create a new conversation session
  createSession(sessionId = null) {
    const id = sessionId || uuidv4();
    const session = {
      id,
      messages: [],
      createdAt: new Date(),
      lastActivity: new Date(),
    };
    
    this.conversations.set(id, session);
    return session;
  }

  // Get or create conversation session
  getSession(sessionId) {
    if (!this.conversations.has(sessionId)) {
      return this.createSession(sessionId);
    }
    
    const session = this.conversations.get(sessionId);
    session.lastActivity = new Date();
    return session;
  }

  // Add message to conversation
  addMessage(sessionId, role, content) {
    const session = this.getSession(sessionId);
    const message = {
      role,
      content,
      timestamp: new Date(),
    };
    
    session.messages.push(message);
    
    // Trim conversation if it exceeds limits
    this.trimConversation(session);
    
    return message;
  }

  // Trim conversation to stay within limits
  trimConversation(session) {
    const { maxMessages, maxTokens } = agentConfig.conversationMemory;
    
    // Remove oldest messages if we exceed max messages
    if (session.messages.length > maxMessages) {
      const messagesToRemove = session.messages.length - maxMessages;
      session.messages.splice(0, messagesToRemove);
    }
    
    // TODO: Implement token counting for more precise trimming
  }

  // Process user message and generate AI response
  async processMessage(message, sessionId, modelName = null) {
    try {
      // Add user message to conversation
      this.addMessage(sessionId, 'user', message);
      
      // Get conversation context
      const session = this.getSession(sessionId);
      const messages = this.buildMessageHistory(session);
      
      // Generate AI response
      const response = await this.generateResponse(messages, modelName);
      
      // Add AI response to conversation
      this.addMessage(sessionId, 'assistant', response);
      
      return {
        success: true,
        response,
        sessionId,
        timestamp: new Date().toISOString(),
        model: modelName || 'default',
      };
    } catch (error) {
      console.error('Error processing message:', error);
      return {
        success: false,
        response: "I'm sorry, I encountered an error processing your request. Please try again.",
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }

  // Build message history for API call
  buildMessageHistory(session) {
    const messages = [
      {
        role: 'system',
        content: agentConfig.systemPrompt,
      },
    ];
    
    // Add conversation history
    messages.push(...session.messages);
    
    return messages;
  }

  // Generate response using OpenRouter or fallback
  async generateResponse(messages, modelName = null) {
    // Check if OpenRouter is available
    if (!openai) {
      return this.generateFallbackResponse(messages[messages.length - 1]?.content || '');
    }

    const model = modelName || agentConfig.responseSettings.defaultModel;
    
    try {
      const completion = await openai.chat.completions.create({
        model: model,
        messages: messages,
        max_tokens: this.model.maxTokens,
        temperature: this.model.temperature,
        top_p: this.model.topP,
        frequency_penalty: this.model.frequencyPenalty,
        presence_penalty: this.model.presencePenalty,
        stream: false,
      });

      return completion.choices[0].message.content;
    } catch (error) {
      console.error('OpenRouter API error:', error);
      return this.generateFallbackResponse(messages[messages.length - 1]?.content || '');
    }
  }

  // Generate fallback response when API is not available
  generateFallbackResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    // Simple response logic based on message content
    if (message.includes('hello') || message.includes('hi')) {
      return "Hello! I'm PropAI, your AI assistant. How can I help you today?";
    }
    
    if (message.includes('help')) {
      return "I'm here to help! I can assist with various tasks including answering questions, providing information, and helping with analysis. What would you like to know?";
    }
    
    if (message.includes('code') || message.includes('programming')) {
      return "I can help you with programming questions! What programming language or framework are you working with?";
    }

    // Default responses
    const responses = [
      "I understand you're asking about that. Let me help you with that.",
      "That's an interesting question. Here's what I can tell you about that.",
      "I can help you with that. Let me provide some information.",
      "Thanks for your message. I'm here to assist you with that.",
      "I appreciate your question. Let me address that for you."
    ];

    return responses[Math.floor(Math.random() * responses.length)];
  }

  // Get available models
  getAvailableModels() {
    return availableModels;
  }

  // Get conversation history
  getConversationHistory(sessionId) {
    const session = this.getSession(sessionId);
    return session.messages;
  }

  // Clear conversation
  clearConversation(sessionId) {
    if (this.conversations.has(sessionId)) {
      const session = this.conversations.get(sessionId);
      session.messages = [];
      session.lastActivity = new Date();
    }
  }

  // Get conversation stats
  getConversationStats(sessionId) {
    const session = this.getSession(sessionId);
    return {
      sessionId: session.id,
      messageCount: session.messages.length,
      createdAt: session.createdAt,
      lastActivity: session.lastActivity,
    };
  }
}

module.exports = AIAgent; 