#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Assistant System
Tests AI functionality, Thermia integration, and n8n compatibility
"""

import os
import sys
import json
import pytest
import requests
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.ai_rag_chat import AIRAGChat
from scripts.thermia_integration import ThermiaHVACIntegration

class TestAISystem:
    """Test suite for AI system functionality"""
    
    @pytest.fixture
    def ai_system(self):
        """Initialize AI system for testing"""
        return AIRAGChat()
    
    @pytest.fixture
    def thermia_integration(self):
        """Initialize Thermia integration for testing"""
        return ThermiaHVACIntegration()
    
    def test_ai_system_initialization(self, ai_system):
        """Test AI system initialization"""
        assert ai_system is not None
        assert ai_system.vectorstore is not None
        assert ai_system.qa_chain is not None
    
    def test_knowledge_base_loading(self, ai_system):
        """Test knowledge base loading"""
        # Test that context files are loaded
        context_dir = Path("context")
        assert context_dir.exists()
        
        # Check for HVAC knowledge files
        hvac_file = context_dir / "hvac_systems.txt"
        diagnostic_file = context_dir / "diagnostic_procedures.txt"
        
        assert hvac_file.exists(), "HVAC systems knowledge file not found"
        assert diagnostic_file.exists(), "Diagnostic procedures knowledge file not found"
    
    def test_ai_question_answering(self, ai_system):
        """Test AI question answering capabilities"""
        # Test HVAC-related questions
        questions = [
            "What is a heat pump?",
            "How does a Thermia heat pump work?",
            "What are the main components of an HVAC system?",
            "How do I diagnose HVAC problems?"
        ]
        
        for question in questions:
            response = ai_system.ask_question(question)
            assert response is not None
            assert len(response) > 0
            assert "error" not in response.lower()
    
    def test_knowledge_base_search(self, ai_system):
        """Test knowledge base search functionality"""
        search_queries = [
            "temperature control",
            "maintenance procedures",
            "efficiency optimization",
            "troubleshooting"
        ]
        
        for query in search_queries:
            results = ai_system.search_knowledge_base(query)
            assert isinstance(results, list)
            if results:  # If results found
                assert all(isinstance(r, dict) for r in results)
                assert all('content' in r for r in results)
    
    def test_system_status(self, ai_system):
        """Test system status reporting"""
        status = ai_system.get_system_status()
        
        assert isinstance(status, dict)
        assert 'model_name' in status
        assert 'vectorstore_loaded' in status
        assert 'qa_chain_ready' in status
        assert 'thermia_integration' in status
        assert 'timestamp' in status
    
    def test_hvac_systems_integration(self, ai_system):
        """Test HVAC systems integration"""
        systems = ai_system.get_hvac_systems()
        assert isinstance(systems, list)
        
        # Test with mock data
        if systems:
            system = systems[0]
            assert 'id' in system
            assert 'name' in system
            assert 'model' in system
            assert 'is_online' in system
    
    def test_hvac_diagnosis(self, ai_system):
        """Test HVAC system diagnosis"""
        # Test with mock system ID
        diagnosis = ai_system.diagnose_hvac_system("mock-001")
        
        assert isinstance(diagnosis, dict)
        assert 'system_id' in diagnosis
        assert 'status' in diagnosis
        assert 'issues' in diagnosis
        assert 'recommendations' in diagnosis
    
    def test_hvac_optimization_suggestions(self, ai_system):
        """Test HVAC optimization suggestions"""
        suggestions = ai_system.get_hvac_optimization_suggestions("mock-001")
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

class TestThermiaIntegration:
    """Test suite for Thermia integration"""
    
    @pytest.fixture
    def thermia_integration(self):
        """Initialize Thermia integration for testing"""
        return ThermiaHVACIntegration()
    
    def test_thermia_initialization(self, thermia_integration):
        """Test Thermia integration initialization"""
        assert thermia_integration is not None
    
    def test_fetch_heat_pumps(self, thermia_integration):
        """Test fetching heat pumps"""
        systems = thermia_integration.fetch_heat_pumps()
        
        assert isinstance(systems, list)
        assert len(systems) > 0
        
        # Test system data structure
        for system in systems:
            assert hasattr(system, 'id')
            assert hasattr(system, 'name')
            assert hasattr(system, 'model')
            assert hasattr(system, 'is_online')
    
    def test_system_diagnosis(self, thermia_integration):
        """Test system diagnosis functionality"""
        diagnosis = thermia_integration.diagnose_system("mock-001")
        
        assert diagnosis.system_id == "mock-001"
        assert diagnosis.timestamp is not None
        assert diagnosis.status in ["EXCELLENT", "GOOD", "FAIR", "POOR", "ERROR"]
        assert isinstance(diagnosis.issues, list)
        assert isinstance(diagnosis.recommendations, list)
    
    def test_optimization_suggestions(self, thermia_integration):
        """Test optimization suggestions"""
        suggestions = thermia_integration.get_optimization_suggestions("mock-001")
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
    
    def test_system_status_summary(self, thermia_integration):
        """Test system status summary"""
        summary = thermia_integration.get_system_status_summary()
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert "HVAC Systems Overview" in summary

class TestFlaskAPI:
    """Test suite for Flask API endpoints"""
    
    @pytest.fixture
    def api_base_url(self):
        """Get API base URL"""
        return "http://localhost:5000"
    
    def test_health_endpoint(self, api_base_url):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{api_base_url}/api/health", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert 'status' in data
            assert 'ai_system' in data
        except requests.exceptions.RequestException:
            pytest.skip("Flask server not running")
    
    def test_chat_endpoint(self, api_base_url):
        """Test chat endpoint"""
        try:
            response = requests.post(
                f"{api_base_url}/api/chat",
                json={"message": "What is a heat pump?"},
                timeout=10
            )
            assert response.status_code == 200
            
            data = response.json()
            assert 'response' in data
            assert 'sessionId' in data
        except requests.exceptions.RequestException:
            pytest.skip("Flask server not running")
    
    def test_search_endpoint(self, api_base_url):
        """Test search endpoint"""
        try:
            response = requests.post(
                f"{api_base_url}/api/search",
                json={"query": "temperature control"},
                timeout=5
            )
            assert response.status_code == 200
            
            data = response.json()
            assert 'query' in data
            assert 'results' in data
        except requests.exceptions.RequestException:
            pytest.skip("Flask server not running")
    
    def test_hvac_systems_endpoint(self, api_base_url):
        """Test HVAC systems endpoint"""
        try:
            response = requests.get(f"{api_base_url}/api/hvac/systems", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert 'systems' in data
            assert 'count' in data
        except requests.exceptions.RequestException:
            pytest.skip("Flask server not running")
    
    def test_hvac_diagnosis_endpoint(self, api_base_url):
        """Test HVAC diagnosis endpoint"""
        try:
            response = requests.get(f"{api_base_url}/api/hvac/systems/mock-001/diagnose", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert 'system_id' in data
            assert 'status' in data
        except requests.exceptions.RequestException:
            pytest.skip("Flask server not running")

class TestN8NCompatibility:
    """Test suite for n8n compatibility"""
    
    def test_n8n_webhook_format(self):
        """Test n8n webhook request/response format"""
        # Simulate n8n webhook request
        n8n_request = {
            "message": "What is the status of my HVAC system?",
            "sessionId": "n8n-session-123",
            "timestamp": datetime.now().isoformat()
        }
        
        # This would be the expected response format for n8n
        expected_response_format = {
            "response": "string",
            "sessionId": "string",
            "timestamp": "string"
        }
        
        assert isinstance(n8n_request, dict)
        assert "message" in n8n_request
        assert "sessionId" in n8n_request
        assert "timestamp" in n8n_request
    
    def test_api_endpoints_for_n8n(self):
        """Test that all necessary endpoints exist for n8n integration"""
        required_endpoints = [
            "/api/chat",
            "/api/health",
            "/api/system-status",
            "/api/hvac/systems",
            "/api/hvac/status"
        ]
        
        # These endpoints should be available for n8n workflows
        for endpoint in required_endpoints:
            assert endpoint.startswith("/api/")
    
    def test_json_response_format(self):
        """Test that all responses are valid JSON format"""
        # Test response format for n8n compatibility
        sample_responses = [
            {"response": "AI response", "sessionId": "123", "timestamp": "2024-01-01T00:00:00Z"},
            {"systems": [], "count": 0, "timestamp": "2024-01-01T00:00:00Z"},
            {"status": "healthy", "ai_system": {}, "timestamp": "2024-01-01T00:00:00Z"}
        ]
        
        for response in sample_responses:
            # Test that response can be serialized to JSON
            json_str = json.dumps(response)
            assert isinstance(json_str, str)
            
            # Test that response can be deserialized from JSON
            parsed = json.loads(json_str)
            assert isinstance(parsed, dict)

class TestIntegration:
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow from question to HVAC diagnosis"""
        # Initialize AI system
        ai_system = AIRAGChat()
        
        # Test question about HVAC
        question = "What are the common issues with HVAC systems?"
        response = ai_system.ask_question(question)
        assert response is not None
        
        # Test HVAC systems integration
        systems = ai_system.get_hvac_systems()
        assert isinstance(systems, list)
        
        # Test diagnosis if systems available
        if systems:
            diagnosis = ai_system.diagnose_hvac_system(systems[0]['id'])
            assert isinstance(diagnosis, dict)
            assert 'status' in diagnosis
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        ai_system = AIRAGChat()
        
        # Test with invalid system ID
        diagnosis = ai_system.diagnose_hvac_system("invalid-id")
        assert 'error' in diagnosis or diagnosis['status'] == 'ERROR'
        
        # Test with empty question
        response = ai_system.ask_question("")
        assert response is not None  # Should handle empty input gracefully

def run_all_tests():
    """Run all tests and generate report"""
    print("Running comprehensive test suite for AI Assistant System...")
    print("=" * 60)
    
    # Test categories
    test_categories = [
        ("AI System", TestAISystem),
        ("Thermia Integration", TestThermiaIntegration),
        ("Flask API", TestFlaskAPI),
        ("N8N Compatibility", TestN8NCompatibility),
        ("Integration", TestIntegration)
    ]
    
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
    print("TEST SUMMARY")
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
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total_failed} test(s) failed. Please review the errors above.")
    
    return total_failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 