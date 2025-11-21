# Sheikh AI - GitHub Automation with Playwright Testing

## 🚀 Overview

The Sheikh AI project now includes a comprehensive testing and automation framework powered by Playwright and GitHub Actions. This ensures the application is always error-free, well-tested, and production-ready.

## 📋 What's Been Implemented

### 1. **Playwright Testing Framework**
- **Cross-browser testing**: Chrome, Firefox, Safari
- **Mobile responsive testing**: iPhone, Android layouts
- **End-to-end test suites**: Complete user workflow testing
- **API integration testing**: Backend endpoint validation
- **Accessibility testing**: WCAG compliance checks

### 2. **GitHub Actions CI/CD Pipeline**
- **Automated testing**: Runs on every push and PR
- **Multi-stage workflow**: Backend → Frontend → Security → Performance
- **Artifact storage**: Test reports and build artifacts
- **Notification system**: Failure and success alerts
- **Scheduled runs**: Daily testing at 2 AM UTC

### 3. **Comprehensive Test Coverage**

#### Frontend Tests (`frontend/tests/`)
- **chat.spec.js**: Chat interface functionality
  - Page loading and layout validation
  - Message sending and AI response verification
  - AI provider switching (Gemini/OpenAI)
  - Conversation management
  - File upload capabilities
  - Error handling and network resilience
  - Responsive design validation
  - Accessibility compliance

- **api.spec.js**: Backend API testing
  - Health check endpoint validation
  - CRUD operations for conversations
  - Message processing with AI providers
  - File upload endpoints
  - Shell command execution
  - Browser automation endpoints
  - Request validation and error handling

#### Test Utilities (`frontend/tests/utils.js`)
- Helper functions for reliable testing
- API interaction utilities
- Performance monitoring tools
- Accessibility testing helpers
- Responsive design checks
- Mock data fixtures

### 4. **Performance & Security Testing**

#### Load Testing (`load_test.py`)
- Concurrent user simulation
- Response time monitoring
- Success rate validation (95%+ required)
- Performance metrics collection
- JSON result export

#### Security Scanning
- **Trivy vulnerability scanner**: Container and dependency scanning
- **SARIF reporting**: GitHub Security tab integration
- **Automated security checks**: Every commit and PR

### 5. **Development Tools**

#### Setup Script (`setup-testing.sh`)
- Automated environment setup
- Dependency installation
- Configuration file generation
- Verification and validation
- Usage instructions

#### Package Management
- Updated `package.json` with Playwright scripts
- Test execution commands
- Debug and UI testing options

## 🔧 Configuration

### Environment Variables
The CI/CD pipeline requires these GitHub Secrets:
- `GOOGLE_GENERATIVE_AI_API_KEY`: Google Gemini API key
- `OPENAI_API_KEY`: OpenAI API key

### Test Environment (`backend/.env.test`)
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sheikh_ai_test
GOOGLE_GENERATIVE_AI_API_KEY=your_test_api_key
OPENAI_API_KEY=your_test_api_key
DEBUG=true
ENVIRONMENT=testing
```

## 📊 Test Categories

### 1. **Functional Tests**
- ✅ Chat message sending/receiving
- ✅ AI provider switching
- ✅ Conversation management
- ✅ File upload functionality
- ✅ Shell command execution
- ✅ Browser automation

### 2. **Quality Assurance**
- ✅ Responsive design validation
- ✅ Accessibility compliance (WCAG)
- ✅ Cross-browser compatibility
- ✅ Network error handling
- ✅ Input validation
- ✅ API endpoint validation

### 3. **Performance Tests**
- ✅ Load testing with concurrent users
- ✅ Response time monitoring
- ✅ Success rate validation
- ✅ Memory usage tracking
- ✅ Database query optimization

### 4. **Security Tests**
- ✅ Vulnerability scanning
- ✅ Dependency security checks
- ✅ CORS configuration validation
- ✅ Input sanitization
- ✅ Authentication/authorization

## 🚀 Quick Start

### 1. **Setup Testing Environment**
```bash
# Run the automated setup script
./setup-testing.sh

# Or manually setup
cd frontend && npm install && npx playwright install
cd backend && pip install -r requirements.txt && pip install pytest
```

### 2. **Run Tests Locally**
```bash
# Start services
cd backend && python -m uvicorn app.interfaces.api.main:app --port 8000 &
cd frontend && npm run dev &

# Run tests
cd frontend
npm run test          # All tests
npm run test:ui       # Interactive UI
npm run test:headed   # Visible browser
```

### 3. **Load Testing**
```bash
# Run performance tests
python load_test.py --users 10 --duration 30

