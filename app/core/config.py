"""
Core Configuration Management

This module handles environment configuration and settings
for the AI Code Reviewer application.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Code Reviewer"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # AI Model Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.1
    
    # Alternative AI Models
    COHERE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Static Analysis Tools Configuration
    PYLINT_ENABLED: bool = True
    ESLINT_ENABLED: bool = True
    BANDIT_ENABLED: bool = True
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./ai_code_reviewer.db"
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_EXTENSIONS: List[str] = [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".go", ".rs"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that required settings are configured."""
    if not settings.OPENAI_API_KEY and not settings.COHERE_API_KEY and not settings.ANTHROPIC_API_KEY:
        raise ValueError("At least one AI API key must be configured (OpenAI, Cohere, or Anthropic)")
    
    return True

# Initialize settings validation
if __name__ == "__main__":
    validate_settings()
    print("Settings validation passed!")

