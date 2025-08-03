# N8N Webhook Setup for PropAI

This guide shows you how to create an n8n workflow that connects with the PropAI frontend.

## Step 1: Create a New Workflow in N8N

1. Open your n8n instance (usually at `http://localhost:5678`)
2. Click "Add Workflow" or create a new workflow
3. Name it "PropAI Chatbot"

## Step 2: Add Webhook Trigger

1. Click the "+" button to add a node
2. Search for "Webhook" and select it
3. Configure the webhook:
   - **HTTP Method**: POST
   - **Path**: `chatbot`
   - **Response Mode**: Respond to Webhook
4. Click "Save" and note the webhook URL (e.g., `http://localhost:5678/webhook/chatbot`)

## Step 3: Add Processing Node

1. Click the "+" button again to add another node
2. You can use any of these options:

### Option A: Simple Echo (for testing)
- Search for "Code" node
- Add this JavaScript code:
```javascript
const userMessage = $input.first().json.message;
const response = {
  response: `You said: "${userMessage}". This is a test response from n8n.`
};
return response;
```

### Option B: AI Integration
- Search for "OpenAI" or your preferred AI service
- Configure with your API key
- Set the prompt to process the user message

### Option C: HTTP Request
- Search for "HTTP Request" node
- Configure to call external APIs

## Step 4: Add Respond to Webhook Node

1. Click the "+" button to add another node
2. Search for "Respond to Webhook" and select it
3. Configure:
   - **Respond With**: JSON
   - **Response Body**: `={{ $json }}`

## Step 5: Connect the Nodes

1. Connect the **Webhook Trigger** → **Processing Node** → **Respond to Webhook**
2. Your workflow should look like: `Webhook → Process → Respond`

## Step 6: Activate the Workflow

1. Click the "Active" toggle in the top right
2. The workflow is now live and ready to receive requests

## Step 7: Configure Frontend

1. Create a `.env` file in your PropAI project root:
```env
REACT_APP_N8N_WEBHOOK_URL=https://agent-loop-hackathon.app.n8n.cloud/webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16
```

2. Restart your React app:
```bash
npm start
```

## Testing the Connection

1. Open your PropAI frontend at `http://localhost:3000`
2. Type a message and send it
3. Check your n8n workflow execution history to see the requests
4. You should see the response in the chat

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure n8n allows requests from `http://localhost:3000`
2. **Webhook Not Found**: Check that the workflow is active and the path is correct
3. **No Response**: Verify the "Respond to Webhook" node is properly configured

### Debug Steps:

1. Check n8n execution history for errors
2. Open browser console (F12) to see network requests
3. Verify the webhook URL in your `.env` file matches n8n

## Example Workflow JSON

You can import this example workflow into n8n:

```json
{
  "name": "PropAI Chatbot",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "chatbot",
        "responseMode": "responseNode"
      },
      "id": "webhook-trigger",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "jsCode": "const userMessage = $input.first().json.message;\nconst response = {\n  response: `You said: \"${userMessage}\". This is a test response from n8n.`\n};\nreturn response;"
      },
      "id": "process-message",
      "name": "Process Message",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      },
      "id": "respond-to-webhook",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [680, 300]
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "Process Message",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Message": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {},
  "versionId": "1"
}
```

## Next Steps

Once connected, you can enhance your n8n workflow with:
- AI services (OpenAI, Claude, etc.)
- Database operations
- External API calls
- File processing
- Email notifications
- And much more! 