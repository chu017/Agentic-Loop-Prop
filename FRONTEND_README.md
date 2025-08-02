# HVAC AI Assistant Frontend

A modern TypeScript React frontend for the HVAC AI Assistant system, built with shadcn/ui components and designed for builders to manage HVAC projects and interact with AI-powered diagnostics.

## 🚀 Features

### **Project Management**
- Create and manage HVAC projects
- Select HVAC models from Thermia catalog
- Describe project issues and requirements
- Track project status (Active, Resolved, Pending)

### **AI-Powered Chat Interface**
- Real-time conversation with HVAC AI Assistant
- Context-aware responses based on project details
- Quick action buttons for common tasks
- System status monitoring

### **Modern UI/UX**
- Built with TypeScript for type safety
- shadcn/ui components for consistent design
- Responsive layout for all devices
- Dark/light mode support
- Smooth animations and transitions

### **HVAC System Integration**
- Thermia API integration
- Real-time system monitoring
- Diagnostic capabilities
- Optimization suggestions

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible components
- **Lucide React** - Modern icon library
- **Axios** - HTTP client for API calls
- **Radix UI** - Headless UI primitives

## 📦 Installation

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend API running (Flask server)

### Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your API URL:
   ```env
   REACT_APP_API_URL=http://localhost:5000
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## 🏗️ Project Structure

```
src/
├── components/
│   ├── ui/                 # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   └── textarea.tsx
│   ├── ProjectList.tsx     # Project management
│   ├── ProjectSetup.tsx    # Project creation
│   └── HVACChat.tsx        # AI chat interface
├── services/
│   └── api.ts             # API integration
├── types/
│   └── index.ts           # TypeScript types
├── lib/
│   └── utils.ts           # Utility functions
├── App.tsx                # Main app component
└── index.tsx              # Entry point
```

## 🎨 UI Components

### **Project Setup Form**
- Project name and description
- HVAC model selection dropdown
- Issue description textarea
- Form validation and error handling

### **Project List**
- Grid layout with project cards
- Status filtering (All, Active, Resolved, Pending)
- Project statistics dashboard
- Quick access to AI assistant

### **Chat Interface**
- Real-time messaging with AI
- Message history with timestamps
- Quick action buttons
- Project context sidebar
- Loading states and error handling

## 🔧 Configuration

### **API Endpoints**
The frontend communicates with these backend endpoints:

- `POST /api/chat` - Send messages to AI
- `GET /api/hvac/systems` - Get HVAC systems
- `GET /api/hvac/status` - Get system status
- `GET /api/health` - Health check
- `POST /api/search` - Search knowledge base

### **Environment Variables**
```env
REACT_APP_API_URL=http://localhost:5000
```

### **HVAC Models**
Supported Thermia models:
- Thermia Diplomat Duo
- Thermia Calibra
- Thermia Atlas
- Thermia Mega
- Thermia Classic
- Thermia Compact
- Other (custom)

## 🎯 User Flow

### **1. Project Creation**
1. Click "New Project" button
2. Fill in project details:
   - Project name
   - Description (optional)
   - HVAC model selection
   - Issue description
3. Submit form to create project
4. Automatically opens AI chat interface

### **2. AI Assistant Interaction**
1. View project context in sidebar
2. Ask questions about HVAC system
3. Use quick action buttons for common tasks:
   - System Status
   - Diagnose Issues
   - Optimization Tips
4. Receive AI-powered responses
5. Navigate back to project list

### **3. Project Management**
1. View all projects in grid layout
2. Filter by status (Active, Resolved, Pending)
3. Click project card to open AI assistant
4. View project statistics and metrics

## 🎨 Design System

### **Colors**
- Primary: Blue (#2563eb)
- Success: Green (#16a34a)
- Warning: Orange (#ea580c)
- Error: Red (#dc2626)
- Neutral: Gray scale

### **Typography**
- Headings: Inter font family
- Body: System font stack
- Icons: Lucide React

### **Components**
- Cards with subtle shadows
- Rounded corners (8px radius)
- Consistent spacing (4px grid)
- Hover states and transitions

## 🔌 API Integration

### **Chat API**
```typescript
// Send message to AI
const response = await chatAPI.sendMessage(message, sessionId);

// Search knowledge base
const results = await chatAPI.searchKnowledge(query, maxResults);
```

### **HVAC API**
```typescript
// Get all systems
const systems = await hvacAPI.getSystems();

// Diagnose system
const diagnosis = await hvacAPI.diagnoseSystem(systemId);

// Get optimization suggestions
const suggestions = await hvacAPI.getOptimizationSuggestions(systemId);
```

### **System API**
```typescript
// Health check
const health = await systemAPI.getHealth();

// System status
const status = await systemAPI.getSystemStatus();
```

## 🧪 Testing

### **Run Tests**
```bash
npm test
```

### **Test Coverage**
- Component rendering
- User interactions
- API integration
- Error handling
- Responsive design

## 🚀 Deployment

### **Build for Production**
```bash
npm run build
```

### **Serve Static Files**
```bash
npx serve -s build
```

### **Docker Deployment**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔧 Development

### **Adding New Components**
1. Create component in `src/components/`
2. Add TypeScript interfaces
3. Import shadcn/ui components
4. Add to main App.tsx

### **Styling Guidelines**
- Use Tailwind CSS classes
- Follow shadcn/ui patterns
- Maintain responsive design
- Use consistent spacing

### **State Management**
- React hooks for local state
- localStorage for persistence
- Context API for global state (if needed)

## 🐛 Troubleshooting

### **Common Issues**

1. **API Connection Errors**
   - Check backend server is running
   - Verify API URL in .env
   - Check CORS configuration

2. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript errors
   - Verify all dependencies

3. **Styling Issues**
   - Ensure Tailwind CSS is configured
   - Check shadcn/ui installation
   - Verify CSS imports

### **Debug Mode**
```bash
# Enable debug logging
REACT_APP_DEBUG=true npm start
```

## 📚 Additional Resources

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [React TypeScript Guide](https://react-typescript-cheatsheet.netlify.app/)
- [Lucide Icons](https://lucide.dev/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with TypeScript
4. Add tests if applicable
5. Submit pull request

## 📄 License

This project is part of the HVAC AI Assistant system. See main README for license information.

---

**Built with ❤️ using TypeScript, React, and shadcn/ui** 