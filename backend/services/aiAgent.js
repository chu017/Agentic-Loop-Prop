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

  // Generate response using OpenRouter
  async generateResponse(messages, modelName = null) {
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
      throw new Error(`AI service error: ${error.message}`);
    }
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