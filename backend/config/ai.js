const OpenAI = require('openai');

// OpenRouter configuration
const openRouterConfig = {
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
  defaultModel: process.env.DEFAULT_MODEL || 'deepseek-ai/deepseek-coder-r1-0528',
  maxTokens: parseInt(process.env.MAX_TOKENS) || 1000,
  temperature: parseFloat(process.env.TEMPERATURE) || 0.7,
};

// Initialize OpenAI client for OpenRouter (only if API key is available)
let openai = null;
if (openRouterConfig.apiKey) {
  openai = new OpenAI({
    baseURL: openRouterConfig.baseURL,
    apiKey: openRouterConfig.apiKey,
  });
}

// Available models on OpenRouter
const availableModels = {
  'deepseek-ai/deepseek-coder-r1-0528': 'DeepSeek R1 0528 (Free)',
  'anthropic/claude-3.5-sonnet': 'Claude 3.5 Sonnet',
  'anthropic/claude-3-opus': 'Claude 3 Opus',
  'openai/gpt-4o': 'GPT-4o',
  'openai/gpt-4o-mini': 'GPT-4o Mini',
  'meta-llama/llama-3.1-70b-instruct': 'Llama 3.1 70B',
  'google/gemini-pro': 'Gemini Pro',
};

// AI Agent configuration
const agentConfig = {
  systemPrompt: `You are PropAI, an intelligent AI assistant designed to help users with various tasks. You are:

1. **Helpful and Friendly**: Always respond in a helpful, friendly manner
2. **Knowledgeable**: You can help with coding, analysis, problem-solving, and general questions
3. **Context-Aware**: Remember conversation history and provide relevant responses
4. **Clear and Concise**: Provide clear, well-structured responses
5. **Safe**: Avoid harmful, unethical, or illegal content

Your capabilities include:
- Programming and technical assistance
- Data analysis and interpretation
- Problem-solving and brainstorming
- General knowledge and information
- Creative writing and content generation

Always be respectful, honest about your limitations, and focus on being genuinely helpful.`,

  conversationMemory: {
    maxMessages: 20,
    maxTokens: 4000,
  },

  responseSettings: {
    maxTokens: openRouterConfig.maxTokens,
    temperature: openRouterConfig.temperature,
    topP: 0.9,
    frequencyPenalty: 0.1,
    presencePenalty: 0.1,
  },
};

module.exports = {
  openai,
  openRouterConfig,
  availableModels,
  agentConfig,
}; 