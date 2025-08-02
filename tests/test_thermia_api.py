#!/usr/bin/env python3
"""
Thermia API Integration Test Suite
Tests the integration with python-thermia-online-api package
"""

import os
import sys
import json
import pytest
import requests
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.thermia_integration import ThermiaHVACIntegration, HVACSystemData, DiagnosticResult

class TestThermiaAPI:
    """Test suite for Thermia API integration"""
    
    @pytest.fixture
    def thermia_integration(self):
        """Initialize Thermia integration for testing"""
        return ThermiaHVACIntegration()
    
    def test_thermia_initialization(self, thermia_integration):
        """Test Thermia integration initialization"""
        assert thermia_integration is not None
        assert hasattr(thermia_integration, 'username')
        assert hasattr(thermia_integration, 'password')
        assert hasattr(thermia_integration, 'thermia')
    
    def test_mock_data_generation(self, thermia_integration):
        """Test mock data generation when no credentials provided"""
        systems = thermia_integration.fetch_heat_pumps()
        
        assert isinstance(systems, list)
        assert len(systems) > 0
        
        # Test mock system structure
        mock_system = systems[0]
        assert isinstance(mock_system, HVACSystemData)
        assert mock_system.id == "mock-001"
        assert mock_system.name == "Test Heat Pump 1"
        assert mock_system.model == "Thermia Diplomat Duo"
        assert isinstance(mock_system.is_online, bool)
    
    def test_system_data_structure(self, thermia_integration):
        """Test HVAC system data structure"""
        systems = thermia_integration.fetch_heat_pumps()
        
        for system in systems:
            # Required fields
            assert hasattr(system, 'id')
            assert hasattr(system, 'name')
            assert hasattr(system, 'model')
            assert hasattr(system, 'is_online')
            assert hasattr(system, 'indoor_temperature')
            assert hasattr(system, 'outdoor_temperature')
            assert hasattr(system, 'hot_water_temperature')
            assert hasattr(system, 'heat_temperature')
            assert hasattr(system, 'operation_mode')
            assert hasattr(system, 'active_alarms')
            assert hasattr(system, 'compressor_operational_time')
            assert hasattr(system, 'last_online')
            
            # Type checks
            assert isinstance(system.id, str)
            assert isinstance(system.name, str)
            assert isinstance(system.model, str)
            assert isinstance(system.is_online, bool)
            assert isinstance(system.active_alarms, list)
            assert isinstance(system.operation_mode, str)
    
    def test_system_diagnosis(self, thermia_integration):
        """Test system diagnosis functionality"""
        # Test with valid system ID
        diagnosis = thermia_integration.diagnose_system("mock-001")
        
        assert isinstance(diagnosis, DiagnosticResult)
        assert diagnosis.system_id == "mock-001"
        assert diagnosis.timestamp is not None
        assert diagnosis.status in ["EXCELLENT", "GOOD", "FAIR", "POOR", "ERROR"]
        assert isinstance(diagnosis.issues, list)
        assert isinstance(diagnosis.recommendations, list)
        assert diagnosis.efficiency_score is not None
        
        # Test with invalid system ID
        invalid_diagnosis = thermia_integration.diagnose_system("invalid-id")
        assert invalid_diagnosis.status == "ERROR"
        assert "System not found" in invalid_diagnosis.issues
    
    def test_optimization_suggestions(self, thermia_integration):
        """Test optimization suggestions"""
        suggestions = thermia_integration.get_optimization_suggestions("mock-001")
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # Check for common optimization suggestions
        suggestion_text = " ".join(suggestions).lower()
        assert any(keyword in suggestion_text for keyword in [
            "temperature", "efficiency", "maintenance", "insulation"
        ])
    
    def test_temperature_setting(self, thermia_integration):
        """Test temperature setting functionality"""
        # Test with valid temperature
        success = thermia_integration.set_temperature("mock-001", 22.5)
        assert success is True
        
        # Test with invalid system ID
        success = thermia_integration.set_temperature("invalid-id", 22.5)
        assert success is False
    
    def test_operation_mode_setting(self, thermia_integration):
        """Test operation mode setting functionality"""
        # Test with valid mode
        success = thermia_integration.set_operation_mode("mock-001", "Heating")
        assert success is True
        
        # Test with invalid system ID
        success = thermia_integration.set_operation_mode("invalid-id", "Heating")
        assert success is False
    
    def test_system_status_summary(self, thermia_integration):
        """Test system status summary"""
        summary = thermia_integration.get_system_status_summary()
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert "HVAC Systems Overview" in summary
        assert "Total systems" in summary
        assert "Online systems" in summary
        assert "Offline systems" in summary
    
    def test_system_by_id(self, thermia_integration):
        """Test getting system by ID"""
        # Test with valid ID
        system = thermia_integration.get_system_by_id("mock-001")
        assert system is not None
        assert system.id == "mock-001"
        assert system.name == "Test Heat Pump 1"
        
        # Test with invalid ID
        invalid_system = thermia_integration.get_system_by_id("invalid-id")
        assert invalid_system is None

