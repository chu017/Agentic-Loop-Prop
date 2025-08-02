#!/usr/bin/env python3
"""
Comprehensive Test Runner for AI Assistant System
Runs all tests including AI system, Thermia API, and n8n compatibility
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_command(cmd, description, timeout=300):
    """Run a command and return results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=project_root
        )
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print("Error:")
                print(result.stderr)
            if result.stdout:
                print("Output:")
                print(result.stdout)
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT")
        return {
            'success': False,
            'error': 'Command timed out',
            'returncode': -1
        }
    except Exception as e:
        print(f"💥 EXCEPTION: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'returncode': -1
        }

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking Dependencies...")
    print("=" * 60)
    
    dependencies = [
        ('python', '--version', 'Python'),
        ('pip', '--version', 'pip'),
        ('node', '--version', 'Node.js'),
        ('npm', '--version', 'npm'),
        ('ollama', '--version', 'Ollama')
    ]
    
    results = {}
    
    for cmd, arg, name in dependencies:
        result = run_command([cmd, arg], f"Checking {name}")
        results[name] = result['success']
        
        if result['success']:
            print(f"✅ {name} is available")
        else:
            print(f"❌ {name} is not available or not working")
    
    return results

def install_python_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python Dependencies...")
    print("=" * 60)
    
    result = run_command(
        ['pip', 'install', '-r', 'requirements.txt'],
        "Installing Python dependencies from requirements.txt"
    )
    
    return result['success']

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("\nInstalling Node.js Dependencies...")
    print("=" * 60)
    
    result = run_command(
        ['npm', 'install'],
        "Installing Node.js dependencies"
    )
    
    return result['success']

def test_ai_system():
    """Test AI system functionality"""
    print("\nTesting AI System...")
    print("=" * 60)
    
    # Test AI RAG chat system
    result = run_command(
        [sys.executable, 'scripts/ai_rag_chat.py'],
        "Testing AI RAG chat system"
    )
    
    return result['success']

def test_thermia_integration():
    """Test Thermia API integration"""
    print("\nTesting Thermia API Integration...")
    print("=" * 60)
    
    # Test Thermia integration
    result = run_command(
        [sys.executable, 'scripts/thermia_integration.py'],
        "Testing Thermia integration"
    )
    
    return result['success']

