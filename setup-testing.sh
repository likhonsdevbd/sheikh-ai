#!/bin/bash

# Sheikh AI Testing Setup Script
# This script sets up the complete testing environment for the Sheikh AI project

set -e  # Exit on any error

echo "🚀 Setting up Sheikh AI Testing Environment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js installation..."
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ and try again."
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1)
    
    if [ "$MAJOR_VERSION" -lt 18 ]; then
        print_error "Node.js version $NODE_VERSION is too old. Please install Node.js 18+ and try again."
        exit 1
    fi
    
    print_success "Node.js version $NODE_VERSION detected"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11+ and try again."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python version $PYTHON_VERSION detected"
}

# Check if PostgreSQL is available
check_postgres() {
    print_status "Checking PostgreSQL availability..."
    if ! command -v psql &> /dev/null; then
        print_warning "PostgreSQL client not found. Some database tests may fail."
        print_warning "Install PostgreSQL or ensure it's running on localhost:5432"
    else
        print_success "PostgreSQL client found"
    fi
}

# Setup frontend dependencies
setup_frontend() {
    print_status "Setting up frontend testing environment..."
    
    if [ ! -d "frontend" ]; then
        print_error "Frontend directory not found. Please run this script from the project root."
        exit 1
    fi
    
    cd frontend
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    # Install Playwright browsers
    print_status "Installing Playwright browsers..."
    npx playwright install
    
    print_success "Frontend setup complete"
    cd ..
}

# Setup backend dependencies
setup_backend() {
    print_status "Setting up backend testing environment..."
    
    if [ ! -d "backend" ]; then
        print_error "Backend directory not found. Please run this script from the project root."
        exit 1
    fi
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Install test dependencies
    print_status "Installing test dependencies..."
    pip install pytest pytest-asyncio httpx
    
    print_success "Backend setup complete"
    cd ..
}

# Create test environment file
create_test_env() {
    print_status "Creating test environment configuration..."
    
    if [ -f "backend/.env.test" ]; then
        print_warning "Test environment file already exists. Skipping creation."
        return
    fi
    
    cat > backend/.env.test << EOF
# Test Environment Configuration for Sheikh AI
# This file is used for automated testing

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sheikh_ai_test

# API Keys (Replace with test keys)
GOOGLE_GENERATIVE_AI_API_KEY=your_test_google_api_key_here
OPENAI_API_KEY=your_test_openai_api_key_here

# Application Settings
APP_NAME=Sheikh AI Test
DEBUG=true
ENVIRONMENT=testing

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
EOF
    
    print_success "Test environment file created at backend/.env.test"
    print_warning "Please update the API keys in backend/.env.test with actual test keys"
}

# Verify test configuration
verify_setup() {
    print_status "Verifying test setup..."
    
    # Check if Playwright is properly installed
    cd frontend
    if ! npx playwright --version &> /dev/null; then
        print_error "Playwright installation verification failed"
        exit 1
    fi
    print_success "Playwright verification passed"
    cd ..
    
    # Check if pytest is available in backend
    cd backend
    source venv/bin/activate
    if ! python -m pytest --version &> /dev/null; then
        print_error "Pytest verification failed"
        exit 1
    fi
    print_success "Pytest verification passed"
    cd ..
    
    # Check test files exist
    if [ ! -f "frontend/tests/chat.spec.js" ]; then
        print_error "Test files not found. Please ensure all test files are present."
        exit 1
    fi
    
    print_success "All verifications passed"
}

# Display usage instructions
show_usage() {
    echo ""
    echo "✅ Testing environment setup complete!"
    echo ""
    echo "📋 Next steps:"
    echo ""
    echo "1. Update API keys in backend/.env.test"
    echo "2. Start the backend server:"
    echo "   cd backend && source venv/bin/activate"
    echo "   python -m uvicorn app.interfaces.api.main:app --host 0.0.0.0 --port 8000"
    echo ""
    echo "3. In another terminal, start the frontend server:"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
    echo "4. Run tests:"
    echo "   cd frontend"
    echo "   npm run test          # Run all tests"
    echo "   npm run test:ui       # Run tests with UI"
    echo "   npm run test:headed   # Run tests in headed mode"
    echo ""
    echo "📊 Test reports will be available at:"
    echo "   frontend/test-results/"
    echo ""
    echo "🔧 Available test commands:"
    echo "   npm run test              # Run all tests"
    echo "   npm run test:ui           # Interactive test runner"
    echo "   npm run test:debug        # Debug mode"
    echo "   npm run test:headed       # Visible browser"
    echo "   npm run test:report       # Show test report"
    echo ""
    echo "📖 For more information, see:"
    echo "   frontend/tests/README.md"
    echo ""
    print_success "Happy testing! 🎯"
}

# Main execution
main() {
    echo "Starting setup process..."
    
    # Pre-flight checks
    check_node
    check_python
    check_postgres
    
    # Setup environments
    setup_frontend
    setup_backend
    
    # Create configuration files
    create_test_env
    
    # Verify everything is working
    verify_setup
    
    # Show usage instructions
    show_usage
}

# Run main function
main "$@"