class TestThermiaAPIIntegration:
    """Test integration with actual Thermia API (if credentials provided)"""
    
    @pytest.fixture
    def thermia_integration_with_creds(self):
        """Initialize Thermia integration with credentials if available"""
        username = os.getenv('THERMIA_USERNAME')
        password = os.getenv('THERMIA_PASSWORD')
        
        if username and password:
            return ThermiaHVACIntegration(username, password)
        else:
            pytest.skip("Thermia credentials not provided")
    
    def test_real_thermia_connection(self, thermia_integration_with_creds):
        """Test connection to real Thermia API"""
        # This test will only run if credentials are provided
        assert thermia_integration_with_creds.thermia is not None
        
        # Test fetching real systems
        systems = thermia_integration_with_creds.fetch_heat_pumps()
        assert isinstance(systems, list)
        
        # Test with real system if available
        if systems:
            real_system = systems[0]
            assert isinstance(real_system, HVACSystemData)
            
            # Test diagnosis with real system
            diagnosis = thermia_integration_with_creds.diagnose_system(real_system.id)
            assert isinstance(diagnosis, DiagnosticResult)
    
    def test_real_thermia_operations(self, thermia_integration_with_creds):
        """Test operations with real Thermia systems"""
        systems = thermia_integration_with_creds.fetch_heat_pumps()
        
        if systems:
            real_system = systems[0]
            
            # Test temperature setting (read-only test)
            original_temp = real_system.heat_temperature
            success = thermia_integration_with_creds.set_temperature(real_system.id, original_temp)
            # Note: This might fail if the system doesn't support temperature setting
            # or if we don't have write permissions
            
            # Test operation mode setting (read-only test)
            original_mode = real_system.operation_mode
            success = thermia_integration_with_creds.set_operation_mode(real_system.id, original_mode)
            # Note: This might fail if the system doesn't support mode setting
            # or if we don't have write permissions

