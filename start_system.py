#!/usr/bin/env python3
"""
Unified startup script for the HVAC AI Assistant System
Starts both backend and frontend services
"""

import os
import sys
import subprocess
import time
import threading
import signal
from pathlib import Path

# Global variables to track processes
backend_process = None
frontend_process = None

def signal_handler(signum, frame):
    """Handle Ctrl+C to gracefully stop all processes"""
    print("\n🛑 Shutting down all services...")
    
    if backend_process:
        backend_process.terminate()
        print("✅ Backend stopped")
    
    if frontend_process:
        frontend_process.terminate()
        print("✅ Frontend stopped")
    
    sys.exit(0)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking system dependencies...")
    
    # Check Python
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python: {result.stdout.strip()}")
        else:
            print("❌ Python not found")
            return False
    except FileNotFoundError:
        print("❌ Python not found")
        return False
    
    # Check Node.js
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
    
    # Check npm
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

def install_dependencies():
    """Install all dependencies"""
    print("\nInstalling dependencies...")
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    try:
        result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Python dependencies installed")
        else:
            print(f"❌ Failed to install Python dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing Python dependencies: {e}")
        return False
    
    # Install Node.js dependencies
    print("Installing Node.js dependencies...")
    try:
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Node.js dependencies installed")
        else:
            print(f"❌ Failed to install Node.js dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing Node.js dependencies: {e}")
        return False
    
    return True

def start_backend():
    """Start the Flask backend"""
    global backend_process
    
    print("Starting Flask backend...")
    try:
        backend_process = subprocess.Popen(
            ['python', 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("✅ Backend started successfully")
            return True
        else:
            stdout, stderr = backend_process.communicate()
            print(f"❌ Backend failed to start: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def start_frontend():
    """Start the React frontend"""
    global frontend_process
    
    print("Starting React frontend...")
    try:
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the server to start
        time.sleep(5)
        
        if frontend_process.poll() is None:
            print("✅ Frontend started successfully")
            return True
        else:
            stdout, stderr = frontend_process.communicate()
            print(f"❌ Frontend failed to start: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

def check_services():
    """Check if services are running"""
    print("\nChecking service status...")
    
    # Check backend
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is responding")
        else:
            print("❌ Backend is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Backend is not accessible: {e}")
        return False
    
    # Check frontend (optional)
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is responding")
        else:
            print("⚠️  Frontend may not be fully loaded yet")
    except Exception as e:
        print("⚠️  Frontend may not be fully loaded yet")
    
    return True

def main():
    """Main function"""
    print("HVAC AI Assistant System Startup")
    print("=" * 40)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if we're in the right directory
    if not Path('app.py').exists() or not Path('package.json').exists():
        print("❌ Required files not found. Please run this script from the project root directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Required dependencies not found.")
        print("Please install Node.js from: https://nodejs.org/")
        return
    
    # Install dependencies if needed
    if not Path('node_modules').exists() or not Path('venv').exists():
        if not install_dependencies():
            print("\n❌ Failed to install dependencies.")
            return
    
    # Start backend
    if not start_backend():
        print("\n❌ Failed to start backend.")
        return
    
    # Wait a moment for backend to fully start
    time.sleep(2)
    
    # Start frontend
    if not start_frontend():
        print("\n❌ Failed to start frontend.")
        return
    
    # Check services
    time.sleep(3)
    if check_services():
        print("\n🎉 System started successfully!")
        print("\n📱 Access the application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:5000")
        print("\nPress Ctrl+C to stop all services")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)
    else:
        print("\n❌ Some services failed to start properly.")
        print("Check the logs above for more information.")

if __name__ == "__main__":
    main() 