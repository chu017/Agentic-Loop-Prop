#!/usr/bin/env python3
"""
Sentence Transformers Import Diagnostic
Comprehensive analysis of the sentence-transformers import issue
"""

import os
import sys
import subprocess
import importlib
import traceback
from pathlib import Path

def check_python_environment():
    """Check Python environment details"""
    print("🐍 Python Environment Analysis")
    print("=" * 50)
    
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Path: {sys.path[:3]}...")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Platform: {sys.platform}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("❌ Not running in virtual environment")

def check_package_installation():
    """Check if sentence-transformers is properly installed"""
    print("\n📦 Package Installation Check")
    print("=" * 50)
    
    try:
        # Check pip list
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            sentence_transformers_found = False
            transformers_found = False
            torch_found = False
            
            for line in lines:
                if 'sentence-transformers' in line:
                    print(f"✅ Found: {line.strip()}")
                    sentence_transformers_found = True
                elif 'transformers' in line:
                    print(f"✅ Found: {line.strip()}")
                    transformers_found = True
                elif 'torch' in line:
                    print(f"✅ Found: {line.strip()}")
                    torch_found = True
            
            if not sentence_transformers_found:
                print("❌ sentence-transformers not found in pip list")
            if not transformers_found:
                print("❌ transformers not found in pip list")
            if not torch_found:
                print("❌ torch not found in pip list")
                
        else:
            print(f"❌ pip list failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error checking package installation: {e}")

