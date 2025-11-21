#!/bin/bash

# Sheikh AI Assistant Stop Script
# Author: Likhon Sheikh and Team Sheikh

echo "🛑 Stopping Sheikh AI Assistant..."

# Stop and remove containers
if command -v docker-compose &> /dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "✅ All services stopped"
echo ""
echo "💡 To start again, run: ./start.sh"