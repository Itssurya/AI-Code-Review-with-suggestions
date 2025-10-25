#!/bin/bash

# AI Code Reviewer Startup Script (Updated for Virtual Environment)

echo "🚀 Starting AI Code Reviewer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed (for ESLint)
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed. ESLint will not be available."
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "📝 Please edit .env file with your API keys before running again."
        exit 1
    else
        echo "❌ env.example file not found. Please create .env file manually."
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install static analysis tools
echo "🔧 Installing static analysis tools..."
pip install pylint bandit

# Install ESLint if Node.js is available
if command -v npm &> /dev/null; then
    echo "📦 Installing ESLint..."
    npm install -g eslint
fi

# Create logs directory
mkdir -p logs

# Start the application
echo "🎯 Starting AI Code Reviewer API..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""

python app/main.py
