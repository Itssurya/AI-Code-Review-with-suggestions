#!/bin/bash

# AI Code Reviewer - Full Stack Startup Script

echo "🚀 Starting AI Code Reviewer Full Stack Application..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Check if backend is already running
if check_port 8000; then
    echo "✅ Backend already running on port 8000"
else
    echo "🐳 Starting backend with Docker..."
    docker compose up -d
    echo "⏳ Waiting for backend to be ready..."
    sleep 10
fi

# Check if frontend is already running
if check_port 3000; then
    echo "✅ Frontend already running on port 3000"
else
    echo "⚛️  Starting React frontend..."
    cd frontend
    npm start &
    cd ..
    echo "⏳ Waiting for frontend to be ready..."
    sleep 15
fi

echo ""
echo "🎉 AI Code Reviewer is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    docker compose down
    pkill -f "npm start"
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
while true; do
    sleep 1
done

