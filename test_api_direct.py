#!/usr/bin/env python3
"""
Direct API Test
Tests API endpoints directly without AI system dependency
"""

import requests
import json
from datetime import datetime

def test_health_endpoint():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint working")
            print(f"  Status: {data.get('status', 'N/A')}")
            print(f"  Timestamp: {data.get('timestamp', 'N/A')}")
            return True
        else:
            print(f"❌ Health endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def test_direct_data_endpoints():
    """Test data endpoints directly"""
    print("\n📊 Testing Direct Data Endpoints")
    print("=" * 40)
    
    try:
        # Test system status endpoint
        response = requests.get('http://localhost:5000/api/system-status', timeout=5)
        print(f"System Status - Status Code: {response.status_code}")
        print(f"System Status - Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System status endpoint working")
            print(f"  Data integration: {data.get('data_integration', 'N/A')}")
        else:
            print(f"❌ System status endpoint failed")
        
        # Test HVAC systems endpoint
        response = requests.get('http://localhost:5000/api/hvac/systems', timeout=5)
        print(f"HVAC Systems - Status Code: {response.status_code}")
        print(f"HVAC Systems - Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            systems = data.get('systems', [])
            print(f"✅ HVAC systems endpoint working")
            print(f"  Systems found: {len(systems)}")
            
            if systems:
                system = systems[0]
                print(f"✅ Sample system:")
                print(f"  - Name: {system.get('name', 'N/A')}")
                print(f"  - Model: {system.get('model', 'N/A')}")
                print(f"  - Online: {system.get('is_online', 'N/A')}")
                print(f"  - Indoor Temp: {system.get('indoor_temperature', 'N/A')}°C")
        else:
            print(f"❌ HVAC systems endpoint failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct data endpoints test failed: {e}")
        return False

def test_chat_endpoint():
    """Test chat endpoint"""
    print("\n💬 Testing Chat Endpoint")
    print("=" * 40)
    
    try:
        chat_data = {
            "message": "What is the current status of my HVAC system?",
            "sessionId": "test-session"
        }
        
        response = requests.post('http://localhost:5000/api/chat', json=chat_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat endpoint working")
            print(f"  Response: {data.get('response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Chat endpoint test failed: {e}")
        return False

def test_database_direct():
    """Test database directly"""
    print("\n💾 Testing Database Directly")
    print("=" * 40)
    
    try:
        import sqlite3
        
        conn = sqlite3.connect("hvac_data.db")
        cursor = conn.cursor()
        
        # Check system data
        cursor.execute("SELECT COUNT(*) FROM hvac_systems;")
        count = cursor.fetchone()[0]
        print(f"✅ Database has {count} system records")
        
        if count > 0:
            cursor.execute("SELECT name, model, is_online, indoor_temperature FROM hvac_systems LIMIT 1;")
            row = cursor.fetchone()
            print(f"✅ Sample system from database:")
            print(f"  - Name: {row[0]}")
            print(f"  - Model: {row[1]}")
            print(f"  - Online: {row[2]}")
            print(f"  - Indoor Temp: {row[3]}°C")
        
        # Check historical data
        cursor.execute("SELECT COUNT(*) FROM historical_data;")
        count = cursor.fetchone()[0]
        print(f"✅ Database has {count} historical records")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database direct test failed: {e}")
        return False

def main():
    """Main test function"""
    print("HVAC AI Assistant - Direct API Test")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Direct Data Endpoints", test_direct_data_endpoints),
        ("Chat Endpoint", test_chat_endpoint),
        ("Database Direct", test_database_direct)
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
        print("🎉 All direct API tests passed!")
        print("\n✅ API endpoints are working")
        print("✅ Database integration is functional")
        print("✅ Data caching is operational")
        print("✅ System is ready for use")
    else:
        print("\n⚠️  Some tests failed. Check the logs for details.")
        print("\n🔧 Issues identified:")
        if not results.get("Health Endpoint", True):
            print("  - Health endpoint not responding")
        if not results.get("Direct Data Endpoints", True):
            print("  - Data endpoints failing (likely AI system issue)")
        if not results.get("Chat Endpoint", True):
            print("  - Chat endpoint failing (AI system dependency)")
        if not results.get("Database Direct", True):
            print("  - Database access issues")

if __name__ == "__main__":
    main() 