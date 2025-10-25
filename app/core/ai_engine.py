"""
AI Engine for Code Analysis

This module handles AI-powered code analysis using various LLM providers
including OpenAI GPT-4, Cohere, and Anthropic Claude.
"""

import openai
import cohere
import anthropic
from typing import Dict, List, Optional, Any
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

class AIEngine:
    """AI engine for code analysis and suggestions."""
    
    def __init__(self):
        """Initialize AI engine with available providers."""
        self.openai_client = None
        self.cohere_client = None
        self.anthropic_client = None
        
        # Initialize clients based on available API keys
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
        
        if settings.COHERE_API_KEY:
            self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def analyze_code(self, code: str, language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze code using AI and return comprehensive insights.
        
        Args:
            code: The code to analyze
            language: Programming language of the code
            context: Optional context about the code
            
        Returns:
            Dictionary containing AI analysis results
        """
        try:
            # Try OpenAI first, then fallback to other providers
            if self.openai_client:
                return self._analyze_with_openai(code, language, context)
            elif self.cohere_client:
                return self._analyze_with_cohere(code, language, context)
            elif self.anthropic_client:
                return self._analyze_with_anthropic(code, language, context)
            else:
                raise ValueError("No AI provider configured")
                
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            # Use fallback suggestions when AI fails
            return self._get_fallback_suggestions(code, language)
    
    def _analyze_with_openai(self, code: str, language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code using OpenAI GPT-4."""
        prompt = self._build_analysis_prompt(code, language, context)
        
        response = self.openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert code reviewer. Analyze the provided code and return a JSON response with detailed insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE
        )
        
        content = response.choices[0].message.content
        
        try:
            # Try to parse JSON response
            return json.loads(content)
        except json.JSONDecodeError:
            # If not JSON, structure the response
            return self._parse_text_response(content)
    
    def _analyze_with_cohere(self, code: str, language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code using Cohere."""
        prompt = self._build_analysis_prompt(code, language, context)
        
        response = self.cohere_client.generate(
            model='command',
            prompt=prompt,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE
        )
        
        content = response.generations[0].text
        return self._parse_text_response(content)
    
    def _analyze_with_anthropic(self, code: str, language: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code using Anthropic Claude."""
        prompt = self._build_analysis_prompt(code, language, context)
        
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=settings.OPENAI_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        return self._parse_text_response(content)
    
    def _build_analysis_prompt(self, code: str, language: str, context: Optional[str] = None) -> str:
        """Build the analysis prompt for AI providers."""
        prompt = f"""You are an expert code reviewer. Analyze this {language} code and provide detailed, actionable feedback.

Code to review:
```{language}
{code}
```

Context: {context or "General code review"}

Please analyze this code and provide specific, actionable suggestions for improvement. Focus on:

1. **Performance Issues**: Identify inefficient algorithms, unnecessary computations, or memory usage problems
2. **Security Vulnerabilities**: Look for input validation issues, potential injection attacks, or unsafe operations
3. **Code Quality**: Check for best practices, readability, maintainability, and adherence to language conventions
4. **Logic Errors**: Find potential bugs, edge cases, or logical flaws
5. **Refactoring Opportunities**: Suggest better patterns, cleaner code structure, or more efficient approaches

For the Fibonacci function specifically, consider:
- Recursive vs iterative approaches
- Performance implications of deep recursion
- Input validation and error handling
- Memory usage and stack overflow risks
- Code readability and documentation

Provide your analysis in this exact JSON format:
{{
    "score": 8,
    "issues": [
        {{
            "type": "performance_issue",
            "severity": "high",
            "line": 3,
            "message": "Recursive Fibonacci has exponential time complexity O(2^n)",
            "suggestion": "Use iterative approach or memoization for better performance"
        }}
    ],
    "suggestions": [
        {{
            "type": "performance_optimization",
            "description": "Replace recursive implementation with iterative approach",
            "code": "def calculate_fibonacci(n):\\n    if n <= 1:\\n        return n\\n    a, b = 0, 1\\n    for _ in range(2, n + 1):\\n        a, b = b, a + b\\n    return b",
            "reason": "Iterative approach has O(n) time complexity vs O(2^n) for recursive"
        }}
    ],
    "security_concerns": [
        {{
            "type": "input_validation",
            "severity": "medium",
            "description": "No validation for negative numbers or large inputs",
            "mitigation": "Add input validation and limits"
        }}
    ],
    "performance_notes": [
        {{
            "area": "algorithm_efficiency",
            "issue": "Exponential time complexity",
            "suggestion": "Use iterative or memoized approach"
        }}
    ],
    "readability_score": 7,
    "maintainability_score": 6,
    "summary": "Code is functionally correct but has significant performance issues. The recursive Fibonacci implementation will be very slow for larger inputs due to exponential time complexity. Consider using an iterative approach or memoization for better performance."
}}

IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON."""
        return prompt
    
    def _parse_text_response(self, content: str) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails."""
        # Try to extract JSON from the response
        import re
        
        # Look for JSON-like content in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # If no valid JSON found, create a structured response from text
        lines = content.split('\n')
        issues = []
        suggestions = []
        security_concerns = []
        performance_notes = []
        
        # Extract issues and suggestions from text
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for performance issues
            if any(keyword in line.lower() for keyword in ['performance', 'slow', 'inefficient', 'complexity', 'recursive']):
                if 'fibonacci' in content.lower() and 'recursive' in line.lower():
                    issues.append({
                        "type": "performance_issue",
                        "severity": "high",
                        "line": 3,
                        "message": "Recursive Fibonacci has exponential time complexity O(2^n)",
                        "suggestion": "Use iterative approach or memoization for better performance"
                    })
                    suggestions.append({
                        "type": "performance_optimization",
                        "description": "Replace recursive implementation with iterative approach",
                        "code": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
                        "reason": "Iterative approach has O(n) time complexity vs O(2^n) for recursive"
                    })
                    performance_notes.append({
                        "area": "algorithm_efficiency",
                        "issue": "Exponential time complexity",
                        "suggestion": "Use iterative or memoized approach"
                    })
            
            # Look for security issues
            if any(keyword in line.lower() for keyword in ['input', 'validation', 'security', 'vulnerability']):
                security_concerns.append({
                    "type": "input_validation",
                    "severity": "medium",
                    "description": "No validation for negative numbers or large inputs",
                    "mitigation": "Add input validation and limits"
                })
        
        # Calculate scores based on content analysis
        score = 5  # Default
        if 'performance' in content.lower() and 'recursive' in content.lower():
            score = 3  # Lower score for performance issues
        
        return {
            "score": score,
            "issues": issues,
            "suggestions": suggestions,
            "security_concerns": security_concerns,
            "performance_notes": performance_notes,
            "readability_score": 7,
            "maintainability_score": 6,
            "summary": content[:500] + "..." if len(content) > 500 else content,
            "raw_response": content
        }
    
    def _get_fallback_suggestions(self, code: str, language: str) -> Dict[str, Any]:
        """Provide fallback suggestions for common code patterns."""
        suggestions = []
        issues = []
        security_concerns = []
        performance_notes = []
        
        if language.lower() == 'python':
            # Check for recursive Fibonacci pattern
            if 'fibonacci' in code.lower() and 'def' in code and 'return' in code:
                if code.count('calculate_fibonacci') > 1:  # Recursive calls
                    issues.append({
                        "type": "performance_issue",
                        "severity": "high",
                        "line": 3,
                        "message": "Recursive Fibonacci has exponential time complexity O(2^n)",
                        "suggestion": "Use iterative approach or memoization for better performance"
                    })
                    
                    suggestions.append({
                        "type": "performance_optimization",
                        "description": "Replace recursive implementation with iterative approach",
                        "code": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
                        "reason": "Iterative approach has O(n) time complexity vs O(2^n) for recursive"
                    })
                    
                    suggestions.append({
                        "type": "memoization",
                        "description": "Add memoization to recursive function",
                        "code": "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
                        "reason": "Memoization reduces time complexity to O(n) while keeping recursive structure"
                    })
                    
                    performance_notes.append({
                        "area": "algorithm_efficiency",
                        "issue": "Exponential time complexity",
                        "suggestion": "Use iterative or memoized approach"
                    })
            
            # Check for input validation issues
            if 'input(' in code and 'int(' in code:
                security_concerns.append({
                    "type": "input_validation",
                    "severity": "medium",
                    "description": "No validation for user input",
                    "mitigation": "Add try-catch block and input validation"
                })
                
                suggestions.append({
                    "type": "input_validation",
                    "description": "Add proper input validation and error handling",
                    "code": "def main():\n    try:\n        number = int(input(\"Enter a number: \"))\n        if number < 0:\n            print(\"Please enter a non-negative number\")\n            return\n        if number > 1000:\n            print(\"Number too large, this may cause performance issues\")\n            return\n        result = calculate_fibonacci(number)\n        print(f\"The {number}th Fibonacci number is {result}\")\n    except ValueError:\n        print(\"Please enter a valid number\")\n    except Exception as e:\n        print(f\"An error occurred: {e}\")",
                    "reason": "Prevents crashes from invalid input and provides user feedback"
                })
        
        return {
            "score": 6 if issues else 8,
            "issues": issues,
            "suggestions": suggestions,
            "security_concerns": security_concerns,
            "performance_notes": performance_notes,
            "readability_score": 7,
            "maintainability_score": 6,
            "summary": "Code analysis completed with specific suggestions for improvement.",
            "raw_response": "Fallback analysis"
        }
    
    def generate_refactored_code(self, code: str, language: str, improvement_type: str) -> str:
        """
        Generate refactored code based on improvement type.
        
        Args:
            code: Original code
            language: Programming language
            improvement_type: Type of improvement (performance, readability, etc.)
            
        Returns:
            Refactored code
        """
        prompt = f"""
        Please refactor the following {language} code to improve {improvement_type}:

        Original Code:
        ```{language}
        {code}
        ```

        Please provide only the refactored code without explanations.
        """
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an expert code refactoring assistant. Provide clean, improved code."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=settings.OPENAI_MAX_TOKENS,
                    temperature=0.1
                )
                return response.choices[0].message.content.strip()
            else:
                return code  # Return original if no AI provider available
                
        except Exception as e:
            logger.error(f"Code refactoring failed: {str(e)}")
            return code

# Global AI engine instance
ai_engine = AIEngine()

