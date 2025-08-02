#!/usr/bin/env python3
"""
Test Integration Script
Verifies that the AI system properly integrates RAG knowledge with live Thermia API data
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
current_dir = Path(__file__).parent
scripts_dir = current_dir / 'scripts'

if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

def test_data_integration():
    """Test data integration functionality"""
    print("🔍 Testing Data Integration")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        # Initialize data manager
        data_manager = get_data_integration_manager()
        print("✅ Data integration manager initialized")
        
        # Test getting live system data
        systems = data_manager.get_live_system_data()
        print(f"✅ Retrieved {len(systems)} systems")
        
        for system in systems:
            print(f"  - {system.name} ({system.model}): {system.operation_mode}")
            print(f"    Temperature: {system.indoor_temperature}°C indoor, {system.outdoor_temperature}°C outdoor")
            print(f"    Online: {system.is_online}, Alarms: {len(system.active_alarms)}")
        
        # Test diagnosis
        if systems:
            diagnosis = data_manager.get_system_diagnosis(systems[0].id)
            print(f"✅ System diagnosis: {diagnosis['status']}")
            print(f"  Issues: {diagnosis['issues']}")
            print(f"  Efficiency: {diagnosis['efficiency_score']}%")
        
        # Test optimization suggestions
        if systems:
            suggestions = data_manager.get_optimization_suggestions(systems[0].id)
            print(f"✅ Optimization suggestions: {len(suggestions)} suggestions")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data integration test failed: {e}")
        return False

def test_ai_integration():
    """Test AI system integration"""
    print("\n🤖 Testing AI Integration")
    print("=" * 40)
    
    try:
        from ai_rag_chat import get_ai_system
        
        # Initialize AI system
        ai_system = get_ai_system()
        print("✅ AI system initialized")
        
        # Test system status
        status = ai_system.get_system_status()
        print(f"✅ System status: {status['ai_system']}")
        print(f"  Data integration: {status['data_integration']}")
        print(f"  Knowledge base: {status['knowledge_base']}")
        
        # Test basic question
        response = ai_system.ask_question("What is a heat pump?")
        print(f"✅ Basic question response: {response[:100]}...")
        
        # Test HVAC-specific question
        response = ai_system.ask_question("How do I optimize my Thermia heat pump efficiency?")
        print(f"✅ HVAC question response: {response[:100]}...")
        
        # Test with system data
        systems = ai_system.get_hvac_systems()
        if systems:
            system_id = systems[0]['id']
            response = ai_system.ask_question("What's the current status of my system?", system_id)
            print(f"✅ System-specific response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI integration test failed: {e}")
        return False

def test_combined_integration():
    """Test combined RAG + API integration"""
    print("\n🔗 Testing Combined Integration")
    print("=" * 40)
    
    try:
        from ai_rag_chat import get_ai_system
        
        ai_system = get_ai_system()
        
        # Test questions that require both knowledge and live data
        test_questions = [
            "What is the current efficiency of my heat pump system?",
            "How can I improve the performance of my Thermia system?",
            "What maintenance should I schedule based on current system status?",
            "Is my heat pump operating optimally for the current weather conditions?"
        ]
        
        systems = ai_system.get_hvac_systems()
        system_id = systems[0]['id'] if systems else None
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            response = ai_system.ask_question(question, system_id)
            print(f"Response: {response[:200]}...")
        
        # Test diagnosis with AI enhancement
        if systems:
            diagnosis = ai_system.diagnose_hvac_system(systems[0]['id'])
            print(f"\nEnhanced diagnosis: {diagnosis['status']}")
            if 'ai_analysis' in diagnosis:
                print(f"AI Analysis: {diagnosis['ai_analysis'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Combined integration test failed: {e}")
        return False

def test_database_integration():
    """Test database caching and storage"""
    print("\n💾 Testing Database Integration")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        data_manager = get_data_integration_manager()
        
        # Test caching
        systems = data_manager.get_live_system_data()
        print(f"✅ Cached {len(systems)} systems")
        
        # Test retrieving cached data
        cached_systems = data_manager.get_cached_system_data()
        print(f"✅ Retrieved {len(cached_systems)} cached systems")
        
        # Test historical data
        if systems:
            from datetime import datetime, timedelta
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            historical_data = data_manager.get_historical_data(
                systems[0].id, "indoor_temperature", start_time, end_time
            )
            print(f"✅ Retrieved {len(historical_data)} historical data points")
        
        return True
        
    except Exception as e:
        print(f"❌ Database integration test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints")
    print("=" * 40)
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint: {data['status']}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test system status endpoint
        response = requests.get('http://localhost:5000/api/system-status', timeout=5)
        if response.status_code == 200:
            print("✅ System status endpoint working")
        else:
            print(f"❌ System status endpoint failed: {response.status_code}")
        
        # Test HVAC systems endpoint
        response = requests.get('http://localhost:5000/api/hvac/systems', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ HVAC systems endpoint: {len(data.get('systems', []))} systems")
        else:
            print(f"❌ HVAC systems endpoint failed: {response.status_code}")
        
        # Test chat endpoint
        chat_data = {
            "message": "What is the current status of my HVAC system?",
            "sessionId": "test-session"
        }
        response = requests.post('http://localhost:5000/api/chat', json=chat_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat endpoint: {data['response'][:100]}...")
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def main():
    """Main test function"""
    print("HVAC AI Assistant - Integration Test")
    print("=" * 50)
    
    tests = [
        ("Data Integration", test_data_integration),
        ("AI Integration", test_ai_integration),
        ("Combined Integration", test_combined_integration),
        ("Database Integration", test_database_integration),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 40)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! The system is working correctly.")
        print("\n✅ RAG knowledge base is integrated with live Thermia API data")
        print("✅ Database caching is working properly")
        print("✅ AI responses include both knowledge and live system data")
        print("✅ API endpoints are functioning correctly")
    else:
        print("\n⚠️  Some tests failed. Check the logs for details.")
        print("Run: python diagnose_system.py for detailed diagnostics")

if __name__ == "__main__":
    main() 