def check_import_attempts():
    """Test different import approaches"""
    print("\n🔍 Import Attempt Analysis")
    print("=" * 50)
    
    import_tests = [
        ("Direct import", "import sentence_transformers"),
        ("From import", "from sentence_transformers import SentenceTransformer"),
        ("LangChain import", "from langchain_community.embeddings import HuggingFaceEmbeddings"),
        ("Full path import", "import sentence_transformers.SentenceTransformer"),
    ]
    
    for test_name, import_statement in import_tests:
        print(f"\n--- Testing: {test_name} ---")
        print(f"Statement: {import_statement}")
        
        try:
            # Create a new namespace for testing
            test_namespace = {}
            exec(import_statement, test_namespace)
            print("✅ Import successful")
            
            # Try to get version info
            if 'sentence_transformers' in test_namespace:
                try:
                    version = test_namespace['sentence_transformers'].__version__
                    print(f"✅ Version: {version}")
                except:
                    print("✅ Imported but no version info")
                    
        except Exception as e:
            print(f"❌ Import failed: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"Full traceback:")
            traceback.print_exc()

def check_file_locations():
    """Check where sentence-transformers files are located"""
    print("\n📁 File Location Analysis")
    print("=" * 50)
    
    try:
        # Try to find sentence_transformers module
        import sentence_transformers
        print(f"✅ Module location: {sentence_transformers.__file__}")
        print(f"✅ Module directory: {os.path.dirname(sentence_transformers.__file__)}")
        
        # Check if it's a directory
        if os.path.isdir(sentence_transformers.__file__):
            print("✅ Module is a directory (package)")
        else:
            print("❌ Module is not a directory")
            
    except Exception as e:
        print(f"❌ Cannot locate sentence_transformers module: {e}")
    
    # Check site-packages
    try:
        import site
        for path in site.getsitepackages():
            sentence_transformers_path = os.path.join(path, 'sentence_transformers')
            if os.path.exists(sentence_transformers_path):
                print(f"✅ Found in site-packages: {sentence_transformers_path}")
            else:
                print(f"❌ Not found in: {path}")
    except Exception as e:
        print(f"❌ Error checking site-packages: {e}")

def check_dependencies():
    """Check sentence-transformers dependencies"""
    print("\n🔗 Dependency Analysis")
    print("=" * 50)
    
    dependencies = [
        'torch',
        'transformers',
        'numpy',
        'scipy',
        'huggingface_hub',
        'sentencepiece',
        'tqdm'
    ]
    
    for dep in dependencies:
        try:
            module = importlib.import_module(dep)
            print(f"✅ {dep}: {module.__file__}")
            
            # Try to get version
            try:
                version = getattr(module, '__version__', 'unknown')
                print(f"   Version: {version}")
            except:
                print(f"   Version: unknown")
                
        except Exception as e:
            print(f"❌ {dep}: {e}")

def check_langchain_imports():
    """Check LangChain specific imports"""
    print("\n🤖 LangChain Import Analysis")
    print("=" * 50)
    
    langchain_imports = [
        ("langchain_community.embeddings", "from langchain_community.embeddings import HuggingFaceEmbeddings"),
        ("langchain_community.vectorstores", "from langchain_community.vectorstores import FAISS"),
        ("langchain_community.llms", "from langchain_community.llms import Ollama"),
        ("langchain.chains", "from langchain.chains import RetrievalQA"),
        ("langchain.prompts", "from langchain.prompts import PromptTemplate"),
    ]
    
    for module_name, import_statement in langchain_imports:
        print(f"\n--- Testing: {module_name} ---")
        try:
            test_namespace = {}
            exec(import_statement, test_namespace)
            print("✅ Import successful")
        except Exception as e:
            print(f"❌ Import failed: {e}")
            print(f"Error type: {type(e).__name__}")

def check_environment_variables():
    """Check environment variables that might affect imports"""
    print("\n🌍 Environment Variables Analysis")
    print("=" * 50)
    
    relevant_vars = [
        'PYTHONPATH',
        'PYTHONHOME',
        'VIRTUAL_ENV',
        'CONDA_DEFAULT_ENV',
        'LD_LIBRARY_PATH',
        'CUDA_VISIBLE_DEVICES'
    ]
    
    for var in relevant_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def check_system_libraries():
    """Check system libraries that might be missing"""
    print("\n🔧 System Libraries Analysis")
    print("=" * 50)
    
    try:
        import ctypes
        print("✅ ctypes available")
    except Exception as e:
        print(f"❌ ctypes error: {e}")
    
    try:
        import numpy
        print(f"✅ numpy available: {numpy.__version__}")
    except Exception as e:
        print(f"❌ numpy error: {e}")
    
    try:
        import torch
        print(f"✅ torch available: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except Exception as e:
        print(f"❌ torch error: {e}")

def run_ai_system_test():
    """Test the actual AI system initialization"""
    print("\n🤖 AI System Initialization Test")
    print("=" * 50)
    
    try:
        # Add scripts directory to path
        current_dir = Path(__file__).parent
        scripts_dir = current_dir / 'scripts'
        
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        
        print("✅ Added scripts directory to path")
        
        # Try to import the AI system
        try:
            from ai_rag_chat import AIRAGChat
            print("✅ AIRAGChat class imported successfully")
            
            # Try to initialize
            try:
                ai_system = AIRAGChat()
                print("✅ AI system initialized successfully")
                return True
            except Exception as e:
                print(f"❌ AI system initialization failed: {e}")
                print("Full traceback:")
                traceback.print_exc()
                return False
                
        except Exception as e:
            print(f"❌ Failed to import AIRAGChat: {e}")
            print("Full traceback:")
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error in AI system test: {e}")
        return False

def generate_fix_suggestions():
    """Generate suggestions to fix the import issue"""
    print("\n🔧 Fix Suggestions")
    print("=" * 50)
    
    print("Based on the analysis, here are potential fixes:")
    print()
    print("1. Reinstall sentence-transformers:")
    print("   pip uninstall sentence-transformers")
    print("   pip install sentence-transformers==2.2.2")
    print()
    print("2. Check Python environment:")
    print("   python -c 'import sys; print(sys.path)'")
    print()
    print("3. Install in user space:")
    print("   pip install --user sentence-transformers==2.2.2")
    print()
    print("4. Check for conflicting packages:")
    print("   pip list | grep -i sentence")
    print()
    print("5. Try alternative installation:")
    print("   pip install git+https://github.com/UKPLab/sentence-transformers.git")
    print()
    print("6. Check system dependencies:")
    print("   sudo apt-get install python3-dev build-essential")
    print()
    print("7. Use conda instead of pip:")
    print("   conda install -c conda-forge sentence-transformers")

def main():
    """Main diagnostic function"""
    print("🔍 Sentence Transformers Import Diagnostic")
    print("=" * 60)
    print(f"Timestamp: {__import__('datetime').datetime.now()}")
    print()
    
    # Run all diagnostic tests
    tests = [
        ("Python Environment", check_python_environment),
        ("Package Installation", check_package_installation),
        ("Import Attempts", check_import_attempts),
        ("File Locations", check_file_locations),
        ("Dependencies", check_dependencies),
        ("LangChain Imports", check_langchain_imports),
        ("Environment Variables", check_environment_variables),
        ("System Libraries", check_system_libraries),
        ("AI System Test", run_ai_system_test)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Diagnostic Summary")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All diagnostic tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the detailed logs above.")
        generate_fix_suggestions()
    
    print(f"\n📋 Detailed logs saved to: sentence_transformers_diagnostic.log")
    
    # Save detailed log
    with open('sentence_transformers_diagnostic.log', 'w') as f:
        f.write("Sentence Transformers Import Diagnostic Log\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp: {__import__('datetime').datetime.now()}\n\n")
        
        # Re-run tests and capture output
        import io
        import contextlib
        
        for test_name, test_func in tests:
            f.write(f"\n{'='*50}\n")
            f.write(f"Test: {test_name}\n")
            f.write(f"{'='*50}\n")
            
            # Capture output
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                try:
                    test_func()
                except Exception as e:
                    f.write(f"Error: {e}\n")
                    traceback.print_exc(file=f)
            
            f.write(output.getvalue())

if __name__ == "__main__":
    main() 