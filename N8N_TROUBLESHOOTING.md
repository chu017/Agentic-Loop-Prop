# N8N Webhook Troubleshooting

## Current Issue: "Workflow could not be started!"

The webhook is returning a 500 error, which means your n8n workflow needs to be properly configured.

## Step-by-Step Fix:

### 1. Check Your N8N Workflow

1. **Open your n8n instance** at `https://agent-loop-hackathon.app.n8n.cloud`
2. **Find your workflow** that uses the webhook URL
3. **Check if the workflow is ACTIVE** (toggle should be ON)

### 2. Verify Webhook Configuration

Your webhook node should be configured as:
- **HTTP Method**: POST
- **Path**: `webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16`
- **Response Mode**: Respond to Webhook

### 3. Check Workflow Structure

Your workflow should have at least:
1. **Webhook Trigger** (receives the request)
2. **Processing Node** (handles the message)
3. **Respond to Webhook** (sends response back)

### 4. Test the Workflow

1. **Activate the workflow** if it's not active
2. **Test the webhook** by sending a test request
3. **Check execution history** for any errors

### 5. Common Issues & Solutions

#### Issue: Workflow not active
**Solution**: Click the "Active" toggle in the top right of your workflow

#### Issue: Webhook path mismatch
**Solution**: Make sure the webhook path matches exactly: `webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16`

#### Issue: Missing "Respond to Webhook" node
**Solution**: Add a "Respond to Webhook" node and connect it to your processing node

#### Issue: Workflow has errors
**Solution**: Check the execution history for error messages and fix them

### 6. Quick Test Workflow

If you need a simple test workflow, create this:

1. **Webhook Trigger**
   - HTTP Method: POST
   - Path: `webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16`

2. **Code Node** (for processing)
   ```javascript
   const userMessage = $input.first().json.message;
   return {
     response: `Received: ${userMessage}`
   };
   ```

3. **Respond to Webhook**
   - Respond With: JSON
   - Response Body: `={{ $json }}`

4. **Connect**: Webhook → Code → Respond to Webhook
5. **Activate** the workflow

### 7. Verify Connection

After fixing the workflow:
1. **Restart your React app**: `npm start`
2. **Test in browser**: Go to `http://localhost:3000`
3. **Send a message** and check if it works

### 8. Debug Steps

1. **Check n8n execution history** for errors
2. **Open browser console** (F12) to see network requests
3. **Test webhook directly** with curl:
   ```bash
   curl -X POST https://agent-loop-hackathon.app.n8n.cloud/webhook-test/1e53d8a1-e8c8-4e04-9aa4-62de50e36f16 \
   -H "Content-Type: application/json" \
   -d '{"message": "test"}'
   ```

## Expected Response

When working correctly, the webhook should return:
```json
{"response": "Your processed message here"}
```

Instead of the current error:
```json
{"code":0,"message":"Workflow Webhook Error: Workflow could not be started!"}
``` 