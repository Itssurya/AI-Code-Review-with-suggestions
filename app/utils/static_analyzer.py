"""
Static Analysis Tools Integration

This module integrates various static analysis tools including
Pylint, ESLint, and Bandit for comprehensive code analysis.
"""

import subprocess
import tempfile
import os
import json
import re
from typing import List, Dict, Any, Optional
from app.models.review_model import (
    CodeIssue, IssueType, SeverityLevel, StaticAnalysisResult, 
    ProgrammingLanguage
)
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class StaticAnalyzer:
    """Static analysis tool integration."""
    
    def __init__(self):
        """Initialize static analyzer."""
        self.tools_config = {
            'pylint': {
                'enabled': settings.PYLINT_ENABLED,
                'command': 'pylint',
                'args': ['--output-format=json', '--disable=C0114,C0116']
            },
            'eslint': {
                'enabled': settings.ESLINT_ENABLED,
                'command': 'eslint',
                'args': ['--format=json']
            },
            'bandit': {
                'enabled': settings.BANDIT_ENABLED,
                'command': 'bandit',
                'args': ['-f', 'json', '-r']
            }
        }
    
    def analyze_code(self, code: str, language: ProgrammingLanguage, file_name: Optional[str] = None) -> List[StaticAnalysisResult]:
        """
        Analyze code using appropriate static analysis tools.
        
        Args:
            code: The code to analyze
            language: Programming language
            file_name: Optional file name for context
            
        Returns:
            List of static analysis results from different tools
        """
        results = []
        
        # Create temporary file for analysis
        with tempfile.NamedTemporaryFile(mode='w', suffix=self._get_file_extension(language), delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Run appropriate tools based on language
            if language == ProgrammingLanguage.PYTHON:
                if self.tools_config['pylint']['enabled']:
                    results.append(self._run_pylint(temp_file_path))
                if self.tools_config['bandit']['enabled']:
                    results.append(self._run_bandit(temp_file_path))
            
            elif language in [ProgrammingLanguage.JAVASCRIPT, ProgrammingLanguage.TYPESCRIPT]:
                if self.tools_config['eslint']['enabled']:
                    results.append(self._run_eslint(temp_file_path))
            
            # Add more language-specific tools as needed
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
        
        return results
    
    def _get_file_extension(self, language: ProgrammingLanguage) -> str:
        """Get file extension for the given language."""
        extensions = {
            ProgrammingLanguage.PYTHON: '.py',
            ProgrammingLanguage.JAVASCRIPT: '.js',
            ProgrammingLanguage.TYPESCRIPT: '.ts',
            ProgrammingLanguage.JAVA: '.java',
            ProgrammingLanguage.CPP: '.cpp',
            ProgrammingLanguage.C: '.c',
            ProgrammingLanguage.GO: '.go',
            ProgrammingLanguage.RUST: '.rs',
            ProgrammingLanguage.PHP: '.php',
            ProgrammingLanguage.RUBY: '.rb'
        }
        return extensions.get(language, '.txt')
    
    def _run_pylint(self, file_path: str) -> StaticAnalysisResult:
        """Run Pylint analysis on Python code."""
        try:
            cmd = [self.tools_config['pylint']['command']] + self.tools_config['pylint']['args'] + [file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            issues = []
            score = 10.0
            
            if result.stdout:
                try:
                    pylint_data = json.loads(result.stdout)
                    for item in pylint_data:
                        issue = CodeIssue(
                            type=self._map_pylint_type(item.get('type', '')),
                            severity=self._map_pylint_severity(item.get('type', '')),
                            line=item.get('line'),
                            column=item.get('column'),
                            message=item.get('message', ''),
                            suggestion=item.get('message', ''),
                            rule_id=item.get('message-id', ''),
                            tool='pylint'
                        )
                        issues.append(issue)
                        
                        # Calculate score based on issues
                        if item.get('type') in ['error', 'fatal']:
                            score -= 2.0
                        elif item.get('type') == 'warning':
                            score -= 1.0
                        elif item.get('type') == 'refactor':
                            score -= 0.5
                
                except json.JSONDecodeError:
                    # Fallback parsing for non-JSON output
                    issues = self._parse_pylint_text_output(result.stdout)
            
            return StaticAnalysisResult(
                tool='pylint',
                issues=issues,
                score=max(0.0, score),
                summary=f"Pylint found {len(issues)} issues"
            )
            
        except subprocess.TimeoutExpired:
            logger.warning("Pylint analysis timed out")
            return StaticAnalysisResult(
                tool='pylint',
                issues=[],
                score=5.0,
                summary="Pylint analysis timed out"
            )
        except Exception as e:
            logger.error(f"Pylint analysis failed: {str(e)}")
            return StaticAnalysisResult(
                tool='pylint',
                issues=[],
                score=5.0,
                summary=f"Pylint analysis failed: {str(e)}"
            )
    
    def _run_eslint(self, file_path: str) -> StaticAnalysisResult:
        """Run ESLint analysis on JavaScript/TypeScript code."""
        try:
            cmd = [self.tools_config['eslint']['command']] + self.tools_config['eslint']['args'] + [file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            issues = []
            score = 10.0
            
            if result.stdout:
                try:
                    eslint_data = json.loads(result.stdout)
                    for file_data in eslint_data:
                        for message in file_data.get('messages', []):
                            issue = CodeIssue(
                                type=self._map_eslint_type(message.get('severity', 1)),
                                severity=self._map_eslint_severity(message.get('severity', 1)),
                                line=message.get('line'),
                                column=message.get('column'),
                                message=message.get('message', ''),
                                suggestion=message.get('message', ''),
                                rule_id=message.get('ruleId', ''),
                                tool='eslint'
                            )
                            issues.append(issue)
                            
                            # Calculate score based on severity
                            if message.get('severity') == 2:  # Error
                                score -= 2.0
                            elif message.get('severity') == 1:  # Warning
                                score -= 1.0
                
                except json.JSONDecodeError:
                    issues = self._parse_eslint_text_output(result.stdout)
            
            return StaticAnalysisResult(
                tool='eslint',
                issues=issues,
                score=max(0.0, score),
                summary=f"ESLint found {len(issues)} issues"
            )
            
        except subprocess.TimeoutExpired:
            logger.warning("ESLint analysis timed out")
            return StaticAnalysisResult(
                tool='eslint',
                issues=[],
                score=5.0,
                summary="ESLint analysis timed out"
            )
        except Exception as e:
            logger.error(f"ESLint analysis failed: {str(e)}")
            return StaticAnalysisResult(
                tool='eslint',
                issues=[],
                score=5.0,
                summary=f"ESLint analysis failed: {str(e)}"
            )
    
    def _run_bandit(self, file_path: str) -> StaticAnalysisResult:
        """Run Bandit security analysis on Python code."""
        try:
            cmd = [self.tools_config['bandit']['command']] + self.tools_config['bandit']['args'] + [file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            issues = []
            score = 10.0
            
            if result.stdout:
                try:
                    bandit_data = json.loads(result.stdout)
                    for item in bandit_data.get('results', []):
                        issue = CodeIssue(
                            type=IssueType.SECURITY_VULNERABILITY,
                            severity=self._map_bandit_severity(item.get('issue_severity', 'MEDIUM')),
                            line=item.get('line_number'),
                            message=item.get('issue_text', ''),
                            suggestion=item.get('issue_text', ''),
                            rule_id=item.get('test_id', ''),
                            tool='bandit'
                        )
                        issues.append(issue)
                        
                        # Calculate score based on severity
                        severity = item.get('issue_severity', 'MEDIUM')
                        if severity == 'HIGH':
                            score -= 3.0
                        elif severity == 'MEDIUM':
                            score -= 2.0
                        elif severity == 'LOW':
                            score -= 1.0
                
                except json.JSONDecodeError:
                    issues = self._parse_bandit_text_output(result.stdout)
            
            return StaticAnalysisResult(
                tool='bandit',
                issues=issues,
                score=max(0.0, score),
                summary=f"Bandit found {len(issues)} security issues"
            )
            
        except subprocess.TimeoutExpired:
            logger.warning("Bandit analysis timed out")
            return StaticAnalysisResult(
                tool='bandit',
                issues=[],
                score=5.0,
                summary="Bandit analysis timed out"
            )
        except Exception as e:
            logger.error(f"Bandit analysis failed: {str(e)}")
            return StaticAnalysisResult(
                tool='bandit',
                issues=[],
                score=5.0,
                summary=f"Bandit analysis failed: {str(e)}"
            )
    
    def _map_pylint_type(self, pylint_type: str) -> IssueType:
        """Map Pylint issue types to our IssueType enum."""
        mapping = {
            'error': IssueType.SYNTAX_ERROR,
            'fatal': IssueType.SYNTAX_ERROR,
            'warning': IssueType.STYLE_VIOLATION,
            'refactor': IssueType.MAINTAINABILITY_ISSUE,
            'convention': IssueType.STYLE_VIOLATION
        }
        return mapping.get(pylint_type, IssueType.STYLE_VIOLATION)
    
    def _map_pylint_severity(self, pylint_type: str) -> SeverityLevel:
        """Map Pylint issue types to severity levels."""
        mapping = {
            'error': SeverityLevel.HIGH,
            'fatal': SeverityLevel.CRITICAL,
            'warning': SeverityLevel.MEDIUM,
            'refactor': SeverityLevel.LOW,
            'convention': SeverityLevel.LOW
        }
        return mapping.get(pylint_type, SeverityLevel.MEDIUM)
    
    def _map_eslint_type(self, severity: int) -> IssueType:
        """Map ESLint severity to IssueType."""
        if severity == 2:  # Error
            return IssueType.SYNTAX_ERROR
        else:  # Warning
            return IssueType.STYLE_VIOLATION
    
    def _map_eslint_severity(self, severity: int) -> SeverityLevel:
        """Map ESLint severity to SeverityLevel."""
        if severity == 2:  # Error
            return SeverityLevel.HIGH
        else:  # Warning
            return SeverityLevel.MEDIUM
    
    def _map_bandit_severity(self, severity: str) -> SeverityLevel:
        """Map Bandit severity to SeverityLevel."""
        mapping = {
            'HIGH': SeverityLevel.CRITICAL,
            'MEDIUM': SeverityLevel.HIGH,
            'LOW': SeverityLevel.MEDIUM
        }
        return mapping.get(severity, SeverityLevel.MEDIUM)
    
    def _parse_pylint_text_output(self, output: str) -> List[CodeIssue]:
        """Parse Pylint text output when JSON parsing fails."""
        issues = []
        lines = output.split('\n')
        
        for line in lines:
            if ':' in line and any(keyword in line.lower() for keyword in ['error', 'warning', 'refactor']):
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    try:
                        line_num = int(parts[1])
                        issue_type = parts[2].strip()
                        message = parts[3].strip()
                        
                        issue = CodeIssue(
                            type=self._map_pylint_type(issue_type),
                            severity=self._map_pylint_severity(issue_type),
                            line=line_num,
                            message=message,
                            suggestion=message,
                            tool='pylint'
                        )
                        issues.append(issue)
                    except (ValueError, IndexError):
                        continue
        
        return issues
    
    def _parse_eslint_text_output(self, output: str) -> List[CodeIssue]:
        """Parse ESLint text output when JSON parsing fails."""
        issues = []
        lines = output.split('\n')
        
        for line in lines:
            if ':' in line and ('error' in line.lower() or 'warning' in line.lower()):
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    try:
                        line_num = int(parts[1])
                        message = parts[3].strip()
                        
                        issue = CodeIssue(
                            type=IssueType.STYLE_VIOLATION,
                            severity=SeverityLevel.MEDIUM,
                            line=line_num,
                            message=message,
                            suggestion=message,
                            tool='eslint'
                        )
                        issues.append(issue)
                    except (ValueError, IndexError):
                        continue
        
        return issues
    
    def _parse_bandit_text_output(self, output: str) -> List[CodeIssue]:
        """Parse Bandit text output when JSON parsing fails."""
        issues = []
        lines = output.split('\n')
        
        for line in lines:
            if '>> Issue:' in line:
                try:
                    # Extract issue information from Bandit text output
                    issue_text = line.split('>> Issue:')[1].strip()
                    
                    issue = CodeIssue(
                        type=IssueType.SECURITY_VULNERABILITY,
                        severity=SeverityLevel.MEDIUM,
                        message=issue_text,
                        suggestion=issue_text,
                        tool='bandit'
                    )
                    issues.append(issue)
                except IndexError:
                    continue
        
        return issues

# Global static analyzer instance
static_analyzer = StaticAnalyzer()

