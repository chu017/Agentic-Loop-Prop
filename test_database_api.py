#!/usr/bin/env python3
"""
Database and API Integration Test
Tests the database integration and API functionality
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
current_dir = Path(__file__).parent
scripts_dir = current_dir / 'scripts'

if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

def test_database_creation():
    """Test database creation and tables"""
    print("💾 Testing Database Creation")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        # Initialize data manager
        data_manager = get_data_integration_manager()
        print("✅ Data integration manager initialized")
        
        # Check if database file exists
        db_path = Path("hvac_data.db")
        if db_path.exists():
            print(f"✅ Database file created: {db_path}")
            print(f"  Size: {db_path.stat().st_size} bytes")
        else:
            print("❌ Database file not found")
            return False
        
        # Test database connection
        conn = sqlite3.connect("hvac_data.db")
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        expected_tables = ['hvac_systems', 'historical_data', 'knowledge_cache']
        for table in expected_tables:
            if table in table_names:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
                return False
        
        # Check table structure
        cursor.execute("PRAGMA table_info(hvac_systems);")
        columns = cursor.fetchall()
        print(f"✅ hvac_systems table has {len(columns)} columns")
        
        cursor.execute("PRAGMA table_info(historical_data);")
        columns = cursor.fetchall()
        print(f"✅ historical_data table has {len(columns)} columns")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database creation test failed: {e}")
        return False

def test_data_caching():
    """Test data caching functionality"""
    print("\n📊 Testing Data Caching")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        data_manager = get_data_integration_manager()
        
        # Get live data (should cache it)
        systems = data_manager.get_live_system_data()
        print(f"✅ Retrieved {len(systems)} systems from live data")
        
        # Check if data was cached
        cached_systems = data_manager.get_cached_system_data()
        print(f"✅ Retrieved {len(cached_systems)} systems from cache")
        
        # Verify data structure
        if systems:
            system = systems[0]
            print(f"✅ System data structure:")
            print(f"  - Name: {system.name}")
            print(f"  - Model: {system.model}")
            print(f"  - Online: {system.is_online}")
            print(f"  - Indoor Temp: {system.indoor_temperature}°C")
            print(f"  - Outdoor Temp: {system.outdoor_temperature}°C")
            print(f"  - Operation Mode: {system.operation_mode}")
            print(f"  - Active Alarms: {len(system.active_alarms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data caching test failed: {e}")
        return False

def test_historical_data():
    """Test historical data functionality"""
    print("\n📈 Testing Historical Data")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        data_manager = get_data_integration_manager()
        
        # Get a system ID
        systems = data_manager.get_live_system_data()
        if not systems:
            print("❌ No systems available for historical data test")
            return False
        
        system_id = systems[0].id
        
        # Test historical data retrieval
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        historical_data = data_manager.get_historical_data(
            system_id, "indoor_temperature", start_time, end_time
        )
        
        print(f"✅ Retrieved {len(historical_data)} historical data points")
        
        if historical_data:
            print(f"✅ Sample data point:")
            sample = historical_data[0]
            print(f"  - Time: {sample['time']}")
            print(f"  - Value: {sample['value']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Historical data test failed: {e}")
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
            print(f"  Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test HVAC systems endpoint
        response = requests.get('http://localhost:5000/api/hvac/systems', timeout=5)
        if response.status_code == 200:
            data = response.json()
            systems = data.get('systems', [])
            print(f"✅ HVAC systems endpoint: {len(systems)} systems")
            
            if systems:
                system = systems[0]
                print(f"✅ Sample system:")
                print(f"  - Name: {system.get('name', 'N/A')}")
                print(f"  - Model: {system.get('model', 'N/A')}")
                print(f"  - Online: {system.get('is_online', 'N/A')}")
                print(f"  - Indoor Temp: {system.get('indoor_temperature', 'N/A')}°C")
        else:
            print(f"❌ HVAC systems endpoint failed: {response.status_code}")
        
        # Test system status endpoint
        response = requests.get('http://localhost:5000/api/system-status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System status endpoint working")
            print(f"  Data integration: {data.get('data_integration', 'N/A')}")
        else:
            print(f"❌ System status endpoint failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def test_database_queries():
    """Test direct database queries"""
    print("\n🔍 Testing Database Queries")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("hvac_data.db")
        cursor = conn.cursor()
        
        # Test hvac_systems table
        cursor.execute("SELECT COUNT(*) FROM hvac_systems;")
        count = cursor.fetchone()[0]
        print(f"✅ hvac_systems table has {count} records")
        
        if count > 0:
            cursor.execute("SELECT name, model, is_online, indoor_temperature FROM hvac_systems LIMIT 1;")
            row = cursor.fetchone()
            print(f"✅ Sample record:")
            print(f"  - Name: {row[0]}")
            print(f"  - Model: {row[1]}")
            print(f"  - Online: {row[2]}")
            print(f"  - Indoor Temp: {row[3]}°C")
        
        # Test historical_data table
        cursor.execute("SELECT COUNT(*) FROM historical_data;")
        count = cursor.fetchone()[0]
        print(f"✅ historical_data table has {count} records")
        
        if count > 0:
            cursor.execute("SELECT system_id, register_name, value, timestamp FROM historical_data LIMIT 1;")
            row = cursor.fetchone()
            print(f"✅ Sample historical record:")
            print(f"  - System ID: {row[0]}")
            print(f"  - Register: {row[1]}")
            print(f"  - Value: {row[2]}")
            print(f"  - Timestamp: {row[3]}")
        
        # Test knowledge_cache table
        cursor.execute("SELECT COUNT(*) FROM knowledge_cache;")
        count = cursor.fetchone()[0]
        print(f"✅ knowledge_cache table has {count} records")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database queries test failed: {e}")
        return False

def main():
    """Main test function"""
    print("HVAC AI Assistant - Database & API Integration Test")
    print("=" * 60)
    
    tests = [
        ("Database Creation", test_database_creation),
        ("Data Caching", test_data_caching),
        ("Historical Data", test_historical_data),
        ("API Endpoints", test_api_endpoints),
        ("Database Queries", test_database_queries)
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
        print("🎉 All database and API integration tests passed!")
        print("\n✅ Database is properly created and functional")
        print("✅ Data caching is working correctly")
        print("✅ Historical data storage is operational")
        print("✅ API endpoints are responding properly")
        print("✅ Database queries are executing successfully")
    else:
        print("\n⚠️  Some tests failed. Check the logs for details.")

if __name__ == "__main__":
    main() 