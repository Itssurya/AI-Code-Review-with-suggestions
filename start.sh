#!/bin/bash
# Startup script for Railway deployment
# Uses PORT environment variable provided by Railway

PORT=${PORT:-8000}

echo "Starting AI Code Reviewer on port $PORT"

exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