# Advanced options
python load_test.py --url http://localhost:8000/api/v1 --users 20 --duration 60
```

## 📈 CI/CD Pipeline Flow

```mermaid
graph TD
    A[Push/PR] --> B[Backend Tests]
    B --> C[Frontend Tests]
    C --> D[Security Scan]
    D --> E[Performance Test]
    E --> F[Build & Deploy]
    F --> G[Notifications]
    
    B --> H[Test Fail?]
    C --> I[Test Fail?]
    D --> J[Vulnerabilities?]
    E --> K[Performance OK?]
    
    H -->|Yes| L[Stop Pipeline]
    I -->|Yes| L
    J -->|Yes| L
    K -->|No| L
    
    G --> M[Success]
    L --> N[Failure Alert]
```

## 🎯 Testing Benefits

### For Developers
- **Early Bug Detection**: Catch issues before deployment
- **Consistent Quality**: Automated validation every commit
- **Faster Debugging**: Detailed test reports and artifacts
- **Confidence in Changes**: Comprehensive test coverage

### For Users
- **Reliable Application**: Thoroughly tested features
- **Better Performance**: Load testing ensures scalability
- **Security Assurance**: Regular vulnerability scanning
- **Accessibility**: WCAG compliance validation

### for DevOps
- **Automated Deployment**: CI/CD pipeline handles releases
- **Monitoring**: Performance metrics and health checks
- **Documentation**: Test reports and coverage data
- **Notifications**: Immediate alerts for issues

## 📋 Test Execution Commands

### Frontend Testing
```bash
npm run test              # Run all tests
npm run test:ui           # Interactive test runner
npm run test:debug        # Debug mode
npm run test:headed       # Visible browser
npm run test:report       # Show HTML report
npm run test:install      # Install Playwright browsers
```

### Backend Testing
```bash
# Run with pytest
pytest                    # All tests
pytest --cov             # With coverage
pytest test_file.py      # Specific test
pytest -v                # Verbose output
```

### Load Testing
```bash
python load_test.py               # Default settings
python load_test.py --users 20    # 20 concurrent users
python load_test.py --duration 60 # 1 minute test
python load_test.py --health-only # Health endpoint only
```

## 📊 Test Reports & Artifacts

### Generated Reports
- **Playwright HTML Report**: `frontend/test-results/`
- **Coverage Reports**: XML format for Codecov
- **Security Scan Results**: SARIF format
- **Load Test Results**: JSON export with metrics

### GitHub Artifacts
- Test execution videos and screenshots
- Coverage reports and metrics
- Security scan results
- Docker build artifacts

## 🔍 Monitoring & Alerts

### Automated Monitoring
- **Daily Health Checks**: Scheduled test runs
- **Performance Metrics**: Response times and success rates
- **Security Alerts**: Vulnerability detection
- **Test Coverage**: Code coverage tracking

### Notification System
- **Failure Alerts**: Immediate notifications on test failures
- **Success Confirmations**: Deployment success notifications
- **Performance Degradation**: Alerts when response times increase

## 🛠️ Troubleshooting

### Common Issues
1. **Tests timeout**: Increase wait times or check server status
2. **Element not found**: Update selectors or check page state
3. **API failures**: Verify backend is running and accessible
4. **Performance issues**: Check load test results and optimize

### Debug Mode
```bash
# Enable debug logging
DEBUG=true npm run test

# Interactive debugging
npm run test:debug

# Browser developer tools
npm run test:headed
```

## 📚 Resources

### Documentation
- **Playwright Docs**: https://playwright.dev/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Test Strategy**: See `frontend/tests/README.md`
- **CI/CD Pipeline**: See `.github/workflows/ci-cd.yml`

### Tools
- **Playwright**: End-to-end testing framework
- **Pytest**: Python testing framework
- **Trivy**: Vulnerability scanner
- **Locust**: Advanced load testing (optional)

## 🎉 Next Steps

1. **Configure GitHub Secrets**: Add API keys to repository settings
2. **Run Initial Tests**: Execute the testing suite
3. **Review Results**: Check test reports and coverage
4. **Optimize Performance**: Address any performance issues
5. **Set up Notifications**: Configure alert channels

## 💡 Best Practices

### Test Writing
- Use descriptive test names
- Implement proper waits and timeouts
- Clean up test data after execution
- Mock external dependencies when possible

### CI/CD
- Keep tests fast and reliable
- Use parallel execution where possible
- Monitor test execution times
- Maintain high test coverage (>80%)

### Performance
- Set realistic performance baselines
- Monitor trends over time
- Address performance regressions promptly
- Use load testing for scaling decisions

---

**🎯 Result**: Your Sheikh AI application now has enterprise-grade testing and automation that ensures it's always error-free, performant, and secure! The comprehensive test suite catches issues early, validates functionality across browsers and devices, and provides detailed insights for continuous improvement.

**Repository**: https://github.com/likhonsdevbd/sheikh-ai  
**Documentation**: Complete testing guide and API documentation included