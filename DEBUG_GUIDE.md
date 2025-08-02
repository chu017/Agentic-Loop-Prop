# HVAC AI Assistant - Debug Guide

This guide helps you troubleshoot common issues with the HVAC AI Assistant system.

## 🚨 Common Issues & Solutions

### **1. TypeScript Import Errors**

**Error**: `Cannot find module '@/lib/utils'`

**Solution**:
```bash
# Make sure you're in the project root
cd Agentic-Loop-Prop-backup

# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### **2. Proxy Errors (CORS Issues)**

**Error**: `Proxy error: Could not proxy request`

**Solution**:
1. Make sure the Flask backend is running:
   ```bash
   python app.py
   ```

2. Check that the backend is accessible:
   ```bash
   curl http://localhost:5000/api/health
   ```

3. Verify CORS configuration in `app.py`

### **3. API Connection Errors**

**Error**: `Failed to fetch` or `Network Error`

**Solutions**:
1. **Check backend is running**:
   ```bash
   # Terminal 1: Start Flask backend
   python app.py
   ```

2. **Check API endpoints**:
   ```bash
   curl http://localhost:5000/api/health
   curl http://localhost:5000/api/system-status
   ```

3. **Verify environment variables**:
   ```bash
   # Create .env file if it doesn't exist
   cp env.example .env
   ```

### **4. React Build Errors**

**Error**: `Module not found` or `Cannot resolve module`

**Solution**:
```bash
# Clear all caches
npm cache clean --force
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install

# Start fresh
npm start
```

### **5. Ollama Connection Issues**

**Error**: `Ollama not running` or `Model not found`

**Solution**:
```bash
# Install Ollama (if not installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull the required model
ollama pull mistral
```

### **6. Python Dependencies Issues**

**Error**: `ModuleNotFoundError` or `ImportError`

**Solution**:
```bash
# Install Python dependencies
pip install -r requirements.txt

# If using virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔧 **Step-by-Step Debug Process**

### **Step 1: Check System Requirements**
```bash
# Check Node.js version (should be 16+)
node --version

# Check npm version
npm --version

# Check Python version (should be 3.8+)
python --version

# Check if Ollama is installed
ollama --version
```

### **Step 2: Verify Project Structure**
```bash
# Should be in the project root
ls -la

# Should see these files:
# - package.json
# - requirements.txt
# - app.py
# - src/ (directory)
```

### **Step 3: Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### **Step 4: Start Backend**
```bash
# Start Flask backend
python app.py

# Should see: "Starting Flask app on port 5000"
# Test with: curl http://localhost:5000/api/health
```

### **Step 5: Start Frontend**
```bash
# In a new terminal
npm start

# Should open browser to http://localhost:3000
```

## 🐛 **Debugging Commands**

### **Check Backend Status**
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test system status
curl http://localhost:5000/api/system-status

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "sessionId": "test"}'
```

### **Check Frontend Build**
```bash
# Build for production
npm run build

# Check for TypeScript errors
npx tsc --noEmit
```

### **Check Logs**
```bash
# Backend logs
tail -f ai_flask_app.log

# AI system logs
tail -f ai_rag_chat.log

# Thermia integration logs
tail -f thermia_integration.log
```

## 🔍 **Common Error Messages**

### **TypeScript Errors**
- `TS2307: Cannot find module '@/lib/utils'` → Check path aliases in tsconfig.json
- `TS2339: Property does not exist` → Check interface definitions in types/index.ts

### **React Errors**
- `Module not found` → Run `npm install`
- `Proxy error` → Check if backend is running on port 5000
- `Failed to fetch` → Check CORS configuration

### **Python Errors**
- `ModuleNotFoundError` → Run `pip install -r requirements.txt`
- `ImportError` → Check Python path and virtual environment
- `Connection refused` → Check if Ollama is running

## 🛠️ **Advanced Debugging**

### **Enable Debug Mode**
```bash
# Set debug environment variable
export REACT_APP_DEBUG=true
npm start
```

### **Check Network Requests**
1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Check for failed requests to `/api/*` endpoints

### **Check Console Logs**
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Look for JavaScript errors

### **Test API Endpoints**
```bash
# Test all endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/system-status
curl http://localhost:5000/api/hvac/systems
```

## 📞 **Getting Help**

If you're still having issues:

1. **Check the logs** in the project directory
2. **Verify all dependencies** are installed
3. **Test each component** separately
4. **Check the browser console** for JavaScript errors
5. **Verify the API endpoints** are responding

### **Useful Commands for Debugging**
```bash
# Check if ports are in use
lsof -i :3000  # Frontend port
lsof -i :5000  # Backend port
lsof -i :11434 # Ollama port

# Check process status
ps aux | grep python
ps aux | grep node

# Check disk space
df -h

# Check memory usage
free -h
```

---

**Remember**: Always start the backend (Flask) before the frontend (React)! 