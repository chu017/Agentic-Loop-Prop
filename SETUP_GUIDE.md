# HVAC AI Assistant - Complete Setup Guide

This guide will walk you through setting up the complete HVAC AI Assistant system, including all dependencies, configuration files, and API keys.

## 🎯 **What You Need to Set Up**

### **1. Environment Configuration (.env file)**
### **2. Ollama Installation & Model Setup**
### **3. Thermia API Credentials (Optional)**
### **4. Custom AI Model Configuration**

## 🚀 **Quick Setup (Recommended)**

Run the complete setup script:

```bash
cd Agentic-Loop-Prop-backup
python setup_complete.py
```

This script will:
- ✅ Create `.env` file with all configurations
- ✅ Install all Python and Node.js dependencies
- ✅ Install and start Ollama
- ✅ Pull the Mistral model
- ✅ Create custom HVAC AI model
- ✅ Test the complete system

## 📋 **Manual Setup Steps**

### **Step 1: Environment Configuration**

Create a `.env` file in the project root:

```bash
cp env.example .env
```

**Required Configuration:**
```env
# Flask Configuration
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=hvac-ai-assistant-secret-key-2024

# AI Model Configuration
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT=30

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000
REACT_APP_DEBUG=true

# AI System Configuration
KNOWLEDGE_BASE_DIR=context
VECTOR_STORE_PATH=vector_store
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RESULTS=5

# Thermia Mock Data Configuration
USE_MOCK_DATA=true
MOCK_SYSTEMS_COUNT=3
```

**Optional Thermia API Configuration:**
```env
# Uncomment and fill in for real API access
# THERMIA_USERNAME=your_thermia_username
# THERMIA_PASSWORD=your_thermia_password
# THERMIA_API_URL=https://api.thermia.com
```

### **Step 2: Install Dependencies**

**Python Dependencies:**
```bash
pip install -r requirements.txt
```

**Node.js Dependencies:**
```bash
npm install
```

### **Step 3: Install Ollama**

**Install Ollama:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Start Ollama Service:**
```bash
ollama serve
```

**Pull Base Model:**
```bash
ollama pull mistral
```

### **Step 4: Create Custom HVAC Model**

The system includes a `Modelfile` that creates a custom HVAC-specialized AI model:

```bash
ollama create hvac-assistant -f Modelfile
```

This creates a model with:
- ✅ HVAC-specific system prompt
- ✅ Thermia heat pump expertise
- ✅ Diagnostic and troubleshooting knowledge
- ✅ Energy efficiency optimization
- ✅ Safety and compliance guidelines

### **Step 5: Thermia API Setup (Optional)**

If you have Thermia credentials:

1. **Get Credentials:**
   - Visit: https://online.thermia.se
   - Create an account
   - Get your username and password

2. **Configure in .env:**
   ```env
   THERMIA_USERNAME=your_actual_username
   THERMIA_PASSWORD=your_actual_password
   USE_MOCK_DATA=false
   ```

3. **Test Connection:**
   ```bash
   python -c "from scripts.thermia_integration import ThermiaHVACIntegration; t = ThermiaHVACIntegration(); print('Connection successful' if t.thermia else 'Using mock data')"
   ```

## 🔧 **Configuration Details**

### **Environment Variables Explained**

| Variable | Purpose | Default |
|----------|---------|---------|
| `FLASK_PORT` | Backend API port | 5000 |
| `OLLAMA_MODEL` | AI model to use | mistral |
| `OLLAMA_HOST` | Ollama server URL | http://localhost:11434 |
| `USE_MOCK_DATA` | Use mock HVAC data | true |
| `KNOWLEDGE_BASE_DIR` | Knowledge base location | context |
| `VECTOR_STORE_PATH` | Vector store location | vector_store |

### **AI Model Configuration**

The custom HVAC model includes:

**System Prompt:**
- HVAC system diagnostics
- Thermia heat pump expertise
- Energy efficiency optimization
- Maintenance procedures
- Safety standards

**Model Parameters:**
- Temperature: 0.7 (balanced creativity)
- Top-p: 0.9 (focused responses)
- Context length: 4096 tokens
- Repeat penalty: 1.1

### **API Endpoints**

**Core Endpoints:**
- `GET /api/health` - System health
- `POST /api/chat` - AI chat interface
- `GET /api/system-status` - System status

**HVAC Endpoints:**
- `GET /api/hvac/systems` - Get HVAC systems
- `GET /api/hvac/systems/{id}/diagnose` - Diagnose system
- `POST /api/hvac/systems/{id}/temperature` - Set temperature
- `POST /api/hvac/systems/{id}/mode` - Set operation mode

## 🧪 **Testing Your Setup**

### **Run System Diagnostic:**
```bash
python diagnose_system.py
```

### **Test Individual Components:**

**Backend Test:**
```bash
python app.py
# In another terminal:
curl http://localhost:5000/api/health
```

**Frontend Test:**
```bash
npm start
# Access: http://localhost:3000
```

**AI System Test:**
```bash
python -c "from scripts.ai_rag_chat import AIRAGChat; ai = AIRAGChat(); print(ai.ask_question('What is a heat pump?'))"
```

**Ollama Test:**
```bash
ollama list
curl http://localhost:11434/api/tags
```

## 🚨 **Troubleshooting**

### **Common Issues:**

**1. Ollama Connection Failed:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

**2. Model Not Found:**
```bash
# Pull the model
ollama pull mistral

# Create custom model
ollama create hvac-assistant -f Modelfile
```

**3. Dependencies Missing:**
```bash
# Reinstall Python dependencies
pip install -r requirements.txt

# Reinstall Node.js dependencies
npm install
```

**4. Frontend Build Fails:**
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**5. Backend Import Errors:**
```bash
# Check Python version (need 3.8+)
python --version

# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt
```

### **Log Files:**

- **Backend logs:** `ai_flask_app.log`
- **AI system logs:** `ai_rag_chat.log`
- **Thermia logs:** `thermia_integration.log`

## 🎉 **Success Indicators**

Your setup is complete when:

✅ **Backend responds:** `curl http://localhost:5000/api/health` returns success
✅ **Frontend loads:** http://localhost:3000 shows the HVAC AI Assistant
✅ **AI responds:** Chat interface gives HVAC-specific answers
✅ **Ollama running:** `ollama list` shows available models
✅ **No errors:** All log files show successful initialization

## 📞 **Getting Help**

If you encounter issues:

1. **Run diagnostic:** `python diagnose_system.py`
2. **Check logs:** Look at the log files mentioned above
3. **Test components:** Use the individual test commands
4. **Verify configuration:** Ensure `.env` file is properly set up

---

**Happy HVAC AI Assistant Setup! 🏠❄️🤖** 