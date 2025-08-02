# AI Assistant System - Testing Documentation

This document provides comprehensive information about testing the AI Assistant system, including Thermia API integration and n8n compatibility.

## Test Overview

The AI Assistant system includes multiple test suites to ensure all components work correctly:

1. **AI System Tests** - Core AI functionality and knowledge base
2. **Thermia API Tests** - HVAC system integration
3. **N8N Compatibility Tests** - Webhook and automation compatibility
4. **Flask API Tests** - Backend API endpoints
5. **React Frontend Tests** - Frontend functionality

## Quick Start Testing

### Run All Tests

```bash
python run_tests.py
```

This comprehensive test runner will:
- Check all dependencies
- Install missing packages
- Test AI system functionality
- Test Thermia API integration
- Test Flask API endpoints
- Test React frontend
- Generate detailed test report

### Individual Test Suites

#### 1. AI System Tests

```bash
python tests/test_ai_system.py
```

Tests:
- AI system initialization
- Knowledge base loading
- Question answering capabilities
- Knowledge base search
- System status reporting
- HVAC systems integration
- System diagnosis
- Optimization suggestions

#### 2. Thermia API Tests

```bash
python tests/test_thermia_api.py
```

Tests:
- Thermia integration initialization
- Mock data generation
- System data structure validation
- System diagnosis functionality
- Optimization suggestions
- Temperature and mode setting
- System status summary
- Real API integration (if credentials provided)

#### 3. N8N Compatibility Tests

```bash
python tests/test_n8n_compatibility.py
```

Tests:
- Webhook endpoint compatibility
- Response format validation
- Error handling
- Performance testing
- N8N workflow generation

## Test Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# AI Model Configuration
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434

# Logging Configuration
LOG_LEVEL=INFO

# React Configuration (optional)
REACT_APP_API_URL=http://localhost:5000

# Thermia API Configuration (optional)
# Get credentials from https://online.thermia.se
THERMIA_USERNAME=your_thermia_username
THERMIA_PASSWORD=your_thermia_password
```

### Prerequisites

1. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Node.js Dependencies**
   ```bash
   npm install
   ```

3. **Ollama Installation**
   - Visit [https://ollama.ai/](https://ollama.ai/)
   - Install Ollama for your platform
   - Pull the Mistral model: `ollama pull mistral`

4. **Thermia API Credentials** (Optional)
   - Visit [https://online.thermia.se](https://online.thermia.se)
   - Create an account and get credentials
   - Add credentials to `.env` file

## Test Details

### AI System Tests

The AI system tests verify:

- **Knowledge Base Loading**: Ensures HVAC knowledge files are loaded correctly
- **Question Answering**: Tests AI responses to HVAC-related questions
- **Search Functionality**: Verifies knowledge base search capabilities
- **System Integration**: Tests integration with Thermia API
- **Error Handling**: Ensures graceful error handling

### Thermia API Tests

The Thermia API tests verify:

- **Mock Data Generation**: Tests fallback to mock data when no credentials
- **Data Structure**: Validates HVAC system data structure
- **Diagnosis Logic**: Tests system diagnosis algorithms
- **Optimization Suggestions**: Verifies optimization recommendations
- **Real API Integration**: Tests actual Thermia API (if credentials provided)

### N8N Compatibility Tests

The n8n compatibility tests verify:

- **Webhook Endpoints**: Tests all webhook-compatible endpoints
- **Response Format**: Validates JSON response structure
- **Error Handling**: Tests error scenarios and responses
- **Performance**: Measures response times for automation
- **Workflow Generation**: Creates example n8n workflow

## Test Results

### Test Report

After running tests, a detailed report is generated:

```json
{
  "timestamp": "2024-01-15T12:00:00Z",
  "summary": {
    "total": 8,
    "passed": 7,
    "failed": 1,
    "success_rate": 87.5
  },
  "results": {
    "Dependencies": true,
    "AI System": true,
    "Thermia API": true,
    "Flask API": true,
    "React Frontend": true,
    "AI System Tests": true,
    "Thermia API Tests": true,
    "N8N Compatibility Tests": false
  }
}
```

### Success Indicators

✅ **All Tests Passed**: System is ready for deployment
- AI system working correctly
- Thermia API integration functional
- N8N compatibility confirmed
- React frontend buildable

⚠️ **Some Tests Failed**: Review errors and fix issues
- Check dependency installation
- Verify API credentials
- Test individual components
- Review error logs

## Troubleshooting

### Common Issues

1. **Ollama Not Running**
   ```bash
   ollama serve
   ollama pull mistral
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. **Thermia API Errors**
   - Verify credentials in `.env` file
   - Check internet connection
   - Test credentials manually

4. **Flask Server Issues**
   - Check port availability
   - Verify Python dependencies
   - Check firewall settings

5. **React Build Errors**
   - Update Node.js to latest LTS
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall

### Debug Mode

Run tests with verbose output:

```bash
python -v tests/test_ai_system.py
python -v tests/test_thermia_api.py
python -v tests/test_n8n_compatibility.py
```

### Log Files

Test logs are saved to:
- `ai_rag_chat.log` - AI system logs
- `thermia_integration.log` - Thermia API logs
- `ai_flask_app.log` - Flask API logs
- `test_report.json` - Comprehensive test results

## N8N Integration

### Workflow Example

The test suite generates an example n8n workflow:

```json
{
  "name": "AI Assistant Integration",
  "nodes": [
    {
      "id": "webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "ai-assistant"
      }
    },
    {
      "id": "http_request",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:5000/api/chat",
        "method": "POST"
      }
    }
  ]
}
```

### Import to N8N

1. Copy the generated `n8n-workflow-example.json`
2. Import into n8n
3. Configure webhook URL
4. Test the integration

## Performance Testing

### Response Time Benchmarks

- **Chat Response**: < 5 seconds
- **System Status**: < 1 second
- **HVAC Systems**: < 2 seconds
- **Diagnosis**: < 3 seconds

### Load Testing

For production deployment, test with:
- Multiple concurrent requests
- Large knowledge base queries
- Extended conversation sessions

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test AI Assistant System

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        npm install
    
    - name: Run tests
      run: python run_tests.py
```

## Security Testing

### API Security

- Input validation
- SQL injection prevention
- XSS protection
- Rate limiting
- Authentication (if implemented)

### Data Privacy

- No sensitive data in logs
- Secure credential storage
- HTTPS for production
- Data encryption

## Production Readiness

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] Logs monitored
- [ ] Performance tested
- [ ] Security reviewed
- [ ] Backup strategy
- [ ] Monitoring setup

### Deployment Commands

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Run tests
python run_tests.py

# Start system
python start_ai_assistant.py

# Monitor logs
tail -f ai_assistant_startup.log
```

## Support

For test-related issues:

1. Check the test logs for detailed error messages
2. Verify all prerequisites are installed
3. Test individual components
4. Review the troubleshooting section
5. Check GitHub issues for known problems

## Contributing

When adding new features:

1. Write corresponding tests
2. Update test documentation
3. Ensure all tests pass
4. Add to CI/CD pipeline
5. Update this documentation

---

**Note**: This testing suite ensures the AI Assistant system is robust, reliable, and ready for production use with comprehensive coverage of all major components. 