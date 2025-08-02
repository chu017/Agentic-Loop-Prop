#!/usr/bin/env python3
"""
Simple startup script for the HVAC AI Assistant Frontend
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
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
    """Install npm dependencies"""
    print("\nInstalling npm dependencies...")
    
    try:
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def start_frontend():
    """Start the React frontend"""
    print("\nStarting React frontend...")
    print("The frontend will be available at: http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the React development server
        subprocess.run(['npm', 'start'])
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main function"""
    print("HVAC AI Assistant Frontend Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('package.json').exists():
        print("❌ package.json not found. Please run this script from the project root directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Required dependencies not found.")
        print("Please install Node.js and npm from: https://nodejs.org/")
        return
    
    # Install dependencies if node_modules doesn't exist
    if not Path('node_modules').exists():
        if not install_dependencies():
            print("\n❌ Failed to install dependencies.")
            return
    
    # Start the frontend
    start_frontend()

if __name__ == "__main__":
    main() 