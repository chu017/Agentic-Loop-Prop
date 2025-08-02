#!/usr/bin/env python3
"""
Comprehensive Backend Fix Script
Resolves all backend dependency and configuration issues
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_python_dependencies():
    """Install all Python dependencies"""
    print("\nInstalling Python dependencies...")
    
    # Upgrade pip first
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      capture_output=True, text=True)
        print("✅ Upgraded pip")
    except Exception as e:
        print(f"⚠️  Could not upgrade pip: {e}")
    
    # Install core dependencies
    core_deps = [
        'flask==2.3.3',
        'flask-cors==4.0.0',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
        'numpy==1.24.3',
        'pandas==2.0.3'
    ]
    
    for dep in core_deps:
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {dep}")
            else:
                print(f"❌ Failed to install {dep}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error installing {dep}: {e}")
    
    # Install AI/ML dependencies
    ai_deps = [
        'sentence-transformers==2.2.2',
        'faiss-cpu==1.7.4',
        'langchain==0.0.350',
        'langchain-community==0.0.1',
        'ollama==0.1.7'
    ]
    
    for dep in ai_deps:
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {dep}")
            else:
                print(f"❌ Failed to install {dep}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error installing {dep}: {e}")
    
    # Install Thermia API
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 
                               'git+https://github.com/klejejs/python-thermia-online-api.git'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Thermia API installed")
        else:
            print(f"❌ Failed to install Thermia API: {result.stderr}")
    except Exception as e:
        print(f"❌ Error installing Thermia API: {e}")

def check_ollama():
    """Check and start Ollama"""
    print("\nChecking Ollama...")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama not installed")
            print("Install with: curl -fsSL https://ollama.ai/install.sh | sh")
            return False
    except FileNotFoundError:
        print("❌ Ollama not installed")
        print("Install with: curl -fsSL https://ollama.ai/install.sh | sh")
        return False
    
    # Check if Ollama is running
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("❌ Ollama is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Ollama is not running: {e}")
        print("Start with: ollama serve")
        return False

def pull_ollama_model():
    """Pull the required Ollama model"""
    print("\nPulling Ollama model...")
    
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

def create_env_file():
    """Create .env file with default configuration"""
    print("\nCreating environment configuration...")
    
    env_content = """# Flask Configuration
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# AI Model Configuration
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434

# Thermia API Configuration (optional)
# THERMIA_USERNAME=your_username
# THERMIA_PASSWORD=your_password

# Logging Configuration
LOG_LEVEL=INFO
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def test_imports():
    """Test all critical imports"""
    print("\nTesting imports...")
    
    imports_to_test = [
        ('flask', 'Flask'),
        ('flask_cors', 'CORS'),
        ('langchain', 'langchain'),
        ('sentence_transformers', 'SentenceTransformer'),
        ('faiss', 'faiss'),
        ('ollama', 'ollama'),
        ('ThermiaOnlineAPI', 'Thermia'),
        ('requests', 'requests'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas')
    ]
    
    all_successful = True
    
    for module, import_name in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_successful = False
    
    return all_successful

def test_ai_system():
    """Test AI system initialization"""
    print("\nTesting AI system...")
    
    try:
        from scripts.ai_rag_chat import AIRAGChat
        ai_system = AIRAGChat()
        print("✅ AI system initialized successfully")
        return True
    except Exception as e:
        print(f"❌ AI system initialization failed: {e}")
        return False

def test_backend():
    """Test backend startup"""
    print("\nTesting backend...")
    
    try:
        import app
        print("✅ Backend imports successful")
        return True
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False

def main():
    """Main function"""
    print("HVAC AI Assistant - Backend Fix")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    install_python_dependencies()
    
    # Create environment file
    create_env_file()
    
    # Test imports
    if not test_imports():
        print("\n❌ Some imports failed. Please check the errors above.")
        return
    
    # Test backend
    if not test_backend():
        print("\n❌ Backend test failed.")
        return
    
    # Check Ollama
    ollama_ok = check_ollama()
    if not ollama_ok:
        print("\n⚠️  Ollama is not running. AI features will not work.")
        print("To install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        print("To start Ollama: ollama serve")
        print("To pull model: ollama pull mistral")
        
        response = input("\nContinue without Ollama? (y/N): ")
        if response.lower() != 'y':
            return
    else:
        # Pull model if Ollama is running
        pull_ollama_model()
    
    # Test AI system
    if not test_ai_system():
        print("\n❌ AI system test failed.")
        return
    
    print("\n🎉 Backend is now properly configured!")
    print("\nYou can now start the backend with:")
    print("  python app.py")
    print("\nOr use the unified startup script:")
    print("  python start_system.py")

if __name__ == "__main__":
    main() 