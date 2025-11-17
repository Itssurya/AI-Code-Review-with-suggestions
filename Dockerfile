# Dockerfile for AI Code Reviewer

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install global Node.js packages for static analysis
RUN npm install -g eslint

# Copy requirements and install Python dependencies
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Install additional static analysis tools
RUN pip install pylint bandit

# Copy application code
COPY app/ ./app/

# Copy startup script
COPY start.sh ./start.sh
RUN chmod +x ./start.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port (Railway uses PORT env variable)
EXPOSE ${PORT:-8000}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run the application (Railway provides PORT env variable)
CMD ./start.sh

