"""
Utility Functions for Code Processing

This module contains helper functions for code processing,
file handling, and common operations used throughout the application.
"""

import re
import hashlib
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CodeUtils:
    """Utility class for code processing operations."""
    
    @staticmethod
    def detect_language_from_filename(filename: str) -> Optional[str]:
        """
        Detect programming language from file extension.
        
        Args:
            filename: Name of the file
            
        Returns:
            Programming language string or None
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'objective-c',
            '.mm': 'objective-cpp',
            '.cs': 'csharp',
            '.vb': 'vbnet',
            '.pl': 'perl',
            '.sh': 'bash',
            '.ps1': 'powershell',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.less': 'less',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.conf': 'ini'
        }
        
        if not filename:
            return None
        
        # Extract extension
        if '.' in filename:
            extension = '.' + filename.split('.')[-1].lower()
            return extension_map.get(extension)
        
        return None
    
    @staticmethod
    def extract_code_metrics(code: str) -> Dict[str, Any]:
        """
        Extract basic metrics from code.
        
        Args:
            code: Source code string
            
        Returns:
            Dictionary with code metrics
        """
        lines = code.split('\n')
        
        metrics = {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#') or line.strip().startswith('//')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'max_line_length': max(len(line) for line in lines) if lines else 0,
            'average_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0,
            'cyclomatic_complexity': CodeUtils._calculate_complexity(code),
            'function_count': CodeUtils._count_functions(code),
            'class_count': CodeUtils._count_classes(code),
            'import_count': CodeUtils._count_imports(code)
        }
        
        return metrics
    
    @staticmethod
    def _calculate_complexity(code: str) -> int:
        """Calculate cyclomatic complexity."""
        complexity_keywords = [
            'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally',
            'and', 'or', 'case', 'when', 'switch', 'catch', '&&', '||'
        ]
        
        complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            # Count occurrences of complexity keywords
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, code, re.IGNORECASE)
            complexity += len(matches)
        
        return complexity
    
    @staticmethod
    def _count_functions(code: str) -> int:
        """Count function definitions."""
        function_patterns = [
            r'def\s+\w+\s*\(',  # Python
            r'function\s+\w+\s*\(',  # JavaScript
            r'\w+\s*:\s*function\s*\(',  # JavaScript
            r'public\s+\w+\s+\w+\s*\(',  # Java
            r'private\s+\w+\s+\w+\s*\(',  # Java
            r'protected\s+\w+\s+\w+\s*\(',  # Java
            r'fn\s+\w+\s*\(',  # Rust
            r'func\s+\w+\s*\(',  # Go
        ]
        
        count = 0
        for pattern in function_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            count += len(matches)
        
        return count
    
    @staticmethod
    def _count_classes(code: str) -> int:
        """Count class definitions."""
        class_patterns = [
            r'class\s+\w+',  # Python, Java, C++, etc.
            r'interface\s+\w+',  # Java, TypeScript
            r'struct\s+\w+',  # C, C++, Rust
            r'enum\s+\w+',  # Various languages
        ]
        
        count = 0
        for pattern in class_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            count += len(matches)
        
        return count
    
    @staticmethod
    def _count_imports(code: str) -> int:
        """Count import statements."""
        import_patterns = [
            r'import\s+',  # Python, JavaScript, Java
            r'from\s+\w+\s+import',  # Python
            r'require\s*\(',  # Node.js
            r'#include\s*<',  # C/C++
            r'#include\s*"',  # C/C++
            r'using\s+',  # C#
        ]
        
        count = 0
        for pattern in import_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            count += len(matches)
        
        return count
    
    @staticmethod
    def generate_review_id() -> str:
        """Generate a unique review ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def calculate_code_hash(code: str) -> str:
        """Calculate SHA-256 hash of code for deduplication."""
        return hashlib.sha256(code.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sanitize_code(code: str) -> str:
        """
        Sanitize code by removing sensitive information.
        
        Args:
            code: Source code
            
        Returns:
            Sanitized code
        """
        # Remove potential API keys, passwords, etc.
        sensitive_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'key\s*=\s*["\'][^"\']+["\']',
        ]
        
        sanitized_code = code
        for pattern in sensitive_patterns:
            sanitized_code = re.sub(pattern, '***REDACTED***', sanitized_code, flags=re.IGNORECASE)
        
        return sanitized_code
    
    @staticmethod
    def extract_functions_and_classes(code: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract function and class definitions from code.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            List of extracted functions and classes
        """
        extracted = []
        
        if language.lower() == 'python':
            # Extract Python functions and classes
            function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
            class_pattern = r'class\s+(\w+)(?:\([^)]*\))?:'
            
            for match in re.finditer(function_pattern, code):
                extracted.append({
                    'type': 'function',
                    'name': match.group(1),
                    'line': code[:match.start()].count('\n') + 1,
                    'signature': match.group(0)
                })
            
            for match in re.finditer(class_pattern, code):
                extracted.append({
                    'type': 'class',
                    'name': match.group(1),
                    'line': code[:match.start()].count('\n') + 1,
                    'signature': match.group(0)
                })
        
        elif language.lower() in ['javascript', 'typescript']:
            # Extract JavaScript/TypeScript functions and classes
            function_patterns = [
                r'function\s+(\w+)\s*\(',
                r'(\w+)\s*:\s*function\s*\(',
                r'(\w+)\s*\([^)]*\)\s*=>',
                r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
            ]
            
            class_pattern = r'class\s+(\w+)'
            
            for pattern in function_patterns:
                for match in re.finditer(pattern, code):
                    extracted.append({
                        'type': 'function',
                        'name': match.group(1),
                        'line': code[:match.start()].count('\n') + 1,
                        'signature': match.group(0)
                    })
            
            for match in re.finditer(class_pattern, code):
                extracted.append({
                    'type': 'class',
                    'name': match.group(1),
                    'line': code[:match.start()].count('\n') + 1,
                    'signature': match.group(0)
                })
        
        return extracted
    
    @staticmethod
    def format_code_score(score: float) -> str:
        """Format code score with appropriate rating."""
        if score >= 9.0:
            return "Excellent"
        elif score >= 7.0:
            return "Good"
        elif score >= 5.0:
            return "Fair"
        elif score >= 3.0:
            return "Poor"
        else:
            return "Critical"
    
    @staticmethod
    def calculate_overall_score(static_scores: List[float], ai_score: float) -> float:
        """
        Calculate overall score from static analysis and AI scores.
        
        Args:
            static_scores: List of scores from static analysis tools
            ai_score: Score from AI analysis
            
        Returns:
            Overall weighted score
        """
        if not static_scores and ai_score == 0:
            return 5.0  # Default score
        
        # Weight static analysis 60% and AI analysis 40%
        static_avg = sum(static_scores) / len(static_scores) if static_scores else 5.0
        overall_score = (static_avg * 0.6) + (ai_score * 0.4)
        
        return round(overall_score, 2)
    
    @staticmethod
    def group_issues_by_type(issues: List[Any]) -> Dict[str, List[Any]]:
        """Group issues by their type."""
        grouped = {}
        for issue in issues:
            issue_type = getattr(issue, 'type', 'unknown')
            if issue_type not in grouped:
                grouped[issue_type] = []
            grouped[issue_type].append(issue)
        
        return grouped
    
    @staticmethod
    def generate_summary(issues: List[Any], suggestions: List[Any], score: float) -> str:
        """Generate a summary of the code review."""
        total_issues = len(issues)
        critical_issues = len([i for i in issues if getattr(i, 'severity', '') == 'critical'])
        high_issues = len([i for i in issues if getattr(i, 'severity', '') == 'high'])
        
        summary_parts = []
        
        if score >= 8.0:
            summary_parts.append("Code quality is excellent")
        elif score >= 6.0:
            summary_parts.append("Code quality is good with minor improvements needed")
        elif score >= 4.0:
            summary_parts.append("Code quality needs improvement")
        else:
            summary_parts.append("Code quality requires significant attention")
        
        if total_issues > 0:
            summary_parts.append(f"Found {total_issues} issues")
            if critical_issues > 0:
                summary_parts.append(f"including {critical_issues} critical issues")
            elif high_issues > 0:
                summary_parts.append(f"including {high_issues} high-priority issues")
        
        if suggestions:
            summary_parts.append(f"Generated {len(suggestions)} improvement suggestions")
        
        return ". ".join(summary_parts) + "."

# Global utility instance
code_utils = CodeUtils()