class TestThermiaAPIMockData:
    """Test mock data functionality"""
    
    def test_mock_data_consistency(self):
        """Test that mock data is consistent and realistic"""
        integration = ThermiaHVACIntegration()
        systems = integration.fetch_heat_pumps()
        
        # Test first mock system
        system1 = systems[0]
        assert system1.id == "mock-001"
        assert system1.name == "Test Heat Pump 1"
        assert system1.model == "Thermia Diplomat Duo"
        assert system1.is_online is True
        assert system1.indoor_temperature == 22.5
        assert system1.outdoor_temperature == 5.2
        assert system1.hot_water_temperature == 45.0
        assert system1.heat_temperature == 21.0
        assert system1.operation_mode == "Heating"
        assert system1.active_alarms == []
        assert system1.compressor_operational_time == 1250.5
        
        # Test second mock system
        system2 = systems[1]
        assert system2.id == "mock-002"
        assert system2.name == "Test Heat Pump 2"
        assert system2.model == "Thermia Calibra"
        assert system2.is_online is False
        assert system2.indoor_temperature is None
        assert system2.outdoor_temperature is None
        assert system2.hot_water_temperature is None
        assert system2.heat_temperature == 20.0
        assert system2.operation_mode == "Standby"
        assert system2.active_alarms == ["Communication Error"]
        assert system2.compressor_operational_time == 890.2
    
    def test_mock_diagnosis_logic(self):
        """Test that mock diagnosis logic produces realistic results"""
        integration = ThermiaHVACIntegration()
        
        # Test diagnosis for online system
        diagnosis1 = integration.diagnose_system("mock-001")
        assert diagnosis1.status in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
        assert diagnosis1.efficiency_score is not None
        assert diagnosis1.efficiency_score > 0
        
        # Test diagnosis for offline system
        diagnosis2 = integration.diagnose_system("mock-002")
        assert diagnosis2.status in ["POOR", "ERROR"]
        assert "System is offline" in diagnosis2.issues
    
    def test_mock_optimization_suggestions(self):
        """Test that mock optimization suggestions are realistic"""
        integration = ThermiaHVACIntegration()
        suggestions = integration.get_optimization_suggestions("mock-001")
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # Check for realistic suggestions
        suggestion_text = " ".join(suggestions).lower()
        assert any(keyword in suggestion_text for keyword in [
            "temperature", "efficiency", "maintenance", "insulation", "filter"
        ])

def run_thermia_tests():
    """Run all Thermia API tests"""
    print("Running Thermia API Integration Tests...")
    print("=" * 60)
    
    # Test categories
    test_categories = [
        ("Basic Integration", TestThermiaAPI),
        ("Mock Data", TestThermiaAPIMockData)
    ]
    
    # Check if credentials are available for real API tests
    if os.getenv('THERMIA_USERNAME') and os.getenv('THERMIA_PASSWORD'):
        test_categories.append(("Real API Integration", TestThermiaAPIIntegration))
        print("✓ Thermia credentials found - will test real API integration")
    else:
        print("⚠ No Thermia credentials found - skipping real API tests")
        print("Set THERMIA_USERNAME and THERMIA_PASSWORD environment variables to test real API")
    
    results = {}
    
    for category_name, test_class in test_categories:
        print(f"\nTesting {category_name}...")
        try:
            # Run tests for this category
            test_instance = test_class()
            
            # Get all test methods
            test_methods = [method for method in dir(test_class) if method.startswith('test_')]
            
            passed = 0
            failed = 0
            
            for method_name in test_methods:
                try:
                    method = getattr(test_class, method_name)
                    if hasattr(method, '__self__'):  # Instance method
                        method(test_instance)
                    else:  # Class method
                        method()
                    passed += 1
                    print(f"  ✓ {method_name}")
                except Exception as e:
                    failed += 1
                    print(f"  ✗ {method_name}: {str(e)}")
            
            results[category_name] = {"passed": passed, "failed": failed}
            
        except Exception as e:
            print(f"  ✗ Error testing {category_name}: {str(e)}")
            results[category_name] = {"passed": 0, "failed": 1}
    
    # Print summary
    print("\n" + "=" * 60)
    print("THERMIA API TEST SUMMARY")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    for category, result in results.items():
        passed = result["passed"]
        failed = result["failed"]
        total_passed += passed
        total_failed += failed
        
        print(f"{category}: {passed} passed, {failed} failed")
    
    print(f"\nTOTAL: {total_passed} passed, {total_failed} failed")
    
    if total_failed == 0:
        print("\n🎉 All Thermia API tests passed!")
        print("\nThermia Integration Status:")
        print("✅ Mock data generation working")
        print("✅ System diagnosis functionality working")
        print("✅ Optimization suggestions working")
        print("✅ Temperature and mode setting working")
        
        if os.getenv('THERMIA_USERNAME') and os.getenv('THERMIA_PASSWORD'):
            print("✅ Real API integration tested")
        else:
            print("⚠ Real API integration not tested (no credentials)")
    else:
        print(f"\n⚠️  {total_failed} test(s) failed. Please review the errors above.")
    
    return total_failed == 0

if __name__ == "__main__":
    success = run_thermia_tests()
    sys.exit(0 if success else 1) 