def test_flask_api():
    """Test Flask API endpoints"""
    print("\nTesting Flask API...")
    print("=" * 60)
    
    # Start Flask server in background
    flask_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Wait for server to start
        time.sleep(5)
        
        # Test API endpoints
        import requests
        
        endpoints_to_test = [
            ('GET', '/api/health', 'Health check'),
            ('GET', '/api/system-status', 'System status'),
            ('POST', '/api/chat', 'Chat endpoint', {'message': 'Test message'}),
            ('GET', '/api/hvac/systems', 'HVAC systems'),
            ('GET', '/api/hvac/status', 'HVAC status')
        ]
        
        success_count = 0
        total_count = len(endpoints_to_test)
        
        for method, endpoint, description, *args in endpoints_to_test:
            try:
                url = f"http://localhost:5000{endpoint}"
                
                if method == 'GET':
                    response = requests.get(url, timeout=5)
                elif method == 'POST':
                    data = args[0] if args else {}
                    response = requests.post(url, json=data, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ {description}: {response.status_code}")
                    success_count += 1
                else:
                    print(f"❌ {description}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {description}: Error - {str(e)}")
        
        return success_count == total_count
        
    finally:
        # Clean up Flask process
        flask_process.terminate()
        try:
            flask_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            flask_process.kill()

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print("\nRunning Comprehensive Test Suite...")
    print("=" * 60)
    
    # Run test files
    test_files = [
        ('tests/test_ai_system.py', 'AI System Tests'),
        ('tests/test_thermia_api.py', 'Thermia API Tests'),
        ('tests/test_n8n_compatibility.py', 'N8N Compatibility Tests')
    ]
    
    results = {}
    
    for test_file, description in test_files:
        if Path(test_file).exists():
            result = run_command(
                [sys.executable, test_file],
                f"Running {description}"
            )
            results[description] = result['success']
        else:
            print(f"⚠️  Test file not found: {test_file}")
            results[description] = False
    
    return results

def test_react_frontend():
    """Test React frontend"""
    print("\nTesting React Frontend...")
    print("=" * 60)
    
    # Check if node_modules exists
    if not Path('node_modules').exists():
        print("Installing Node.js dependencies first...")
        install_node_dependencies()
    
    # Test React build
    result = run_command(
        ['npm', 'run', 'build'],
        "Testing React build process"
    )
    
    return result['success']

def generate_test_report(results):
    """Generate comprehensive test report"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TEST REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().isoformat()}")
    print()
    
    # Summary
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    failed_tests = total_tests - passed_tests
    
    print(f"TOTAL TESTS: {total_tests}")
    print(f"PASSED: {passed_tests}")
    print(f"FAILED: {failed_tests}")
    print(f"SUCCESS RATE: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    # Detailed results
    print("DETAILED RESULTS:")
    print("-" * 40)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print()
    
    # Recommendations
    print("RECOMMENDATIONS:")
    print("-" * 40)
    
    if failed_tests == 0:
        print("🎉 All tests passed! The system is ready for deployment.")
        print("✅ AI system is working correctly")
        print("✅ Thermia API integration is functional")
        print("✅ N8N compatibility is confirmed")
        print("✅ React frontend is buildable")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        
        if not results.get('Dependencies', True):
            print("🔧 Install missing dependencies")
        
        if not results.get('AI System', True):
            print("🤖 Check AI system configuration and Ollama setup")
        
        if not results.get('Thermia API', True):
            print("🌡️  Verify Thermia API credentials and connection")
        
        if not results.get('Flask API', True):
            print("🌐 Check Flask server configuration and dependencies")
        
        if not results.get('React Frontend', True):
            print("⚛️  Verify Node.js setup and React dependencies")
    
    # Save report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests/total_tests)*100 if total_tests > 0 else 0
        },
        'results': results
    }
    
    report_file = project_root / 'test_report.json'
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📊 Detailed report saved to: {report_file}")
    
    return failed_tests == 0

def main():
    """Main test runner function"""
    print("AI Assistant System - Comprehensive Test Suite")
    print("=" * 60)
    print(f"Project: {project_root}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = {}
    
    # Check dependencies
    print("\n1. Checking Dependencies...")
    dep_results = check_dependencies()
    results['Dependencies'] = all(dep_results.values())
    
    # Install dependencies if needed
    if not results['Dependencies']:
        print("\nInstalling missing dependencies...")
        install_python_dependencies()
        install_node_dependencies()
    
    # Test AI system
    print("\n2. Testing AI System...")
    results['AI System'] = test_ai_system()
    
    # Test Thermia integration
    print("\n3. Testing Thermia API Integration...")
    results['Thermia API'] = test_thermia_integration()
    
    # Test Flask API
    print("\n4. Testing Flask API...")
    results['Flask API'] = test_flask_api()
    
    # Test React frontend
    print("\n5. Testing React Frontend...")
    results['React Frontend'] = test_react_frontend()
    
    # Run comprehensive tests
    print("\n6. Running Comprehensive Tests...")
    comprehensive_results = run_comprehensive_tests()
    results.update(comprehensive_results)
    
    # Generate report
    success = generate_test_report(results)
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("The AI Assistant system is ready for use.")
        print("\nNext steps:")
        print("1. Start the system: python start_ai_assistant.py")
        print("2. Access the frontend: http://localhost:3000")
        print("3. Test the API: http://localhost:5000/api/health")
        print("4. Import n8n workflow: n8n-workflow-example.json")
    else:
        print("⚠️  SOME TESTS FAILED!")
        print("Please review the errors above and fix issues before deployment.")
    
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 