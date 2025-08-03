# PropAI Server

Backend server for the PropAI agent chatbot.

## Features

- Express.js REST API
- AI agent with conversation history
- Webhook support for n8n integration
- CORS enabled for frontend communication
- Security middleware (Helmet)
- Request logging (Morgan)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp env.example .env
```

3. Configure your environment variables in `.env`

## Running the Server

### Development
```bash
npm run dev
```

### Production
```bash
npm start
```

## API Endpoints

### Health Check
- **GET** `/api/health`
- Returns server status and uptime

### Chat
- **POST** `/api/chat`
- Body: `{ "message": "Hello", "sessionId": "optional" }`
- Returns: `{ "success": true, "response": "AI response", "timestamp": "..." }`

### Webhook (for n8n)
- **POST** `/api/webhook`
- Body: `{ "message": "Hello", "sessionId": "optional" }`
- Returns: `{ "success": true, "response": "AI response", "timestamp": "..." }`

## Environment Variables

- `PORT`: Server port (default: 5000)
- `NODE_ENV`: Environment (development/production)
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `JWT_SECRET`: JWT secret for authentication
- `ALLOWED_ORIGINS`: CORS allowed origins

## Integration with Frontend

The server is designed to work with the React frontend. Update the frontend's webhook URL to point to this server:

```javascript
// In frontend, update the webhook URL
const n8nWebhookUrl = 'http://localhost:5000/api/webhook';
```

## Development

The server includes:
- Conversation history management
- Session-based responses
- Error handling
- Logging
- Security headers

## Production Considerations

- Add database for persistent conversation storage
- Implement proper authentication
- Add rate limiting
- Use environment-specific configurations
- Add monitoring and logging 