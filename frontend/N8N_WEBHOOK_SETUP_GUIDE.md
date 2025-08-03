# N8N Webhook Setup Guide

## Current Issue: 404 Error - Webhook Not Registered

The webhook URL `https://agent-loop-hackathon.app.n8n.cloud/webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16` is returning a 404 error, which means the workflow doesn't exist or isn't properly configured.

## Step-by-Step Fix:

### Step 1: Access Your N8N Instance

1. Go to `https://agent-loop-hackathon.app.n8n.cloud`
2. Log in to your n8n account
3. You should see your workflows dashboard

### Step 2: Create or Find the Workflow

**Option A: Create New Workflow**
1. Click "Add Workflow" or "Create Workflow"
2. Name it "PropAI Chatbot"

**Option B: Find Existing Workflow**
1. Look for a workflow that might be related to this webhook
2. Check if it has a webhook trigger with the path `webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16`

### Step 3: Configure the Webhook Trigger

1. **Add Webhook Trigger Node**
   - Click the "+" button to add a node
   - Search for "Webhook" and select it

2. **Configure the Webhook**
   - **HTTP Method**: POST
   - **Path**: `webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16`
   - **Response Mode**: Respond to Webhook
   - **Options**: Leave default settings

3. **Save the Webhook**
   - Click "Save" on the webhook node
   - Note the webhook URL that appears

### Step 4: Add Processing Node

1. **Add a Code Node**
   - Click the "+" button again
   - Search for "Code" and select it
   - Add this JavaScript code:

```javascript
const userMessage = $input.first().json.message;
const timestamp = $input.first().json.timestamp;
const sessionId = $input.first().json.sessionId;

// Simple echo response for testing
const response = {
  response: `Hello! I received your message: "${userMessage}". This is a test response from n8n.`
};

return response;
```

### Step 5: Add Respond to Webhook Node

1. **Add Respond to Webhook Node**
   - Click the "+" button again
   - Search for "Respond to Webhook" and select it

2. **Configure the Response**
   - **Respond With**: JSON
   - **Response Body**: `={{ $json }}`

### Step 6: Connect the Nodes

1. **Connect Webhook → Code → Respond to Webhook**
   - Drag from the webhook node to the code node
   - Drag from the code node to the respond to webhook node

2. **Your workflow should look like:**
   ```
   Webhook Trigger → Code Node → Respond to Webhook
   ```

### Step 7: Activate the Workflow

1. **Click the "Active" toggle** in the top right corner
2. **The workflow should turn green** when active
3. **Test the webhook** by clicking "Execute workflow" on the webhook node

### Step 8: Test the Connection

1. **Test with curl:**
   ```bash
   curl -X POST https://agent-loop-hackathon.app.n8n.cloud/webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16 \
   -H "Content-Type: application/json" \
   -d '{"message": "test", "timestamp": "2024-01-01T12:00:00.000Z", "sessionId": "test"}'
   ```

2. **Expected response:**
   ```json
   {"response": "Hello! I received your message: \"test\". This is a test response from n8n."}
   ```

### Step 9: Test with PropAI Frontend

1. **Go to your React app** at `http://localhost:3000`
2. **Send a message** in the chat
3. **Check the browser console** (F12) for any errors
4. **You should see the response** from n8n

## Troubleshooting

### If you still get 404:
1. **Check the webhook path** - it must be exactly `webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16`
2. **Make sure the workflow is active** (green toggle)
3. **Try executing the workflow manually** first
4. **Check if the webhook URL is correct** in your n8n instance

### If you get other errors:
1. **Check the execution history** in n8n for error details
2. **Verify the code node** has the correct JavaScript
3. **Make sure all nodes are connected** properly

## Quick Test Workflow JSON

If you want to import a ready-made workflow, use this JSON:

```json
{
  "name": "PropAI Chatbot",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16",
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
        "jsCode": "const userMessage = $input.first().json.message;\nconst response = {\n  response: `Hello! I received your message: \"${userMessage}\". This is a test response from n8n.`\n};\nreturn response;"
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

Once the basic webhook is working, you can enhance it with:
- AI services (OpenAI, Claude, etc.)
- Database operations
- External API calls
- More complex processing logic 