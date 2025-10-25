"""
AI Code Reviewer - Main Application Entry Point

This is the FastAPI application that serves as the main entry point
for the AI-powered code review platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import review_router
from app.core.config import settings

# Initialize FastAPI application
app = FastAPI(
    title="AI Code Reviewer",
    description="AI-powered platform for automated code review and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(review_router.router, prefix="/api/v1", tags=["code-review"])

@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "AI Code Reviewer API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "ai-code-reviewer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

