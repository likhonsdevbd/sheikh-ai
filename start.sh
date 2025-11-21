#!/bin/bash

# Sheikh AI Assistant Startup Script
# Author: Likhon Sheikh and Team Sheikh

set -e

echo "🚀 Starting Sheikh AI Assistant..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p dev_data logs uploads browser/user_data

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Copying environment configuration..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and set your OpenAI API key"
fi

# Build and start services
echo "🏗️  Building and starting services..."
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."

# Check backend
if curl -f http://localhost:8080/health &> /dev/null; then
    echo "✅ Backend service is running"
else
    echo "❌ Backend service is not responding"
fi

# Check VNC server
if netstat -tln | grep -q ":5900"; then
    echo "✅ VNC server is running on port 5900"
else
    echo "❌ VNC server is not responding"
fi

# Check Chrome debugging
if netstat -tln | grep -q ":9222"; then
    echo "✅ Chrome remote debugging is available on port 9222"
else
    echo "❌ Chrome remote debugging is not available"
fi

echo ""
echo "🎉 Sheikh AI Assistant is now running!"
echo ""
echo "📋 Service URLs:"
echo "   - Backend API: http://localhost:8080"
echo "   - Frontend: http://localhost:3000 (when running frontend separately)"
echo "   - VNC Access: localhost:5900"
echo "   - Chrome DevTools: http://localhost:9222"
echo ""
echo "🛠️  Development Commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart: ./start.sh"
echo ""
echo "📝 Don't forget to:"
echo "   1. Set your OpenAI API key in the .env file"
echo "   2. Run the frontend separately: cd frontend && npm run dev"
echo ""
echo "Happy coding! 👨‍💻"