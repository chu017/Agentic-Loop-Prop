# PropAI - AI Agent System

A complete AI agent with React frontend and Express backend using OpenRouter LLM integration.

## 🏗️ Structure

```
Agentic-Loop-Prop/
├── frontend/          # React chatbot UI
│   ├── src/           # React components
│   └── package.json   # Frontend dependencies
├── backend/           # Express server with LLM
│   ├── config/        # AI configuration
│   ├── services/      # AI agent service
│   ├── routes/        # API endpoints
│   └── server.js      # Main server
└── README.md
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Backend
cd backend
cp env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# Frontend
cd frontend
npm install
```

### 2. Install Dependencies
```bash
# Backend
cd backend
npm install

# Frontend
cd frontend
npm install
```

### 3. Run the Application
```bash
# Backend (port 5001)
cd backend
npm start

# Frontend (port 3000)
cd frontend
npm start
```

## 🔑 Required Setup

1. **Get OpenRouter API Key:**
   - Visit [OpenRouter](https://openrouter.ai/)
   - Sign up and get your API key
   - Add to `backend/.env`:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

## 📡 API Endpoints

- `POST /api/chat` - Send message to AI
- `GET /api/chat/models` - Get available models
- `GET /health` - Health check

## 🤖 Available Models

- Claude 3.5 Sonnet (default)
- GPT-4o
- Llama 3.1 70B
- Gemini Pro

## 🎯 Usage

1. **Start both services**
2. **Open frontend:** http://localhost:3000
3. **Select AI model** from dropdown
4. **Start chatting** with the AI agent

## 🔧 Environment Variables

```env
# Backend (.env)
PORT=5001
OPENROUTER_API_KEY=your_key_here
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
ALLOWED_ORIGINS=http://localhost:3000
``` 