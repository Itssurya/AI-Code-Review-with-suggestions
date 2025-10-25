# AI Code Reviewer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)

An AI-powered platform that automatically reviews code, detects issues, and suggests improvements using both static analysis tools and large language models (LLMs).

## 🌟 Features Overview

- 🤖 **AI-Powered Analysis**: Leverage GPT-4, Claude, and Cohere for intelligent code review
- 🔍 **Static Analysis**: Integration with Pylint, ESLint, and Bandit for comprehensive code quality checks
- 🎨 **Modern UI**: Beautiful React frontend with Tailwind CSS
- 🚀 **Fast API**: High-performance FastAPI backend with automatic documentation
- 📊 **Analytics Dashboard**: Track code quality metrics and trends
- 🔒 **Security Scanning**: Identify vulnerabilities and security issues
- 🌐 **Multi-language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more

## 🎯 Project Status

**Sprint 2 Complete**: Frontend integration with React + Tailwind CSS ✅

- ✅ **Sprint 1**: Backend MVP with AI + Static review endpoint
- ✅ **Sprint 2**: Frontend integration with code editor and API  
- 🔄 **Sprint 3**: Smart features - auto-fix, scoring, multi-language support
- ⏳ **Sprint 4**: Deployment, analytics dashboard, authentication, GitHub integration

## 📋 Table of Contents

