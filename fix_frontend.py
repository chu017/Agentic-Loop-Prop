#!/usr/bin/env python3
"""
Fix Frontend Dependencies Script
Resolves common frontend installation issues
"""

import subprocess
import os
import shutil
from pathlib import Path

def clean_installation():
    """Clean npm installation and reinstall"""
    print("🧹 Cleaning npm installation...")
    
    # Remove node_modules and package-lock.json
    if Path('node_modules').exists():
        shutil.rmtree('node_modules')
        print("✅ Removed node_modules")
    
    if Path('package-lock.json').exists():
        os.remove('package-lock.json')
        print("✅ Removed package-lock.json")
    
    # Clear npm cache
    try:
        subprocess.run(['npm', 'cache', 'clean', '--force'], 
                      capture_output=True, text=True)
        print("✅ Cleared npm cache")
    except Exception as e:
        print(f"⚠️  Could not clear npm cache: {e}")

def install_dependencies():
    """Install npm dependencies"""
    print("\n📦 Installing npm dependencies...")
    
    try:
        result = subprocess.run(['npm', 'install'], 
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

def verify_installation():
    """Verify that react-scripts is properly installed"""
    print("\n🔍 Verifying installation...")
    
    try:
        # Check if react-scripts is installed
        result = subprocess.run(['npx', 'react-scripts', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ react-scripts version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ react-scripts not found: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking react-scripts: {e}")
        return False

def test_build():
    """Test if the frontend can build"""
    print("\n🏗️  Testing build...")
    
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Build successful")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def main():
    """Main function"""
    print("HVAC AI Assistant - Frontend Fix")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('package.json').exists():
        print("❌ package.json not found. Please run this script from the project root directory.")
        return
    
    # Clean installation
    clean_installation()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies.")
        return
    
    # Verify installation
    if not verify_installation():
        print("\n❌ react-scripts not properly installed.")
        return
    
    # Test build
    if not test_build():
        print("\n❌ Build test failed.")
        return
    
    print("\n🎉 Frontend is now properly configured!")
    print("\nYou can now start the frontend with:")
    print("  npm start")
    print("\nOr use the unified startup script:")
    print("  python start_system.py")

if __name__ == "__main__":
    main() 