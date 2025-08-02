# PropAI Frontend

A simple and modern React chatbot frontend designed to connect with n8n workflows. This application provides a beautiful, responsive chat interface that can communicate with your n8n automation workflows.

## Features

- 🎨 **Modern UI/UX**: Clean, responsive design with smooth animations
- 🤖 **Real-time Chat**: Instant message sending and receiving
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- ⚡ **Loading States**: Visual feedback during message processing
- 🔗 **N8N Integration**: Easy connection to n8n webhook workflows
- 🎯 **Error Handling**: Graceful error handling and user feedback

## Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- n8n instance running (for backend integration)

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   REACT_APP_N8N_WEBHOOK_URL=http://localhost:5678/webhook/chatbot
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```

The application will open at `http://localhost:3000`

## N8N Workflow Setup

To connect this frontend with n8n, you'll need to create a webhook workflow in n8n:

### 1. Create a Webhook Trigger
- Add a "Webhook" trigger node
- Set the HTTP method to `POST`
- Note the webhook URL (e.g., `http://localhost:5678/webhook/chatbot`)

### 2. Process the Message
- Add nodes to process the incoming message
- You can use AI nodes, HTTP requests, or any other n8n nodes
- The message will be available in the webhook payload as `{{ $json.message }}`

### 3. Return Response
- Add a "Respond to Webhook" node
- Set the response body to include a `response` field:
  ```json
  {
    "response": "Your processed response here"
  }
  ```

### Example N8N Workflow
```
Webhook Trigger → AI Node → Respond to Webhook
```

## Configuration

### Environment Variables

- `REACT_APP_N8N_WEBHOOK_URL`: The URL of your n8n webhook endpoint
  - Default: `http://localhost:5678/webhook/chatbot`

### Customization

You can customize the chatbot by modifying:

- **Appearance**: Edit `src/App.css` for styling changes
- **Behavior**: Modify `src/App.js` for different message handling

## Project Structure

```
├── public/
│   └── index.html              # Main HTML file
├── src/
│   ├── App.js                  # Main app component
│   ├── App.css                 # All styles
│   ├── index.js                # React entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies and scripts
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## API Integration

The frontend sends POST requests to your n8n webhook with the following payload:

```json
{
  "message": "User's message",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "sessionId": "user-session-1234567890"
}
```

Expected response from n8n:

```json
{
  "response": "Bot's response message"
}
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your n8n instance allows requests from `http://localhost:3000`
2. **Connection Failed**: Check that your n8n webhook URL is correct and accessible
3. **Messages Not Sending**: Verify the webhook is configured to accept POST requests

### Debug Mode

Enable debug logging by opening the browser console (F12) to see detailed error messages.

## Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 