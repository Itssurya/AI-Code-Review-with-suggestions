"""
API Routes for Code Review

This module defines FastAPI routes for the code review endpoints,
handling HTTP requests and responses.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

from app.models.review_model import (
    CodeReviewRequest, CodeReviewResponse, BatchReviewRequest, BatchReviewResponse,
    DashboardMetrics, ErrorResponse, ProgrammingLanguage
)
from app.presenters.review_presenter import review_presenter
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    Review a single code file.
    
    This endpoint performs comprehensive code analysis including:
    - Static analysis (Pylint, ESLint, Bandit)
    - AI-powered analysis for logic, security, and performance
    - Code quality scoring and suggestions
    """
    try:
        logger.info(f"Starting code review for {request.language} code")
        
        # Validate file extension if file_name is provided
        if request.file_name:
            detected_lang = code_utils.detect_language_from_filename(request.file_name)
            if detected_lang and detected_lang != request.language.value:
                logger.warning(f"Language mismatch: detected {detected_lang}, specified {request.language.value}")
        
        # Perform review
        response = await review_presenter.review_code(request)
        
        logger.info(f"Code review completed: {response.review_id}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Code review failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Code review failed: {str(e)}")

@router.post("/review/batch", response_model=BatchReviewResponse)
async def batch_review(request: BatchReviewRequest):
    """
    Review multiple code files in batch.
    
    This endpoint allows reviewing multiple files at once for efficiency.
    Useful for reviewing entire projects or multiple related files.
    """
    try:
        logger.info(f"Starting batch review for {len(request.files)} files")
        
        # Validate batch size
        if len(request.files) > 50:  # Limit batch size
            raise HTTPException(status_code=400, detail="Batch size cannot exceed 50 files")
        
        # Perform batch review
        response = await review_presenter.batch_review(request)
        
        logger.info(f"Batch review completed: {response.batch_id}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Batch review failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch review failed: {str(e)}")

@router.get("/review/{review_id}", response_model=CodeReviewResponse)
async def get_review(review_id: str):
    """
    Get a specific review by ID.
    
    This endpoint retrieves the results of a previously performed code review.
    """
    try:
        # Find review in history
        for review in review_presenter.review_history:
            if review.review_id == review_id:
                # Convert ReviewHistory back to CodeReviewResponse
                # This is a simplified version - in production, you'd store full responses
                return CodeReviewResponse(
                    review_id=review.review_id,
                    timestamp=review.timestamp,
                    language=review.language,
                    file_name=review.file_name,
                    overall_score=review.overall_score,
                    total_issues=review.total_issues,
                    critical_issues=0,  # Would need to store this
                    security_issues=0,  # Would need to store this
                    summary=review.summary,
                    recommendations=[],  # Would need to store this
                    processing_time_ms=0,  # Would need to store this
                    tools_used=[]  # Would need to store this
                )
        
        raise HTTPException(status_code=404, detail="Review not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get review {review_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve review: {str(e)}")

@router.get("/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics():
    """
    Get dashboard metrics and statistics.
    
    This endpoint provides aggregated metrics for the dashboard including:
    - Total reviews performed
    - Average code quality scores
    - Most common issues
    - Language distribution
    - Security and performance issue counts
    """
    try:
        metrics = review_presenter.get_dashboard_metrics()
        return metrics
        
    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")

@router.get("/languages", response_model=List[str])
async def get_supported_languages():
    """
    Get list of supported programming languages.
    
    Returns the list of programming languages that the AI Code Reviewer supports.
    """
    return [lang.value for lang in ProgrammingLanguage]

@router.post("/refactor")
async def refactor_code(
    code: str,
    language: ProgrammingLanguage,
    improvement_type: str = "readability"
):
    """
    Generate refactored code suggestions.
    
    This endpoint uses AI to generate improved versions of the provided code
    focusing on specific improvement areas like readability, performance, etc.
    """
    try:
        if not code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        # Generate refactored code using AI engine
        refactored_code = ai_engine.generate_refactored_code(code, language.value, improvement_type)
        
        return {
            "original_code": code,
            "refactored_code": refactored_code,
            "improvement_type": improvement_type,
            "language": language.value
        }
        
    except Exception as e:
        logger.error(f"Code refactoring failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Code refactoring failed: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the AI Code Reviewer service.
    """
    try:
        # Check if AI engine is available
        ai_available = bool(settings.OPENAI_API_KEY or settings.COHERE_API_KEY or settings.ANTHROPIC_API_KEY)
        
        # Check static analysis tools
        static_tools_available = {
            "pylint": settings.PYLINT_ENABLED,
            "eslint": settings.ESLINT_ENABLED,
            "bandit": settings.BANDIT_ENABLED
        }
        
        return {
            "status": "healthy",
            "ai_engine_available": ai_available,
            "static_tools": static_tools_available,
            "version": settings.VERSION
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

@router.get("/config")
async def get_configuration():
    """
    Get current configuration (non-sensitive settings only).
    
    Returns the current configuration settings that are safe to expose.
    """
    return {
        "max_file_size_mb": settings.MAX_FILE_SIZE_MB,
        "allowed_file_extensions": settings.ALLOWED_FILE_EXTENSIONS,
        "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE,
        "static_tools_enabled": {
            "pylint": settings.PYLINT_ENABLED,
            "eslint": settings.ESLINT_ENABLED,
            "bandit": settings.BANDIT_ENABLED
        },
        "ai_model": settings.OPENAI_MODEL if settings.OPENAI_API_KEY else "not_configured",
        "version": settings.VERSION
    }

# Import required modules for the endpoints
from app.utils.code_utils import code_utils
from app.core.ai_engine import ai_engine

