# HVAC AI Assistant

A comprehensive AI-powered HVAC system assistant with TypeScript React frontend and Python Flask backend, featuring Thermia API integration and n8n compatibility.

## 🚀 Quick Start

### **Option 1: Unified Startup (Recommended)**
```bash
# Navigate to project directory
cd Agentic-Loop-Prop-backup

# Run the unified startup script
python start_system.py
```

### **Option 2: Manual Startup**
```bash
# Terminal 1: Start Backend
python start_backend.py

# Terminal 2: Start Frontend  
python start_frontend.py
```

### **Option 3: Traditional Method**
```bash
# Terminal 1: Start Flask Backend
python app.py

# Terminal 2: Start React Frontend
npm start
```

## 📱 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 🛠️ System Requirements

### **Required Software**
- **Python 3.8+**
- **Node.js 16+**
- **npm** (comes with Node.js)
- **Ollama** (for AI features)

### **Installation Commands**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull the required model
ollama pull mistral
```

## 📁 Project Structure

```
Agentic-Loop-Prop-backup/
├── src/                          # TypeScript React frontend
│   ├── components/
│   │   ├── ui/                   # shadcn/ui components
│   │   ├── ProjectList.tsx       # Project management
│   │   ├── ProjectSetup.tsx      # Project creation
│   │   └── HVACChat.tsx          # AI chat interface
│   ├── services/api.ts           # API integration
│   ├── types/index.ts            # TypeScript types
│   └── App.tsx                   # Main app component
├── scripts/
│   ├── ai_rag_chat.py           # AI system core
│   └── thermia_integration.py   # Thermia API integration
├── tests/                        # Test suites
├── app.py                        # Flask backend API
├── start_system.py               # Unified startup script
├── start_backend.py              # Backend startup script
├── start_frontend.py             # Frontend startup script
└── DEBUG_GUIDE.md               # Debug guide
```

## 🔧 Features

### **Frontend Features**
- ✅ **TypeScript React** with modern UI
- ✅ **shadcn/ui** component library
- ✅ **Project Management** - Create and manage HVAC projects
- ✅ **HVAC Model Selection** - Choose from Thermia models
- ✅ **Issue Description** - Describe HVAC problems
- ✅ **AI Chat Interface** - Interactive AI assistant
- ✅ **Real-time Status** - System health monitoring
- ✅ **Responsive Design** - Works on all devices

### **Backend Features**
- ✅ **Flask API** with CORS support
- ✅ **AI Integration** with Ollama/Mistral
- ✅ **Thermia API** integration for HVAC systems
- ✅ **Knowledge Base** with RAG capabilities
- ✅ **n8n Compatibility** for workflow automation
- ✅ **Comprehensive Testing** suite
- ✅ **Error Handling** and logging

### **AI Features**
- ✅ **Natural Language Processing** for HVAC queries
- ✅ **System Diagnosis** and troubleshooting
- ✅ **Optimization Suggestions** for efficiency
- ✅ **Temperature Control** via API
- ✅ **Operation Mode** management
- ✅ **Real-time Monitoring** of HVAC systems

## 🐛 Troubleshooting

### **Common Issues**

#### **1. TypeScript Import Errors**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### **2. Backend Connection Errors**
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Start backend manually
python app.py
```

#### **3. Ollama Connection Issues**
```bash
# Check Ollama status
ollama list

# Start Ollama service
ollama serve

# Pull required model
ollama pull mistral
```

#### **4. Port Conflicts**
```bash
# Check what's using the ports
lsof -i :3000  # Frontend port
lsof -i :5000  # Backend port
```

### **Debug Commands**
```bash
# Test backend API
curl http://localhost:5000/api/health
curl http://localhost:5000/api/system-status

# Test frontend build
npm run build

# Check TypeScript errors
npx tsc --noEmit
```

## 📚 Documentation

- **[DEBUG_GUIDE.md](DEBUG_GUIDE.md)** - Comprehensive debugging guide
- **[FRONTEND_README.md](FRONTEND_README.md)** - Frontend-specific documentation
- **[TESTING.md](TESTING.md)** - Testing framework documentation

## 🔌 API Endpoints

### **Core Endpoints**
- `GET /api/health` - System health check
- `POST /api/chat` - AI chat interface
- `POST /api/search` - Knowledge base search
- `GET /api/system-status` - System status

### **HVAC Endpoints**
- `GET /api/hvac/systems` - Get all HVAC systems
- `GET /api/hvac/systems/{id}/diagnose` - Diagnose system
- `GET /api/hvac/systems/{id}/optimize` - Get optimization suggestions
- `POST /api/hvac/systems/{id}/temperature` - Set temperature
- `POST /api/hvac/systems/{id}/mode` - Set operation mode
- `GET /api/hvac/status` - HVAC status summary

## 🧪 Testing

### **Run All Tests**
```bash
python run_tests.py
```

### **Individual Test Suites**
```bash
# AI System Tests
pytest tests/test_ai_system.py

# Thermia API Tests
pytest tests/test_thermia_api.py

# n8n Compatibility Tests
pytest tests/test_n8n_compatibility.py
```

## 🚀 Deployment

### **Development**
```bash
# Start development servers
python start_system.py
```

### **Production**
```bash
# Build frontend
npm run build

# Start production backend
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the **[DEBUG_GUIDE.md](DEBUG_GUIDE.md)**
2. Verify all dependencies are installed
3. Check that Ollama is running
4. Test API endpoints manually
5. Check browser console for errors

---

**Happy HVAC AI Assistant Development! 🏠❄️🤖** 