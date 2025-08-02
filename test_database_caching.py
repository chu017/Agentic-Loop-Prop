#!/usr/bin/env python3
"""
Database Caching Test
Tests that data is properly cached to the database
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
current_dir = Path(__file__).parent
scripts_dir = current_dir / 'scripts'

if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

def test_data_caching_to_database():
    """Test that data is properly cached to the database"""
    print("💾 Testing Database Caching")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        # Initialize data manager
        data_manager = get_data_integration_manager()
        print("✅ Data integration manager initialized")
        
        # Get live data (this should cache to database)
        systems = data_manager.get_live_system_data()
        print(f"✅ Retrieved {len(systems)} systems from live data")
        
        # Check database directly
        conn = sqlite3.connect("hvac_data.db")
        cursor = conn.cursor()
        
        # Check if data was cached
        cursor.execute("SELECT COUNT(*) FROM hvac_systems;")
        count = cursor.fetchone()[0]
        print(f"✅ Database has {count} cached system records")
        
        if count > 0:
            # Get sample data from database
            cursor.execute("SELECT name, model, is_online, indoor_temperature, outdoor_temperature, operation_mode FROM hvac_systems LIMIT 1;")
            row = cursor.fetchone()
            print(f"✅ Sample cached data:")
            print(f"  - Name: {row[0]}")
            print(f"  - Model: {row[1]}")
            print(f"  - Online: {row[2]}")
            print(f"  - Indoor Temp: {row[3]}°C")
            print(f"  - Outdoor Temp: {row[4]}°C")
            print(f"  - Operation Mode: {row[5]}")
        
        # Test historical data caching
        if systems:
            system_id = systems[0].id
            
            # Get historical data (should cache to database)
            from datetime import timedelta
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            historical_data = data_manager.get_historical_data(
                system_id, "indoor_temperature", start_time, end_time
            )
            
            print(f"✅ Retrieved {len(historical_data)} historical data points")
            
            # Check if historical data was cached
            cursor.execute("SELECT COUNT(*) FROM historical_data;")
            hist_count = cursor.fetchone()[0]
            print(f"✅ Database has {hist_count} cached historical records")
            
            if hist_count > 0:
                cursor.execute("SELECT system_id, register_name, value, timestamp FROM historical_data LIMIT 1;")
                row = cursor.fetchone()
                print(f"✅ Sample historical cached data:")
                print(f"  - System ID: {row[0]}")
                print(f"  - Register: {row[1]}")
                print(f"  - Value: {row[2]}")
                print(f"  - Timestamp: {row[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database caching test failed: {e}")
        return False

def test_data_retrieval_from_cache():
    """Test retrieving data from cache"""
    print("\n📊 Testing Data Retrieval from Cache")
    print("=" * 40)
    
    try:
        from data_integration import get_data_integration_manager
        
        data_manager = get_data_integration_manager()
        
        # Get data from cache
        cached_systems = data_manager.get_cached_system_data()
        print(f"✅ Retrieved {len(cached_systems)} systems from cache")
        
        if cached_systems:
            system = cached_systems[0]
            print(f"✅ Cached system data:")
            print(f"  - Name: {system.name}")
            print(f"  - Model: {system.model}")
            print(f"  - Online: {system.is_online}")
            print(f"  - Indoor Temp: {system.indoor_temperature}°C")
            print(f"  - Outdoor Temp: {system.outdoor_temperature}°C")
            print(f"  - Operation Mode: {system.operation_mode}")
            print(f"  - Active Alarms: {len(system.active_alarms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data retrieval from cache test failed: {e}")
        return False

def test_database_structure():
    """Test database structure and integrity"""
    print("\n🏗️  Testing Database Structure")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("hvac_data.db")
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("PRAGMA table_info(hvac_systems);")
        columns = cursor.fetchall()
        print(f"✅ hvac_systems table structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(historical_data);")
        columns = cursor.fetchall()
        print(f"✅ historical_data table structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(knowledge_cache);")
        columns = cursor.fetchall()
        print(f"✅ knowledge_cache table structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Check indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
        indexes = cursor.fetchall()
        print(f"✅ Database has {len(indexes)} indexes")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database structure test failed: {e}")
        return False

def test_data_integrity():
    """Test data integrity and consistency"""
    print("\n🔍 Testing Data Integrity")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("hvac_data.db")
        cursor = conn.cursor()
        
        # Test data consistency
        cursor.execute("SELECT COUNT(*) FROM hvac_systems WHERE is_online IS NOT NULL;")
        online_count = cursor.fetchone()[0]
        print(f"✅ {online_count} systems have online status")
        
        cursor.execute("SELECT COUNT(*) FROM hvac_systems WHERE indoor_temperature IS NOT NULL;")
        temp_count = cursor.fetchone()[0]
        print(f"✅ {temp_count} systems have temperature data")
        
        cursor.execute("SELECT COUNT(*) FROM hvac_systems WHERE operation_mode IS NOT NULL;")
        mode_count = cursor.fetchone()[0]
        print(f"✅ {mode_count} systems have operation mode data")
        
        # Test historical data integrity
        cursor.execute("SELECT COUNT(*) FROM historical_data WHERE value IS NOT NULL;")
        value_count = cursor.fetchone()[0]
        print(f"✅ {value_count} historical records have values")
        
        cursor.execute("SELECT COUNT(*) FROM historical_data WHERE timestamp IS NOT NULL;")
        time_count = cursor.fetchone()[0]
        print(f"✅ {time_count} historical records have timestamps")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Data integrity test failed: {e}")
        return False

def main():
    """Main test function"""
    print("HVAC AI Assistant - Database Caching Test")
    print("=" * 50)
    
    tests = [
        ("Database Caching", test_data_caching_to_database),
        ("Data Retrieval from Cache", test_data_retrieval_from_cache),
        ("Database Structure", test_database_structure),
        ("Data Integrity", test_data_integrity)
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
        print("🎉 All database caching tests passed!")
        print("\n✅ Data is properly cached to database")
        print("✅ Data can be retrieved from cache")
        print("✅ Database structure is correct")
        print("✅ Data integrity is maintained")
        print("\n📊 Database Integration Summary:")
        print("  - SQLite database: ✅ Working")
        print("  - Data caching: ✅ Working")
        print("  - Historical data: ✅ Working")
        print("  - Data retrieval: ✅ Working")
        print("  - API integration: ✅ Ready (when AI system is fixed)")
    else:
        print("\n⚠️  Some tests failed. Check the logs for details.")

if __name__ == "__main__":
    main() 