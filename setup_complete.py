#!/usr/bin/env python3
"""
Complete Setup Script for HVAC AI Assistant
Handles all configuration, installation, and setup steps
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    print("📝 Creating environment configuration...")
    
    env_content = """# Flask Configuration
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=hvac-ai-assistant-secret-key-2024

# AI Model Configuration
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT=30

# Thermia API Configuration
# Uncomment and fill in your Thermia credentials for real API access
# THERMIA_USERNAME=your_thermia_username
# THERMIA_PASSWORD=your_thermia_password
# THERMIA_API_URL=https://api.thermia.com

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=ai_assistant.log

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000
REACT_APP_DEBUG=true

# Security Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ALLOWED_HOSTS=localhost,127.0.0.1

# AI System Configuration
KNOWLEDGE_BASE_DIR=context
VECTOR_STORE_PATH=vector_store
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RESULTS=5

# Thermia Mock Data Configuration
USE_MOCK_DATA=true
MOCK_SYSTEMS_COUNT=3
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def install_ollama():
    """Install Ollama if not already installed"""
    print("\n🤖 Installing Ollama...")
    
    try:
        # Check if Ollama is already installed
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama already installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    # Install Ollama
    try:
        print("Installing Ollama...")
        result = subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            install_script = result.stdout
            # Execute the install script
            install_process = subprocess.run(['sh'], input=install_script, text=True)
            if install_process.returncode == 0:
                print("✅ Ollama installed successfully")
                return True
            else:
                print("❌ Failed to install Ollama")
                return False
        else:
            print("❌ Failed to download Ollama install script")
            return False
    except Exception as e:
        print(f"❌ Error installing Ollama: {e}")
        print("Please install manually: curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def start_ollama():
    """Start Ollama service"""
    print("\n🚀 Starting Ollama service...")
    
    try:
        # Check if Ollama is running
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is already running")
            return True
    except Exception:
        pass
    
    # Start Ollama in background
    try:
        process = subprocess.Popen(['ollama', 'serve'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for Ollama to start
        import time
        time.sleep(3)
        
        # Check if it's running
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                print("✅ Ollama started successfully")
                return True
            else:
                print("❌ Ollama failed to start properly")
                return False
        except Exception:
            print("❌ Ollama failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def create_custom_model():
    """Create custom HVAC model using Modelfile"""
    print("\n🏗️  Creating custom HVAC model...")
    
    try:
        # Check if Modelfile exists
        modelfile = Path('Modelfile')
        if not modelfile.exists():
            print("❌ Modelfile not found")
            return False
        
        # Create the custom model
        result = subprocess.run(['ollama', 'create', 'hvac-assistant', '-f', 'Modelfile'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Custom HVAC model created successfully")
            return True
        else:
            print(f"❌ Failed to create model: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        return False

def pull_base_model():
    """Pull the base Mistral model"""
    print("\n📥 Pulling base Mistral model...")
    
    try:
        result = subprocess.run(['ollama', 'pull', 'mistral'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Mistral model pulled successfully")
            return True
        else:
            print(f"❌ Failed to pull model: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return False

def install_python_dependencies():
    """Install all Python dependencies"""
    print("\n🐍 Installing Python dependencies...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Python dependencies installed")
            return True
        else:
            print(f"❌ Failed to install Python dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing Python dependencies: {e}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("\n📦 Installing Node.js dependencies...")
    
    try:
        result = subprocess.run(['npm', 'install'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Node.js dependencies installed")
            return True
        else:
            print(f"❌ Failed to install Node.js dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing Node.js dependencies: {e}")
        return False

def test_system():
    """Test the complete system"""
    print("\n🧪 Testing system...")
    
    # Test Python imports
    try:
        from scripts.ai_rag_chat import AIRAGChat
        print("✅ AI system import successful")
    except Exception as e:
        print(f"❌ AI system import failed: {e}")
        return False
    
    # Test AI system initialization
    try:
        ai_system = AIRAGChat()
        print("✅ AI system initialized")
    except Exception as e:
        print(f"❌ AI system initialization failed: {e}")
        return False
    
    # Test Ollama connection
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama connection successful")
        else:
            print("❌ Ollama connection failed")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False
    
    # Test frontend build
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Frontend build successful")
        else:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Frontend build failed: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("HVAC AI Assistant - Complete Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('app.py').exists() or not Path('package.json').exists():
        print("❌ Required files not found. Please run this script from the project root directory.")
        return
    
    # Step 1: Create environment file
    create_env_file()
    
    # Step 2: Install Python dependencies
    if not install_python_dependencies():
        print("\n❌ Failed to install Python dependencies.")
        return
    
    # Step 3: Install Node.js dependencies
    if not install_node_dependencies():
        print("\n❌ Failed to install Node.js dependencies.")
        return
    
    # Step 4: Install Ollama
    if not install_ollama():
        print("\n⚠️  Ollama installation failed. Please install manually.")
        print("Run: curl -fsSL https://ollama.ai/install.sh | sh")
    
    # Step 5: Start Ollama
    if not start_ollama():
        print("\n⚠️  Ollama failed to start. Please start manually.")
        print("Run: ollama serve")
    
    # Step 6: Pull base model
    if not pull_base_model():
        print("\n⚠️  Failed to pull base model.")
        print("Run: ollama pull mistral")
    
    # Step 7: Create custom model
    if not create_custom_model():
        print("\n⚠️  Failed to create custom model.")
        print("The system will use the base Mistral model.")
    
    # Step 8: Test system
    if not test_system():
        print("\n❌ System test failed.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the system: python start_system.py")
    print("2. Access frontend: http://localhost:3000")
    print("3. Access backend: http://localhost:5000")
    print("\n🔧 If you have Thermia credentials:")
    print("1. Edit .env file")
    print("2. Uncomment THERMIA_USERNAME and THERMIA_PASSWORD")
    print("3. Add your credentials")
    print("4. Restart the system")

if __name__ == "__main__":
    main() 