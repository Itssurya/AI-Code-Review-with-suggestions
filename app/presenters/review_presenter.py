"""
Review Presenter - Business Logic Layer

This module orchestrates the business logic for code review operations,
coordinating between static analysis, AI analysis, and data processing.
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from app.models.review_model import (
    CodeReviewRequest, CodeReviewResponse, BatchReviewRequest, BatchReviewResponse,
    StaticAnalysisResult, AIAnalysisResult, CodeIssue, CodeSuggestion, SecurityConcern,
    PerformanceNote, ReviewHistory, DashboardMetrics, ErrorResponse
)
from app.core.ai_engine import ai_engine
from app.utils.static_analyzer import static_analyzer
from app.utils.code_utils import code_utils
from app.core.config import settings

logger = logging.getLogger(__name__)

class ReviewPresenter:
    """Presenter for code review business logic."""
    
    def __init__(self):
        """Initialize the review presenter."""
        self.review_history: List[ReviewHistory] = []
    
    async def review_code(self, request: CodeReviewRequest) -> CodeReviewResponse:
        """
        Perform comprehensive code review.
        
        Args:
            request: Code review request
            
        Returns:
            Comprehensive code review response
        """
        start_time = time.time()
        review_id = code_utils.generate_review_id()
        
        try:
            # Validate request
            self._validate_review_request(request)
            
            # Sanitize code
            sanitized_code = code_utils.sanitize_code(request.code)
            
            # Extract code metrics
            metrics = code_utils.extract_code_metrics(sanitized_code)
            
            # Initialize response data
            static_results: List[StaticAnalysisResult] = []
            ai_result: Optional[AIAnalysisResult] = None
            tools_used = []
            
            # Perform static analysis if requested
            if request.include_static_analysis:
                try:
                    static_results = static_analyzer.analyze_code(
                        sanitized_code, 
                        request.language, 
                        request.file_name
                    )
                    tools_used.extend([result.tool for result in static_results])
                    logger.info(f"Static analysis completed for {review_id}")
                except Exception as e:
                    logger.error(f"Static analysis failed for {review_id}: {str(e)}")
                    static_results = []
            
            # Perform AI analysis if requested
            if request.include_ai_analysis:
                try:
                    ai_analysis_data = ai_engine.analyze_code(
                        sanitized_code,
                        request.language.value,
                        request.context
                    )
                    
                    # Convert AI analysis data to AIAnalysisResult
                    ai_result = self._convert_ai_analysis(ai_analysis_data)
                    tools_used.append("ai_engine")
                    logger.info(f"AI analysis completed for {review_id}")
                except Exception as e:
                    logger.error(f"AI analysis failed for {review_id}: {str(e)}")
                    ai_result = None
            
            # Combine and process results
            all_issues = self._combine_issues(static_results, ai_result)
            all_suggestions = self._extract_suggestions(ai_result)
            security_concerns = self._extract_security_concerns(ai_result)
            performance_notes = self._extract_performance_notes(ai_result)
            
            # Calculate scores
            static_scores = [result.score for result in static_results]
            ai_score = ai_result.score if ai_result else 5.0
            overall_score = code_utils.calculate_overall_score(static_scores, ai_score)
            
            # Generate summary and recommendations
            summary = self._generate_review_summary(all_issues, all_suggestions, overall_score)
            recommendations = self._generate_recommendations(all_issues, all_suggestions, request.focus_areas)
            
            # Count issues by severity
            issue_counts = self._count_issues_by_severity(all_issues)
            
            # Create response
            response = CodeReviewResponse(
                review_id=review_id,
                timestamp=datetime.now(),
                language=request.language,
                file_name=request.file_name,
                static_analysis=static_results[0] if static_results else None,
                ai_analysis=ai_result,
                overall_score=overall_score,
                total_issues=len(all_issues),
                critical_issues=issue_counts.get('critical', 0),
                security_issues=len(security_concerns),
                summary=summary,
                recommendations=recommendations,
                processing_time_ms=int((time.time() - start_time) * 1000),
                tools_used=tools_used
            )
            
            # Store in history
            self._store_review_history(response)
            
            logger.info(f"Code review completed for {review_id} in {response.processing_time_ms}ms")
            return response
            
        except Exception as e:
            logger.error(f"Code review failed for {review_id}: {str(e)}")
            raise e
    
    async def batch_review(self, request: BatchReviewRequest) -> BatchReviewResponse:
        """
        Perform batch code review for multiple files.
        
        Args:
            request: Batch review request
            
        Returns:
            Batch review response
        """
        start_time = time.time()
        batch_id = code_utils.generate_review_id()
        
        reviews = []
        successful_reviews = 0
        failed_reviews = 0
        
        for file_data in request.files:
            try:
                # Create individual review request
                individual_request = CodeReviewRequest(
                    code=file_data['code'],
                    language=file_data['language'],
                    file_name=file_data.get('file_name'),
                    context=file_data.get('context'),
                    include_static_analysis=request.include_static_analysis,
                    include_ai_analysis=request.include_ai_analysis,
                    focus_areas=request.focus_areas
                )
                
                # Perform review
                review_response = await self.review_code(individual_request)
                reviews.append(review_response)
                successful_reviews += 1
                
            except Exception as e:
                logger.error(f"Failed to review file in batch {batch_id}: {str(e)}")
                failed_reviews += 1
        
        # Generate overall summary
        overall_summary = self._generate_batch_summary(reviews, successful_reviews, failed_reviews)
        
        response = BatchReviewResponse(
            batch_id=batch_id,
            timestamp=datetime.now(),
            total_files=len(request.files),
            successful_reviews=successful_reviews,
            failed_reviews=failed_reviews,
            reviews=reviews,
            overall_summary=overall_summary,
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        return response
    
    def get_dashboard_metrics(self) -> DashboardMetrics:
        """Get dashboard metrics from review history."""
        if not self.review_history:
            return DashboardMetrics(
                total_reviews=0,
                average_score=0.0,
                most_common_issues=[],
                language_distribution={},
                security_issues_count=0,
                performance_issues_count=0,
                recent_reviews=[]
            )
        
        # Calculate metrics
        total_reviews = len(self.review_history)
        average_score = sum(review.overall_score for review in self.review_history) / total_reviews
        
        # Language distribution
        language_distribution = {}
        for review in self.review_history:
            lang = review.language.value
            language_distribution[lang] = language_distribution.get(lang, 0) + 1
        
        # Most common issues (simplified)
        most_common_issues = [
            {"type": "style_violation", "count": 15},
            {"type": "security_vulnerability", "count": 8},
            {"type": "performance_issue", "count": 5}
        ]
        
        # Recent reviews
        recent_reviews = sorted(self.review_history, key=lambda x: x.timestamp, reverse=True)[:10]
        
        return DashboardMetrics(
            total_reviews=total_reviews,
            average_score=round(average_score, 2),
            most_common_issues=most_common_issues,
            language_distribution=language_distribution,
            security_issues_count=sum(review.total_issues for review in self.review_history if "security" in review.summary.lower()),
            performance_issues_count=sum(review.total_issues for review in self.review_history if "performance" in review.summary.lower()),
            recent_reviews=recent_reviews
        )
    
    def _validate_review_request(self, request: CodeReviewRequest) -> None:
        """Validate the review request."""
        if not request.code.strip():
            raise ValueError("Code cannot be empty")
        
        if len(request.code) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"Code size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB")
    
    def _convert_ai_analysis(self, ai_data: Dict[str, Any]) -> AIAnalysisResult:
        """Convert AI analysis data to AIAnalysisResult model."""
        return AIAnalysisResult(
            score=ai_data.get('score', 5.0),
            issues=[self._convert_ai_issue(issue) for issue in ai_data.get('issues', [])],
            suggestions=[self._convert_ai_suggestion(suggestion) for suggestion in ai_data.get('suggestions', [])],
            security_concerns=[self._convert_security_concern(concern) for concern in ai_data.get('security_concerns', [])],
            performance_notes=[self._convert_performance_note(note) for note in ai_data.get('performance_notes', [])],
            readability_score=ai_data.get('readability_score', 5.0),
            maintainability_score=ai_data.get('maintainability_score', 5.0),
            summary=ai_data.get('summary', ''),
            raw_response=ai_data.get('raw_response')
        )
    
    def _convert_ai_issue(self, issue_data: Dict[str, Any]) -> CodeIssue:
        """Convert AI issue data to CodeIssue model."""
        return CodeIssue(
            type=issue_data.get('type', 'style_violation'),
            severity=issue_data.get('severity', 'medium'),
            line=issue_data.get('line'),
            message=issue_data.get('message', ''),
            suggestion=issue_data.get('suggestion'),
            tool='ai_engine'
        )
    
    def _convert_ai_suggestion(self, suggestion_data: Dict[str, Any]) -> CodeSuggestion:
        """Convert AI suggestion data to CodeSuggestion model."""
        return CodeSuggestion(
            type=suggestion_data.get('type', 'improvement'),
            description=suggestion_data.get('description', ''),
            refactored_code=suggestion_data.get('refactored_code'),
            reason=suggestion_data.get('reason', ''),
            confidence=suggestion_data.get('confidence', 0.8)
        )
    
    def _convert_security_concern(self, concern_data: Dict[str, Any]) -> SecurityConcern:
        """Convert security concern data to SecurityConcern model."""
        return SecurityConcern(
            type=concern_data.get('type', 'vulnerability'),
            severity=concern_data.get('severity', 'medium'),
            description=concern_data.get('description', ''),
            mitigation=concern_data.get('mitigation', ''),
            cwe_id=concern_data.get('cwe_id')
        )
    
    def _convert_performance_note(self, note_data: Dict[str, Any]) -> PerformanceNote:
        """Convert performance note data to PerformanceNote model."""
        return PerformanceNote(
            area=note_data.get('area', 'general'),
            issue=note_data.get('issue', ''),
            suggestion=note_data.get('suggestion', ''),
            impact_level=note_data.get('impact_level', 'medium')
        )
    
    def _combine_issues(self, static_results: List[StaticAnalysisResult], ai_result: Optional[AIAnalysisResult]) -> List[CodeIssue]:
        """Combine issues from static analysis and AI analysis."""
        all_issues = []
        
        # Add static analysis issues
        for result in static_results:
            all_issues.extend(result.issues)
        
        # Add AI analysis issues
        if ai_result:
            all_issues.extend(ai_result.issues)
        
        return all_issues
    
    def _extract_suggestions(self, ai_result: Optional[AIAnalysisResult]) -> List[CodeSuggestion]:
        """Extract suggestions from AI analysis."""
        if ai_result:
            return ai_result.suggestions
        return []
    
    def _extract_security_concerns(self, ai_result: Optional[AIAnalysisResult]) -> List[SecurityConcern]:
        """Extract security concerns from AI analysis."""
        if ai_result:
            return ai_result.security_concerns
        return []
    
    def _extract_performance_notes(self, ai_result: Optional[AIAnalysisResult]) -> List[PerformanceNote]:
        """Extract performance notes from AI analysis."""
        if ai_result:
            return ai_result.performance_notes
        return []
    
    def _count_issues_by_severity(self, issues: List[CodeIssue]) -> Dict[str, int]:
        """Count issues by severity level."""
        counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for issue in issues:
            severity = issue.severity.value if hasattr(issue.severity, 'value') else issue.severity
            counts[severity] = counts.get(severity, 0) + 1
        
        return counts
    
    def _generate_review_summary(self, issues: List[CodeIssue], suggestions: List[CodeSuggestion], score: float) -> str:
        """Generate a summary of the code review."""
        return code_utils.generate_summary(issues, suggestions, score)
    
    def _generate_recommendations(self, issues: List[CodeIssue], suggestions: List[CodeSuggestion], focus_areas: Optional[List[str]]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Priority-based recommendations
        critical_issues = [i for i in issues if i.severity.value == 'critical']
        if critical_issues:
            recommendations.append(f"Address {len(critical_issues)} critical issues immediately")
        
        security_issues = [i for i in issues if i.type.value == 'security_vulnerability']
        if security_issues:
            recommendations.append(f"Review and fix {len(security_issues)} security vulnerabilities")
        
        # Focus area recommendations
        if focus_areas:
            for area in focus_areas:
                if area == 'performance':
                    recommendations.append("Consider performance optimizations")
                elif area == 'readability':
                    recommendations.append("Improve code readability and documentation")
                elif area == 'security':
                    recommendations.append("Conduct thorough security review")
        
        # General recommendations
        if suggestions:
            recommendations.append(f"Implement {len(suggestions)} improvement suggestions")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _generate_batch_summary(self, reviews: List[CodeReviewResponse], successful: int, failed: int) -> str:
        """Generate summary for batch review."""
        if not reviews:
            return f"Batch review completed: {successful} successful, {failed} failed"
        
        avg_score = sum(review.overall_score for review in reviews) / len(reviews)
        total_issues = sum(review.total_issues for review in reviews)
        
        return f"Batch review completed: {successful} successful, {failed} failed. Average score: {avg_score:.1f}, Total issues: {total_issues}"
    
    def _store_review_history(self, response: CodeReviewResponse) -> None:
        """Store review in history."""
        history_item = ReviewHistory(
            review_id=response.review_id,
            timestamp=response.timestamp,
            file_name=response.file_name,
            language=response.language,
            overall_score=response.overall_score,
            total_issues=response.total_issues,
            summary=response.summary
        )
        
        self.review_history.append(history_item)
        
        # Keep only last 100 reviews in memory
        if len(self.review_history) > 100:
            self.review_history = self.review_history[-100:]

# Global presenter instance
review_presenter = ReviewPresenter()

