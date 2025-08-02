#!/usr/bin/env python3
"""
Simple startup script for the HVAC AI Assistant Backend
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_dependencies():
    """Check if required Python dependencies are installed"""
    print("Checking Python dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'langchain',
        'faiss_cpu',
        'sentence_transformers',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_ollama():
    """Check if Ollama is running"""
    print("\nChecking Ollama...")
    
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
        print("Please start Ollama with: ollama serve")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    
    try:
        result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def start_backend():
    """Start the Flask backend"""
    print("\nStarting Flask backend...")
    print("The backend will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the Flask app
        subprocess.run(['python', 'app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def main():
    """Main function"""
    print("HVAC AI Assistant Backend Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ app.py not found. Please run this script from the project root directory.")
        return
    
    # Check Python dependencies
    if not check_python_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("\n❌ Failed to install dependencies.")
            return
    
    # Check Ollama (optional but recommended)
    print("\nChecking Ollama status...")
    if not check_ollama():
        print("\n⚠️  Ollama is not running. The AI features may not work properly.")
        print("To install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        print("To start Ollama: ollama serve")
        print("To pull the model: ollama pull mistral")
        
        response = input("\nContinue without Ollama? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Start the backend
    start_backend()

if __name__ == "__main__":
    main() 