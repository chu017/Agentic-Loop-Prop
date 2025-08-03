# PropAI - End-to-End AI Agent

A complete AI agent system with a React frontend chatbot and Express backend with LLM integration using OpenRouter.

## 🏗️ Architecture

```
Agentic-Loop-Prop/
├── frontend/          # React chatbot UI
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/           # Express server with LLM integration
│   ├── config/        # AI configuration
│   ├── services/      # AI agent service
│   ├── routes/        # API routes
│   └── server.js
├── shared/            # Shared types and utilities
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## 🚀 Features

### Frontend (React)
- Modern chatbot UI with real-time messaging
- Model selection (Claude, GPT-4, Llama, etc.)
- Conversation history management
- Session-based chat
- Responsive design

### Backend (Express + OpenRouter)
- LLM integration via OpenRouter
- Multiple AI model support
- Conversation memory and context
- Rate limiting and security
- RESTful API endpoints
- Webhook support for external integrations

## 🛠️ Setup

### Prerequisites
- Node.js (v16+)
- npm or yarn
- OpenRouter API key

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd Agentic-Loop-Prop

# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Environment Configuration

#### Backend (.env)
```bash
cd backend
cp env.example .env
```

Edit `backend/.env`:
```env
# Server Configuration
PORT=5001
NODE_ENV=development

# OpenRouter AI Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
MAX_TOKENS=1000
TEMPERATURE=0.7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

#### Frontend (.env)
```bash
cd frontend
cp .env.example .env
```

### 3. Get OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up and get your API key
3. Add it to `backend/.env`

## 🏃‍♂️ Running the Application

### Development Mode

#### Backend
```bash
cd backend
npm run dev
```
Server runs on: http://localhost:5001

#### Frontend
```bash
cd frontend
npm start
```
Frontend runs on: http://localhost:3000

### Production Mode

#### Backend
```bash
cd backend
npm start
```

#### Frontend
```bash
cd frontend
npm run build
```

## 📡 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send message to AI agent
- `GET /api/chat/models` - Get available AI models
- `GET /api/chat/history/:sessionId` - Get conversation history
- `DELETE /api/chat/history/:sessionId` - Clear conversation
- `GET /api/chat/stats/:sessionId` - Get conversation stats

### System Endpoints
- `GET /health` - Health check
- `POST /api/webhook` - Webhook for external integrations

## 🤖 Available AI Models

- **Claude 3.5 Sonnet** (default)
- **Claude 3 Opus**
- **GPT-4o**
- **GPT-4o Mini**
- **Llama 3.1 70B**
- **Gemini Pro**

## 🔧 Configuration

### AI Agent Settings
- **System Prompt**: Configurable AI personality
- **Memory**: Conversation history management
- **Response Settings**: Temperature, max tokens, etc.
- **Rate Limiting**: Request throttling

### Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `DEFAULT_MODEL`: Default AI model
- `MAX_TOKENS`: Maximum response tokens
- `TEMPERATURE`: Response creativity (0-1)
- `PORT`: Server port
- `ALLOWED_ORIGINS`: CORS origins

## 🎯 Usage Examples

### Basic Chat
```javascript
// Send a message
const response = await fetch('http://localhost:5001/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Hello, how can you help me?",
    sessionId: "user-session-123",
    model: "anthropic/claude-3.5-sonnet"
  })
});
```

### Get Available Models
```javascript
const models = await fetch('http://localhost:5001/api/chat/models');
const data = await models.json();
console.log(data.models);
```

## 🔒 Security Features

- **Helmet**: Security headers
- **CORS**: Cross-origin resource sharing
- **Rate Limiting**: Request throttling
- **Input Validation**: Request sanitization
- **Error Handling**: Graceful error responses

## 📊 Monitoring

- **Health Checks**: `/health` endpoint
- **Request Logging**: Morgan middleware
- **Error Tracking**: Comprehensive error handling
- **Performance**: Response time monitoring

## 🚀 Deployment

### Backend Deployment
1. Set environment variables
2. Install dependencies: `npm install`
3. Start server: `npm start`
4. Use PM2 for production: `pm2 start server.js`

### Frontend Deployment
1. Build: `npm run build`
2. Serve static files
3. Configure reverse proxy

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- Check the `/docs` folder for detailed documentation
- Open issues for bugs or feature requests
- Review environment configuration
- Verify API key setup

## 🔄 Updates

- Regular dependency updates
- New AI model additions
- Security patches
- Performance improvements 