- [Features](#-features-overview)
- [Project Status](#-project-status)
- [Architecture](#️-architecture)
- [Tech Stack](#️-tech-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Frontend Usage](#-frontend-usage)
- [API Usage](#-api-usage)
- [Configuration](#-configuration-options)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [Production Deployment](#-production-deployment)
- [Security](#-security-considerations)
- [Contributing](#-contributing)
- [License](#-license)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)

## 🏗️ Architecture

The project follows a full-stack architecture with MVP (Model-View-Presenter) pattern:

```
AI-Code-Review/
├── app/                         # Backend (FastAPI)
│   ├── main.py                  # FastAPI application entry point
│   ├── core/
│   │   ├── config.py            # Environment configuration
│   │   └── ai_engine.py         # AI logic (Presenter)
│   ├── models/
│   │   └── review_model.py      # Pydantic data models
│   ├── routers/
│   │   └── review_router.py     # API endpoints (View)
│   ├── presenters/
│   │   └── review_presenter.py  # Business logic orchestration
│   └── utils/
│       ├── static_analyzer.py   # Static analysis tools integration
│       └── code_utils.py        # Helper functions
├── frontend/                    # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── CodeEditor.tsx   # Code input component
│   │   │   ├── ReviewResults.tsx # Results display
│   │   │   ├── Dashboard.tsx    # Analytics dashboard
│   │   │   └── Header.tsx       # Navigation header
│   │   ├── services/
│   │   │   └── api.ts           # API service layer
│   │   └── App.tsx              # Main application
│   ├── package.json
│   └── tailwind.config.js       # Tailwind CSS config
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Backend container
├── requirements-minimal.txt     # Python dependencies
└── README.md
```

### Workflow
```
API Request → Presenter → Model Validation → AI Engine + Static Analysis → Response
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI Models**: OpenAI GPT-4, Cohere, Anthropic Claude
- **Static Analysis**: Pylint, ESLint, Bandit
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Docker, AWS/Render/Vercel

### Frontend
- **Framework**: React 19 with TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Code Highlighting**: React Syntax Highlighter
- **Build Tool**: Create React App

## 📋 Prerequisites

- Python 3.8+
- Node.js (for ESLint)
- At least one AI API key (OpenAI, Cohere, or Anthropic)

## 🚀 Quick Start

### Option 1: Full Stack (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/AI-Code-Review.git
cd AI-Code-Review

# Start both frontend and backend
./start-fullstack.sh
```

This will start:
- **Backend**: Docker containers on port 8000
- **Frontend**: React app on port 3000

### Option 2: Manual Setup

#### Backend Only

```bash
# Install Python dependencies
pip install -r requirements-minimal.txt

# Install static analysis tools
pip install pylint bandit
npm install -g eslint

# Start backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Only

```bash
cd frontend
npm install
npm start
```

### 3. Install Static Analysis Tools

```bash
# Install Pylint
pip install pylint

# Install Bandit
pip install bandit

# Install ESLint (if not already installed)
npm install -g eslint
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# AI API Keys (at least one required)
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# AI Model Configuration
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.1

# Static Analysis Tools
PYLINT_ENABLED=true
ESLINT_ENABLED=true
BANDIT_ENABLED=true

# Security
SECRET_KEY=your-secret-key-change-in-production

# File Upload Limits
MAX_FILE_SIZE_MB=10

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### 5. Run the Application

```bash
# Development mode
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py directly
python app/main.py
```

The API will be available at `http://localhost:8000`

### 6. Access the Application

- **Frontend**: http://localhost:3000 (React app)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 Frontend Usage

### Code Editor
1. **Select Language**: Choose from Python, JavaScript, TypeScript, Java, C++, Go, Rust
2. **Enter Code**: Type or paste your code in the editor
3. **Upload File**: Click "Upload File" to load code from a file
4. **Review Code**: Click "Review Code" to analyze your code

### Review Results
- **Overall Score**: See your code's quality score (0-100)
- **AI Analysis**: Get AI-powered insights and suggestions
- **Static Analysis**: View Pylint, Bandit, and ESLint results
- **Issues**: See detailed issues with severity levels
- **Suggestions**: Get improvement recommendations

### Dashboard
- **Analytics**: View review statistics and trends
- **Language Distribution**: See which languages you use most
- **Common Issues**: Identify recurring problems
- **Metrics**: Track your code quality over time

## 📖 API Usage

### Single Code Review

```bash
curl -X POST "http://localhost:8000/api/v1/review" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello_world():\n    print(\"Hello, World!\")\n    return True",
    "language": "python",
    "file_name": "hello.py",
    "include_static_analysis": true,
    "include_ai_analysis": true,
    "focus_areas": ["security", "performance"]
  }'
```

### Batch Code Review

```bash
curl -X POST "http://localhost:8000/api/v1/review/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "code": "def func1():\n    pass",
        "language": "python",
        "file_name": "file1.py"
      },
      {
        "code": "function func2() {\n    console.log(\"test\");\n}",
        "language": "javascript",
        "file_name": "file2.js"
      }
    ],
    "include_static_analysis": true,
    "include_ai_analysis": true
  }'
```

### Get Dashboard Metrics

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/metrics"
```

### Code Refactoring

```bash
curl -X POST "http://localhost:8000/api/v1/refactor" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def calculate(x,y):\n    return x+y",
    "language": "python",
    "improvement_type": "readability"
  }'
```

## 🔧 Configuration Options

### AI Model Configuration

- **OpenAI**: Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` (default: gpt-4)
- **Cohere**: Set `COHERE_API_KEY`
- **Anthropic**: Set `ANTHROPIC_API_KEY`

### Static Analysis Tools

- **Pylint**: Enable/disable with `PYLINT_ENABLED`
- **ESLint**: Enable/disable with `ESLINT_ENABLED`
- **Bandit**: Enable/disable with `BANDIT_ENABLED`

### File Processing

- **Max File Size**: Configure with `MAX_FILE_SIZE_MB`
- **Allowed Extensions**: Modify `ALLOWED_FILE_EXTENSIONS` in config

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_review_presenter.py
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t ai-code-reviewer .
```

### Run with Docker

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  ai-code-reviewer
```

### Docker Compose

```yaml
version: '3.8'
services:
  ai-code-reviewer:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/ai_code_reviewer
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=ai_code_reviewer
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🚀 Production Deployment

### AWS Deployment

1. **EC2 Instance**:
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3-pip nodejs npm
   
   # Install static analysis tools
   pip3 install pylint bandit
   npm install -g eslint
   
   # Run application
   pip3 install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **AWS Lambda** (using Mangum):
   ```python
   from mangum import Mangum
   from app.main import app
   
   handler = Mangum(app)
   ```

### Render Deployment

1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

## 📊 Monitoring and Logging

The application includes comprehensive logging:

```python
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# View logs
tail -f logs/app.log
```

## 🔒 Security Considerations

- **API Keys**: Store securely in environment variables
- **Input Validation**: All inputs are validated using Pydantic
- **Rate Limiting**: Configure with `RATE_LIMIT_PER_MINUTE`
- **CORS**: Configure allowed origins
- **File Size Limits**: Prevent abuse with file size restrictions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/AI-Code-Review.git
   cd AI-Code-Review
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and add tests
5. **Run tests** to ensure everything works:
   ```bash
   pytest
   npm test  # in frontend directory
   ```
6. **Commit your changes**:
   ```bash
   git commit -m "Add your feature"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Submit a pull request** on GitHub

### Development Setup

For contributors, we recommend using the development environment:

```bash
# Install development dependencies
pip install -r requirements.txt
cd frontend && npm install

# Run in development mode
python -m uvicorn app.main:app --reload
cd frontend && npm start
```

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript/React**: Use Prettier and ESLint
- **Commits**: Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **AI Analysis Failing**:
   - Check API key configuration
   - Verify API key has sufficient credits
   - Check network connectivity

2. **Static Analysis Tools Not Found**:
   - Ensure tools are installed globally
   - Check PATH environment variable
   - Install missing dependencies

3. **CORS Issues**:
   - Update `ALLOWED_ORIGINS` in configuration
   - Check frontend URL configuration

4. **File Upload Issues**:
   - Check file size limits
   - Verify file extension is allowed
   - Ensure proper MIME type handling

### Getting Help

- 🐛 **Bug Reports**: [Open an issue](https://github.com/your-username/AI-Code-Review/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Request a feature](https://github.com/your-username/AI-Code-Review/issues/new?template=feature_request.md)
- 💬 **Discussions**: [Join our discussions](https://github.com/your-username/AI-Code-Review/discussions)
- 📖 **Documentation**: Review the API documentation at `/docs`
- 📋 **Check logs** for detailed error messages

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] AI-powered code analysis
- [x] Static analysis integration
- [x] Modern React frontend
- [x] RESTful API

### Phase 2: Advanced Features 🔄
- [ ] GitHub PR integration
- [ ] Real-time code review notifications
- [ ] Custom rule configuration
- [ ] Team collaboration features

### Phase 3: Enterprise Features ⏳
- [ ] Advanced security scanning
- [ ] Performance benchmarking
- [ ] Code quality trends analysis
- [ ] Integration with CI/CD pipelines
- [ ] Multi-tenant support
- [ ] Advanced analytics dashboard

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4 API
- [Cohere](https://cohere.ai/) for language model API
- [Anthropic](https://www.anthropic.com/) for Claude API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Pylint](https://pylint.org/), [ESLint](https://eslint.org/), and [Bandit](https://bandit.readthedocs.io/) teams for static analysis tools
- [React](https://reactjs.org/) and [Tailwind CSS](https://tailwindcss.com/) for the frontend framework

## 📞 Support

If you find this project helpful, please consider:

- ⭐ **Starring** the repository
- 🍴 **Forking** for your own use
- 🐛 **Reporting bugs** and issues
- 💡 **Suggesting** new features
- 🤝 **Contributing** code improvements

---


