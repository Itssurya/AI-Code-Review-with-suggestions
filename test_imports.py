#!/usr/bin/env python3
"""
Simple test script to verify AI Code Reviewer imports and basic functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    
    # Test core imports
    from app.core.config import settings
    print("✅ Core config imported successfully")
    
    from app.models.review_model import CodeReviewRequest, ProgrammingLanguage
    print("✅ Models imported successfully")
    
    from app.core.ai_engine import ai_engine
    print("✅ AI engine imported successfully")
    
    from app.utils.static_analyzer import static_analyzer
    print("✅ Static analyzer imported successfully")
    
    from app.utils.code_utils import code_utils
    print("✅ Code utils imported successfully")
    
    from app.presenters.review_presenter import review_presenter
    print("✅ Review presenter imported successfully")
    
    from app.routers.review_router import router
    print("✅ Review router imported successfully")
    
    from app.main import app
    print("✅ Main app imported successfully")
    
    print("\n🎉 All imports successful! The AI Code Reviewer is ready to run.")
    print(f"📊 Configuration loaded: {settings.PROJECT_NAME} v{settings.VERSION}")
    
    # Test basic functionality
    print("\nTesting basic functionality...")
    
    # Test code utils
    test_code = "def hello():\n    print('Hello World')"
    metrics = code_utils.extract_code_metrics(test_code)
    print(f"✅ Code metrics extracted: {metrics['total_lines']} lines")
    
    # Test language detection
    lang = code_utils.detect_language_from_filename("test.py")
    print(f"✅ Language detection: {lang}")
    
    print("\n🚀 Ready to start the server!")
    print("Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

