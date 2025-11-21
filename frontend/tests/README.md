# Testing Setup Guide

This document explains how to set up and run automated tests for the Sheikh AI application using Playwright and GitHub Actions.

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Playwright browsers installed

## Local Development Setup

### 1. Install Dependencies

```bash
# Install frontend dependencies (includes Playwright)
cd frontend
npm install

# Install Playwright browsers
npx playwright install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

### 2. Environment Setup

Create a `.env.test` file in the backend directory:

```bash
cd backend
cp .env.example .env.test

# Update the test environment variables
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sheikh_ai_test
GOOGLE_GENERATIVE_AI_API_KEY=your_test_api_key
OPENAI_API_KEY=your_test_api_key
```

### 3. Run Tests Locally

#### Start the services:

```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn app.interfaces.api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

#### Run tests:

```bash
# Run all tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests in headed mode (visible browser)
npm run test:headed

# Run specific test file
npx playwright test chat.spec.js

# Run tests with debug mode
npm run test:debug
```

## Test Structure

```
frontend/tests/
├── playwright.config.js    # Playwright configuration
├── chat.spec.js           # Chat interface tests
├── api.spec.js            # API endpoint tests
├── utils.js               # Test utilities and helpers
└── README.md              # This file
```

## Test Categories

### 1. Chat Interface Tests (`chat.spec.js`)
- Page loading and layout
- Message sending and receiving
- AI provider switching
- Conversation management
- File upload functionality
- Error handling
- Responsive design
- Accessibility features

### 2. API Tests (`api.spec.js`)
- Backend health check
- Conversation CRUD operations
- Message processing
- AI provider integration
- File upload endpoints
- Shell command execution
- Browser automation
- Request validation
- Error handling

### 3. Test Utilities (`utils.js`)
- Common helper functions
- API interaction helpers
- Data fixtures
- Performance monitoring
- Accessibility testing
- Responsive design checks

## GitHub Actions CI/CD

The project includes a comprehensive CI/CD pipeline that runs automatically:

### Workflow Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Daily scheduled runs (2 AM UTC)

### Pipeline Stages

1. **Backend Tests**
   - Python dependency installation
   - Pytest execution with coverage
   - Coverage report upload

2. **Frontend Tests**
   - Node.js setup with caching
   - Playwright browser installation
   - Service startup (backend + frontend)
   - End-to-end test execution
   - Report artifact upload

3. **Security Scanning**
   - Trivy vulnerability scanner
   - SARIF report generation
   - GitHub Security tab integration

4. **Performance Testing**
   - Basic load testing with concurrent requests
   - Success rate validation (95%+ required)

5. **Build and Deploy**
   - Docker image creation (main branch only)
   - Artifact storage

6. **Notifications**
   - Failure notifications
   - Success confirmations

## Environment Variables

The CI/CD pipeline requires the following GitHub Secrets:

- `GOOGLE_GENERATIVE_AI_API_KEY`: Google Gemini API key
- `OPENAI_API_KEY`: OpenAI API key

## Test Reports

### Local Reports
After running tests locally, you can view detailed reports:

```bash
# Generate and view HTML report
npm run test:report
```

### CI/CD Reports
- Playwright reports are uploaded as GitHub artifacts
- Coverage reports are sent to Codecov
- Security scan results appear in GitHub Security tab

## Best Practices

### Writing Tests
1. Use descriptive test names
2. Group related tests with `test.describe`
3. Use data-testid attributes for reliable element selection
4. Implement proper waits instead of fixed timeouts
5. Clean up test data after each test

### Test Data
- Use the `testData` fixture from `utils.js`
- Create unique test conversations to avoid conflicts
- Mock API responses for complex scenarios

### Performance
- Test on multiple viewport sizes
- Monitor load times and memory usage
- Validate responsive design

### Accessibility
- Include accessibility checks in every test
- Verify keyboard navigation
- Check color contrast and screen reader compatibility

## Troubleshooting

### Common Issues

1. **Tests fail with "element not found"**
   - Check if the element selectors are correct
   - Ensure the page has fully loaded
   - Use proper wait conditions

2. **Backend connection failures**
   - Verify backend is running on port 8000
   - Check environment variables
   - Ensure database connectivity

3. **Playwright browser installation issues**
   - Run `npx playwright install`
   - Check system dependencies
   - Clear npm cache if needed

4. **Flaky tests**
   - Increase wait timeouts
   - Add explicit waits for dynamic content
   - Use more specific selectors

### Debug Mode
Run tests in debug mode for detailed step-by-step execution:

```bash
npm run test:debug
```

### Browser Console
Check browser console for errors during test execution:

```javascript
// In test file
page.on('console', msg => console.log('PAGE LOG:', msg.text()))
page.on('pageerror', error => console.log('PAGE ERROR:', error.message))
```

## Continuous Improvement

1. **Monitor Test Results**: Review CI/CD reports regularly
2. **Update Tests**: Keep tests updated with new features
3. **Performance Monitoring**: Track test execution times
4. **Coverage Analysis**: Aim for high test coverage
5. **Feedback Loop**: Fix failing tests promptly

## Support

For issues related to:
- Test setup: Check this README and troubleshooting section
- Playwright: Refer to [official Playwright documentation](https://playwright.dev/)
- CI/CD: Review GitHub Actions logs and configuration
- Backend testing: Check pytest documentation and logs