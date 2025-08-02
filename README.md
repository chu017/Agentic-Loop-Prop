# PropAI Frontend

A simple React chatbot frontend that connects with n8n workflows.

## Quick Start

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Open your browser** and go to `http://localhost:3000`

## N8N Setup

1. Create a webhook workflow in n8n
2. Set the webhook URL to: `http://localhost:5678/webhook/chatbot`
3. Configure the response to return: `{"response": "Your message here"}`

## Environment Variables

Create a `.env` file in the root directory:
```env
REACT_APP_N8N_WEBHOOK_URL=https://agent-loop-hackathon.app.n8n.cloud/webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16
``` 