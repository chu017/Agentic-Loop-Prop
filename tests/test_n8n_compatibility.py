#!/usr/bin/env python3
"""
N8N Compatibility Test Suite
Tests webhook endpoints and response formats for n8n integration
"""

import os
import sys
import json
import requests
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class N8NCompatibilityTester:
    """Test n8n compatibility and webhook functionality"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'N8N-Compatibility-Tester/1.0'
        })
    
    def test_webhook_endpoints(self):
        """Test all webhook-compatible endpoints"""
        print("Testing N8N Webhook Endpoints...")
        print("=" * 50)
        
        endpoints = [
            {
                'url': '/api/chat',
                'method': 'POST',
                'data': {
                    'message': 'What is the status of my HVAC system?',
                    'sessionId': 'n8n-test-session-001',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'url': '/api/search',
                'method': 'POST',
                'data': {
                    'query': 'HVAC maintenance',
                    'maxResults': 3
                }
            },
            {
                'url': '/api/hvac/systems',
                'method': 'GET',
                'data': None
            },
            {
                'url': '/api/hvac/status',
                'method': 'GET',
                'data': None
            },
            {
                'url': '/api/system-status',
                'method': 'GET',
                'data': None
            },
            {
                'url': '/api/health',
                'method': 'GET',
                'data': None
            }
        ]
        
        results = {}
        
        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint['url']}"
            method = endpoint['method']
            data = endpoint['data']
            
            print(f"\nTesting {method} {endpoint['url']}...")
            
            try:
                if method == 'GET':
                    response = self.session.get(url, timeout=10)
                elif method == 'POST':
                    response = self.session.post(url, json=data, timeout=10)
                else:
                    print(f"  ✗ Unsupported method: {method}")
                    continue
                
                # Check response status
                if response.status_code == 200:
                    print(f"  ✓ Status: {response.status_code}")
                    
                    # Check JSON response
                    try:
                        json_data = response.json()
                        print(f"  ✓ Valid JSON response")
                        
                        # Validate response structure
                        validation_result = self.validate_response_structure(endpoint['url'], json_data)
                        if validation_result:
                            print(f"  ✓ Response structure valid")
                        else:
                            print(f"  ⚠ Response structure may need attention")
                        
                        results[endpoint['url']] = {
                            'status': 'success',
                            'status_code': response.status_code,
                            'response_time': response.elapsed.total_seconds(),
                            'data': json_data
                        }
                        
                    except json.JSONDecodeError:
                        print(f"  ✗ Invalid JSON response")
                        results[endpoint['url']] = {
                            'status': 'error',
                            'error': 'Invalid JSON response'
                        }
                
                else:
                    print(f"  ✗ Status: {response.status_code}")
                    results[endpoint['url']] = {
                        'status': 'error',
                        'status_code': response.status_code
                    }
                    
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Request failed: {str(e)}")
                results[endpoint['url']] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def validate_response_structure(self, endpoint, data):
        """Validate response structure for n8n compatibility"""
        if not isinstance(data, dict):
            return False
        
        # Define expected structures for each endpoint
        expected_structures = {
            '/api/chat': {
                'required': ['response', 'sessionId', 'timestamp'],
                'optional': ['error']
            },
            '/api/search': {
                'required': ['query', 'results', 'count', 'timestamp'],
                'optional': ['error']
            },
            '/api/hvac/systems': {
                'required': ['systems', 'count', 'timestamp'],
                'optional': ['error']
            },
            '/api/hvac/status': {
                'required': ['summary', 'timestamp'],
                'optional': ['error']
            },
            '/api/system-status': {
                'required': ['status', 'ai_system', 'timestamp'],
                'optional': ['error']
            },
            '/api/health': {
                'required': ['status', 'ai_system', 'timestamp'],
                'optional': ['error']
            }
        }
        
        if endpoint not in expected_structures:
            return True  # Unknown endpoint, assume valid
        
        structure = expected_structures[endpoint]
        required_fields = structure['required']
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                return False
        
        return True
    
    def test_webhook_scenarios(self):
        """Test various webhook scenarios"""
        print("\nTesting N8N Webhook Scenarios...")
        print("=" * 50)
        
        scenarios = [
            {
                'name': 'HVAC Status Query',
                'endpoint': '/api/chat',
                'data': {
                    'message': 'What is the current status of my HVAC systems?',
                    'sessionId': 'n8n-hvac-status-001',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'name': 'HVAC Diagnosis Request',
                'endpoint': '/api/chat',
                'data': {
                    'message': 'Can you diagnose my HVAC system for any issues?',
                    'sessionId': 'n8n-hvac-diagnosis-001',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'name': 'Knowledge Base Search',
                'endpoint': '/api/search',
                'data': {
                    'query': 'temperature optimization',
                    'maxResults': 5
                }
            },
            {
                'name': 'System Health Check',
                'endpoint': '/api/health',
                'data': None
            }
        ]
        
        results = {}
        
        for scenario in scenarios:
            print(f"\nTesting: {scenario['name']}")
            
            try:
                url = f"{self.base_url}{scenario['endpoint']}"
                
                if scenario['data']:
                    response = self.session.post(url, json=scenario['data'], timeout=15)
                else:
                    response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    json_data = response.json()
                    print(f"  ✓ Success - Response received")
                    print(f"  Response keys: {list(json_data.keys())}")
                    
                    # Check for AI response quality
                    if 'response' in json_data:
                        response_text = json_data['response']
                        print(f"  Response length: {len(response_text)} characters")
                        if len(response_text) > 50:
                            print(f"  ✓ Substantial response received")
                        else:
                            print(f"  ⚠ Short response - may need attention")
                    
                    results[scenario['name']] = {
                        'status': 'success',
                        'response_time': response.elapsed.total_seconds(),
                        'data_keys': list(json_data.keys())
                    }
                else:
                    print(f"  ✗ Failed - Status: {response.status_code}")
                    results[scenario['name']] = {
                        'status': 'error',
                        'status_code': response.status_code
                    }
                    
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                results[scenario['name']] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def test_error_handling(self):
        """Test error handling for n8n compatibility"""
        print("\nTesting Error Handling...")
        print("=" * 50)
        
        error_scenarios = [
            {
                'name': 'Empty Message',
                'endpoint': '/api/chat',
                'data': {
                    'message': '',
                    'sessionId': 'n8n-error-test-001'
                }
            },
            {
                'name': 'Missing Message',
                'endpoint': '/api/chat',
                'data': {
                    'sessionId': 'n8n-error-test-002'
                }
            },
            {
                'name': 'Invalid System ID',
                'endpoint': '/api/hvac/systems/invalid-id/diagnose',
                'data': None
            },
            {
                'name': 'Invalid Temperature',
                'endpoint': '/api/hvac/systems/mock-001/temperature',
                'data': {
                    'temperature': 'invalid'
                }
            }
        ]
        
        results = {}
        
        for scenario in error_scenarios:
            print(f"\nTesting: {scenario['name']}")
            
            try:
                url = f"{self.base_url}{scenario['endpoint']}"
                
                if scenario['data']:
                    response = self.session.post(url, json=scenario['data'], timeout=10)
                else:
                    response = self.session.get(url, timeout=10)
                
                # For error scenarios, we expect either 400 or 500 status codes
                if response.status_code in [400, 404, 500]:
                    print(f"  ✓ Expected error status: {response.status_code}")
                    
                    try:
                        json_data = response.json()
                        if 'error' in json_data:
                            print(f"  ✓ Error message provided: {json_data['error']}")
                        else:
                            print(f"  ⚠ No error message in response")
                        
                        results[scenario['name']] = {
                            'status': 'expected_error',
                            'status_code': response.status_code,
                            'error_message': json_data.get('error', 'No error message')
                        }
                    except json.JSONDecodeError:
                        print(f"  ⚠ Non-JSON error response")
                        results[scenario['name']] = {
                            'status': 'non_json_error',
                            'status_code': response.status_code
                        }
                else:
                    print(f"  ⚠ Unexpected status: {response.status_code}")
                    results[scenario['name']] = {
                        'status': 'unexpected_success',
                        'status_code': response.status_code
                    }
                    
            except Exception as e:
                print(f"  ✗ Request failed: {str(e)}")
                results[scenario['name']] = {
                    'status': 'request_failed',
                    'error': str(e)
                }
        
        return results
    
    def test_performance(self):
        """Test API performance for n8n integration"""
        print("\nTesting API Performance...")
        print("=" * 50)
        
        performance_tests = [
            {
                'name': 'Chat Response Time',
                'endpoint': '/api/chat',
                'data': {
                    'message': 'What is a heat pump?',
                    'sessionId': 'n8n-perf-test-001'
                }
            },
            {
                'name': 'System Status Response Time',
                'endpoint': '/api/system-status',
                'data': None
            },
            {
                'name': 'HVAC Systems Response Time',
                'endpoint': '/api/hvac/systems',
                'data': None
            }
        ]
        
        results = {}
        
        for test in performance_tests:
            print(f"\nTesting: {test['name']}")
            
            # Run multiple requests to get average response time
            response_times = []
            
            for i in range(3):  # 3 requests for average
                try:
                    url = f"{self.base_url}{test['endpoint']}"
                    
                    if test['data']:
                        response = self.session.post(url, json=test['data'], timeout=30)
                    else:
                        response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        response_time = response.elapsed.total_seconds()
                        response_times.append(response_time)
                        print(f"  Request {i+1}: {response_time:.3f}s")
                    else:
                        print(f"  Request {i+1}: Failed (Status {response.status_code})")
                        
                except Exception as e:
                    print(f"  Request {i+1}: Error - {str(e)}")
            
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                max_time = max(response_times)
                min_time = min(response_times)
                
                print(f"  Average: {avg_time:.3f}s")
                print(f"  Range: {min_time:.3f}s - {max_time:.3f}s")
                
                # Performance assessment
                if avg_time < 2.0:
                    print(f"  ✓ Good performance")
                    performance = 'good'
                elif avg_time < 5.0:
                    print(f"  ⚠ Acceptable performance")
                    performance = 'acceptable'
                else:
                    print(f"  ⚠ Slow performance")
                    performance = 'slow'
                
                results[test['name']] = {
                    'status': 'success',
                    'average_time': avg_time,
                    'max_time': max_time,
                    'min_time': min_time,
                    'performance': performance
                }
            else:
                print(f"  ✗ All requests failed")
                results[test['name']] = {
                    'status': 'failed',
                    'error': 'All requests failed'
                }
        
        return results
    
    def generate_n8n_workflow_example(self):
        """Generate example n8n workflow configuration"""
        print("\nGenerating N8N Workflow Example...")
        print("=" * 50)
        
        workflow_example = {
            "name": "AI Assistant Integration",
            "nodes": [
                {
                    "id": "webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [240, 300],
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "ai-assistant",
                        "responseMode": "responseNode",
                        "options": {}
                    }
                },
                {
                    "id": "http_request",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [460, 300],
                    "parameters": {
                        "url": "http://localhost:5000/api/chat",
                        "method": "POST",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                }
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {
                                    "name": "message",
                                    "value": "={{ $json.message }}"
                                },
                                {
                                    "name": "sessionId",
                                    "value": "={{ $json.sessionId || 'n8n-session' }}"
                                }
                            ]
                        }
                    }
                },
                {
                    "id": "respond",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "position": [680, 300],
                    "parameters": {
                        "respondWith": "json",
                        "responseBody": "={{ $json }}"
                    }
                }
            ],
            "connections": {
                "Webhook": {
                    "main": [
                        [
                            {
                                "node": "HTTP Request",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "HTTP Request": {
                    "main": [
                        [
                            {
                                "node": "Respond to Webhook",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            }
        }
        
        # Save workflow example
        workflow_file = project_root / "n8n-workflow-example.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow_example, f, indent=2)
        
        print(f"✓ N8N workflow example saved to: {workflow_file}")
        print("This workflow can be imported into n8n for testing the AI assistant integration.")
        
        return workflow_example
    
    def run_all_tests(self):
        """Run all n8n compatibility tests"""
        print("N8N Compatibility Test Suite")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        all_results = {}
        
        # Test webhook endpoints
        print("\n1. Testing Webhook Endpoints...")
        endpoint_results = self.test_webhook_endpoints()
        all_results['endpoints'] = endpoint_results
        
        # Test webhook scenarios
        print("\n2. Testing Webhook Scenarios...")
        scenario_results = self.test_webhook_scenarios()
        all_results['scenarios'] = scenario_results
        
        # Test error handling
        print("\n3. Testing Error Handling...")
        error_results = self.test_error_handling()
        all_results['errors'] = error_results
        
        # Test performance
        print("\n4. Testing Performance...")
        performance_results = self.test_performance()
        all_results['performance'] = performance_results
        
        # Generate n8n workflow example
        print("\n5. Generating N8N Workflow Example...")
        workflow_example = self.generate_n8n_workflow_example()
        all_results['workflow_example'] = workflow_example
        
        # Print summary
        self.print_summary(all_results)
        
        return all_results
    
    def print_summary(self, results):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("N8N COMPATIBILITY TEST SUMMARY")
        print("=" * 60)
        
        # Endpoint summary
        if 'endpoints' in results:
            endpoint_results = results['endpoints']
            successful_endpoints = sum(1 for r in endpoint_results.values() if r.get('status') == 'success')
            total_endpoints = len(endpoint_results)
            print(f"Webhook Endpoints: {successful_endpoints}/{total_endpoints} successful")
        
        # Scenario summary
        if 'scenarios' in results:
            scenario_results = results['scenarios']
            successful_scenarios = sum(1 for r in scenario_results.values() if r.get('status') == 'success')
            total_scenarios = len(scenario_results)
            print(f"Webhook Scenarios: {successful_scenarios}/{total_scenarios} successful")
        
        # Error handling summary
        if 'errors' in results:
            error_results = results['errors']
            expected_errors = sum(1 for r in error_results.values() if r.get('status') == 'expected_error')
            total_errors = len(error_results)
            print(f"Error Handling: {expected_errors}/{total_errors} handled correctly")
        
        # Performance summary
        if 'performance' in results:
            performance_results = results['performance']
            good_performance = sum(1 for r in performance_results.values() if r.get('performance') == 'good')
            total_performance = len(performance_results)
            print(f"Performance: {good_performance}/{total_performance} tests with good performance")
        
        print("\nN8N Integration Status:")
        if 'endpoints' in results and all(r.get('status') == 'success' for r in results['endpoints'].values()):
            print("✅ All webhook endpoints are working correctly")
        else:
            print("⚠️  Some webhook endpoints may need attention")
        
        print("\nNext Steps:")
        print("1. Import the generated n8n-workflow-example.json into n8n")
        print("2. Configure the webhook URL in n8n")
        print("3. Test the integration with real webhook calls")
        print("4. Monitor performance and adjust as needed")

def main():
    """Main function to run n8n compatibility tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test N8N compatibility for AI Assistant')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='Base URL for the AI Assistant API')
    parser.add_argument('--output', help='Output file for test results')
    
    args = parser.parse_args()
    
    tester = N8NCompatibilityTester(args.url)
    results = tester.run_all_tests()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nTest results saved to: {args.output}")

if __name__ == "__main__":
    main() 