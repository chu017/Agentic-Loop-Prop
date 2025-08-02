#!/usr/bin/env python3
"""
Comprehensive System Diagnostic Script
Checks all components and identifies issues
"""

import subprocess
import sys
import os
from pathlib import Path
import json

def check_system_requirements():
    """Check basic system requirements"""
    print("🔍 System Requirements Check")
    print("=" * 40)
    
    # Python version
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python version too old. Need 3.8+")
        return False
    else:
        print("✅ Python version OK")
    
    # Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def check_python_dependencies():
    """Check Python dependencies"""
    print("\n🐍 Python Dependencies Check")
    print("=" * 40)
    
    dependencies = [
        'flask',
        'flask_cors',
        'langchain',
        'langchain_community',
        'sentence_transformers',
        'faiss',
        'ollama',
        'requests',
        'numpy',
        'pandas',
        'python_dotenv',
        'ThermiaOnlineAPI'
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - missing")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print("Run: python fix_backend.py")
        return False
    
    return True

def check_node_dependencies():
    """Check Node.js dependencies"""
    print("\n📦 Node.js Dependencies Check")
    print("=" * 40)
    
    if not Path('node_modules').exists():
        print("❌ node_modules not found")
        print("Run: npm install")
        return False
    
    if not Path('package.json').exists():
        print("❌ package.json not found")
        return False
    
    # Check react-scripts specifically
    try:
        result = subprocess.run(['npx', 'react-scripts', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ react-scripts: {result.stdout.strip()}")
        else:
            print("❌ react-scripts not found")
            return False
    except Exception as e:
        print(f"❌ Error checking react-scripts: {e}")
        return False
    
    return True

def check_ollama():
    """Check Ollama status"""
    print("\n🤖 Ollama Check")
    print("=" * 40)
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama not installed")
            return False
    except FileNotFoundError:
        print("❌ Ollama not installed")
        return False
    
    # Check if Ollama is running
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            
            # Check available models
            models_response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if models_response.status_code == 200:
                models = models_response.json()
                if 'models' in models and models['models']:
                    print(f"✅ Models available: {[m['name'] for m in models['models']]}")
                else:
                    print("⚠️  No models found. Run: ollama pull mistral")
            return True
        else:
            print("❌ Ollama is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Ollama is not running: {e}")
        return False

def check_backend():
    """Check backend functionality"""
    print("\n🔧 Backend Check")
    print("=" * 40)
    
    # Test imports
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
    
    # Test Flask app
    try:
        import app
        print("✅ Flask app import successful")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    return True

def check_frontend():
    """Check frontend functionality"""
    print("\n⚛️  Frontend Check")
    print("=" * 40)
    
    # Check if src directory exists
    if not Path('src').exists():
        print("❌ src directory not found")
        return False
    
    # Check key files
    key_files = [
        'src/App.tsx',
        'src/index.tsx',
        'src/components/',
        'public/index.html'
    ]
    
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - missing")
            return False
    
    # Test build
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Frontend builds successfully")
        else:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Build test failed: {e}")
        return False
    
    return True

def check_api_endpoints():
    """Check API endpoints"""
    print("\n🌐 API Endpoints Check")
    print("=" * 40)
    
    # Start backend if not running
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            return True
        else:
            print("❌ Backend not responding properly")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def generate_report():
    """Generate comprehensive report"""
    print("\n📊 System Diagnostic Report")
    print("=" * 40)
    
    checks = [
        ("System Requirements", check_system_requirements),
        ("Python Dependencies", check_python_dependencies),
        ("Node.js Dependencies", check_node_dependencies),
        ("Ollama Status", check_ollama),
        ("Backend Functionality", check_backend),
        ("Frontend Functionality", check_frontend),
        ("API Endpoints", check_api_endpoints)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results[check_name] = False
    
    # Summary
    print("\n📋 Summary")
    print("=" * 40)
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All systems operational!")
    else:
        print("\n🔧 Issues found. Run the following to fix:")
        print("  python fix_backend.py    # Fix backend issues")
        print("  python fix_frontend.py   # Fix frontend issues")
        print("  ollama serve             # Start Ollama")
        print("  ollama pull mistral      # Pull AI model")

def main():
    """Main function"""
    print("HVAC AI Assistant - System Diagnostic")
    print("=" * 50)
    
    generate_report()

if __name__ == "__main__":
    main() 