"""
Data Models for Code Review

This module defines Pydantic models for data validation and serialization
in the AI Code Reviewer application.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime

class SeverityLevel(str, Enum):
    """Severity levels for code issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IssueType(str, Enum):
    """Types of code issues."""
    SYNTAX_ERROR = "syntax_error"
    STYLE_VIOLATION = "style_violation"
    LOGIC_ERROR = "logic_error"
    SECURITY_VULNERABILITY = "security_vulnerability"
    PERFORMANCE_ISSUE = "performance_issue"
    MAINTAINABILITY_ISSUE = "maintainability_issue"
    DOCUMENTATION_ISSUE = "documentation_issue"

class ProgrammingLanguage(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"

class CodeIssue(BaseModel):
    """Model for individual code issues."""
    type: IssueType
    severity: SeverityLevel
    line: Optional[int] = None
    column: Optional[int] = None
    message: str
    suggestion: Optional[str] = None
    rule_id: Optional[str] = None
    tool: Optional[str] = None  # Which tool found this issue

class CodeSuggestion(BaseModel):
    """Model for code improvement suggestions."""
    type: str
    description: str
    refactored_code: Optional[str] = None
    reason: str
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)

class SecurityConcern(BaseModel):
    """Model for security-related issues."""
    type: str
    severity: SeverityLevel
    description: str
    mitigation: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID

class PerformanceNote(BaseModel):
    """Model for performance-related observations."""
    area: str
    issue: str
    suggestion: str
    impact_level: str = Field(default="medium")  # low, medium, high

class StaticAnalysisResult(BaseModel):
    """Model for static analysis tool results."""
    tool: str
    issues: List[CodeIssue]
    score: float = Field(ge=0.0, le=10.0)
    summary: str

class AIAnalysisResult(BaseModel):
    """Model for AI analysis results."""
    score: float = Field(ge=0.0, le=10.0)
    issues: List[CodeIssue]
    suggestions: List[CodeSuggestion]
    security_concerns: List[SecurityConcern]
    performance_notes: List[PerformanceNote]
    readability_score: float = Field(ge=0.0, le=10.0)
    maintainability_score: float = Field(ge=0.0, le=10.0)
    summary: str
    raw_response: Optional[str] = None

class CodeReviewRequest(BaseModel):
    """Model for code review requests."""
    code: str = Field(..., min_length=1, description="The code to review")
    language: ProgrammingLanguage
    context: Optional[str] = Field(None, description="Additional context about the code")
    file_name: Optional[str] = Field(None, description="Name of the file being reviewed")
    include_static_analysis: bool = Field(default=True, description="Include static analysis")
    include_ai_analysis: bool = Field(default=True, description="Include AI analysis")
    focus_areas: Optional[List[str]] = Field(
        default=None, 
        description="Specific areas to focus on (security, performance, readability, etc.)"
    )

class CodeReviewResponse(BaseModel):
    """Model for code review responses."""
    review_id: str
    timestamp: datetime
    language: ProgrammingLanguage
    file_name: Optional[str]
    
    # Analysis results
    static_analysis: Optional[StaticAnalysisResult] = None
    ai_analysis: Optional[AIAnalysisResult] = None
    
    # Overall metrics
    overall_score: float = Field(ge=0.0, le=10.0)
    total_issues: int
    critical_issues: int
    security_issues: int
    
    # Summary
    summary: str
    recommendations: List[str]
    
    # Processing info
    processing_time_ms: int
    tools_used: List[str]

class BatchReviewRequest(BaseModel):
    """Model for batch code review requests."""
    files: List[Dict[str, Union[str, ProgrammingLanguage]]] = Field(
        ..., 
        description="List of files to review with code and language"
    )
    include_static_analysis: bool = Field(default=True)
    include_ai_analysis: bool = Field(default=True)
    focus_areas: Optional[List[str]] = None

class BatchReviewResponse(BaseModel):
    """Model for batch code review responses."""
    batch_id: str
    timestamp: datetime
    total_files: int
    successful_reviews: int
    failed_reviews: int
    reviews: List[CodeReviewResponse]
    overall_summary: str
    processing_time_ms: int

class ReviewHistory(BaseModel):
    """Model for review history tracking."""
    review_id: str
    timestamp: datetime
    file_name: Optional[str]
    language: ProgrammingLanguage
    overall_score: float
    total_issues: int
    summary: str

class DashboardMetrics(BaseModel):
    """Model for dashboard metrics."""
    total_reviews: int
    average_score: float
    most_common_issues: List[Dict[str, Any]]
    language_distribution: Dict[str, int]
    security_issues_count: int
    performance_issues_count: int
    recent_reviews: List[ReviewHistory]

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# Validators
@validator('code')
def validate_code_not_empty(cls, v):
    """Validate that code is not empty."""
    if not v.strip():
        raise ValueError('Code cannot be empty')
    return v

@validator('focus_areas')
def validate_focus_areas(cls, v):
    """Validate focus areas."""
    if v is not None:
        valid_areas = ['security', 'performance', 'readability', 'maintainability', 'style', 'documentation']
        for area in v:
            if area.lower() not in valid_areas:
                raise ValueError(f'Invalid focus area: {area}. Valid areas: {valid_areas}')
    return v

