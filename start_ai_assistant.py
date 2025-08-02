#!/usr/bin/env python3
"""
AI Assistant Startup Script
Handles Ollama, Flask server, and React frontend for the AI assistant
"""

import os
import sys
import time
import subprocess
import signal
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_assistant_startup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AIAssistantStartup:
    def __init__(self):
        """Initialize AI assistant startup"""
        self.ollama_process = None
        self.flask_process = None
        self.react_process = None
        self.project_root = Path(__file__).parent
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        # Check Python packages
        required_packages = [
            'flask', 'langchain', 'faiss-cpu', 'sentence-transformers',
            'requests', 'flask-cors', 'python-dotenv'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✓ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"✗ {package} is missing")
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.info("Install missing packages with: pip install " + " ".join(missing_packages))
            return False
        
        # Check Ollama installation
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info(f"✓ Ollama is installed: {result.stdout.strip()}")
            else:
                logger.error("✗ Ollama is not properly installed")
                return False
        except FileNotFoundError:
            logger.error("✗ Ollama is not installed")
            logger.info("Install Ollama from: https://ollama.ai/")
            return False
        
        # Check Node.js and npm
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info(f"✓ Node.js is installed: {result.stdout.strip()}")
            else:
                logger.error("✗ Node.js is not properly installed")
                return False
        except FileNotFoundError:
            logger.error("✗ Node.js is not installed")
            logger.info("Install Node.js from: https://nodejs.org/")
            return False
        
        try:
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info(f"✓ npm is installed: {result.stdout.strip()}")
            else:
                logger.error("✗ npm is not properly installed")
                return False
        except FileNotFoundError:
            logger.error("✗ npm is not installed")
            logger.info("Install npm with Node.js")
            return False
        
        return True
    
    def check_ollama_connection(self):
        """Check if Ollama server is running"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                logger.info("✓ Ollama server is running")
                return True
            else:
                logger.warning("✗ Ollama server responded with error")
                return False
        except Exception as e:
            logger.warning(f"✗ Cannot connect to Ollama server: {e}")
            return False
    
    def start_ollama_server(self):
        """Start Ollama server if not running"""
        if self.check_ollama_connection():
            logger.info("Ollama server is already running")
            return True
        
        logger.info("Starting Ollama server...")
        try:
            self.ollama_process = subprocess.Popen(
                ['ollama', 'serve'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(3)
            
            if self.check_ollama_connection():
                logger.info("✓ Ollama server started successfully")
                return True
            else:
                logger.error("✗ Failed to start Ollama server")
                return False
                
        except Exception as e:
            logger.error(f"✗ Error starting Ollama server: {e}")
            return False
    
    def check_model_availability(self):
        """Check if required model is available"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                if 'mistral' in model_names:
                    logger.info("✓ Mistral model is available")
                    return True
                else:
                    logger.warning("✗ Mistral model not found")
                    return False
            else:
                logger.warning("✗ Cannot check model availability")
                return False
        except Exception as e:
            logger.warning(f"✗ Error checking model availability: {e}")
            return False
    
    def pull_model_if_needed(self):
        """Pull Mistral model if not available"""
        if self.check_model_availability():
            return True
        
        logger.info("Pulling Mistral model...")
        try:
            result = subprocess.run(['ollama', 'pull', 'mistral'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logger.info("✓ Mistral model pulled successfully")
                return True
            else:
                logger.error(f"✗ Failed to pull Mistral model: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"✗ Error pulling Mistral model: {e}")
            return False
    
    def start_flask_app(self):
        """Start Flask backend server"""
        logger.info("Starting Flask backend server...")
        try:
            self.flask_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )
            
            # Wait for Flask to start
            time.sleep(5)
            
            # Check if Flask is running
            try:
                import requests
                response = requests.get("http://localhost:5000/", timeout=3)
                if response.status_code == 200:
                    logger.info("✓ Flask backend server started successfully")
                    return True
                else:
                    logger.error("✗ Flask server responded with error")
                    return False
            except Exception as e:
                logger.error(f"✗ Cannot connect to Flask server: {e}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Error starting Flask server: {e}")
            return False
    
    def start_react_app(self):
        """Start React frontend"""
        logger.info("Starting React frontend...")
        try:
            # Install npm dependencies if needed
            if not (self.project_root / 'node_modules').exists():
                logger.info("Installing npm dependencies...")
                subprocess.run(['npm', 'install'], cwd=self.project_root, check=True)
            
            # Start React development server
            self.react_process = subprocess.Popen(
                ['npm', 'start'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )
            
            # Wait for React to start
            time.sleep(10)
            
            logger.info("✓ React frontend started successfully")
            logger.info("Frontend available at: http://localhost:3000")
            return True
                
        except Exception as e:
            logger.error(f"✗ Error starting React frontend: {e}")
            return False
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal, cleaning up...")
            self.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def cleanup(self):
        """Clean up processes on shutdown"""
        logger.info("Cleaning up processes...")
        
        if self.react_process:
            logger.info("Stopping React frontend...")
            self.react_process.terminate()
            try:
                self.react_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.react_process.kill()
        
        if self.flask_process:
            logger.info("Stopping Flask backend...")
            self.flask_process.terminate()
            try:
                self.flask_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.flask_process.kill()
        
        if self.ollama_process:
            logger.info("Stopping Ollama server...")
            self.ollama_process.terminate()
            try:
                self.ollama_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ollama_process.kill()
        
        logger.info("Cleanup completed")
    
    def run(self):
        """Run the AI assistant startup sequence"""
        logger.info("Starting AI Assistant...")
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Check dependencies
        if not self.check_dependencies():
            logger.error("Dependency check failed. Please install missing dependencies.")
            return False
        
        # Start Ollama server
        if not self.start_ollama_server():
            logger.error("Failed to start Ollama server.")
            return False
        
        # Pull model if needed
        if not self.pull_model_if_needed():
            logger.error("Failed to pull required model.")
            return False
        
        # Start Flask backend
        if not self.start_flask_app():
            logger.error("Failed to start Flask backend.")
            return False
        
        # Start React frontend
        if not self.start_react_app():
            logger.error("Failed to start React frontend.")
            return False
        
        logger.info("✓ AI Assistant started successfully!")
        logger.info("Frontend: http://localhost:3000")
        logger.info("Backend API: http://localhost:5000")
        logger.info("Press Ctrl+C to stop all services")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down AI Assistant...")
            self.cleanup()

def main():
    """Main function"""
    startup = AIAssistantStartup()
    startup.run()

if __name__ == "__main__":
    main() 