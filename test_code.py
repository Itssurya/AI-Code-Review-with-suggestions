"""
Test file for AI Code Reviewer

This file contains various code issues and patterns that can be used
to test the AI Code Reviewer functionality.
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any

# Security issues
def insecure_function():
    """Function with security vulnerabilities."""
    password = "admin123"  # Hardcoded password
    eval("print('Hello')")  # Dangerous eval usage
    os.system("rm -rf /")  # Dangerous system call
    return password

# Performance issues
def inefficient_function(data: List[int]) -> List[int]:
    """Function with performance issues."""
    result = []
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] == data[j]:
                result.append(data[i])
    return result

# Style and maintainability issues
class BadClass:
    def __init__(self):
        self.x=1
        self.y=2
        self.z=3
    
    def method1(self):
        return self.x+self.y+self.z
    
    def method2(self):
        if True:
            return "always true"
        else:
            return "never reached"

# Logic errors
def buggy_function(x: int, y: int) -> int:
    """Function with logic errors."""
    if x > 0:
        return x + y
    elif x < 0:
        return x - y
    # Missing else case for x == 0

# Documentation issues
def undocumented_function(param1, param2):
    return param1 + param2

# Type hints missing
def no_type_hints(a, b, c):
    return a * b + c

# Unused imports
import math
import datetime
import random

# Long function (maintainability issue)
def very_long_function():
    """This function is too long and does too many things."""
    data = []
    for i in range(100):
        data.append(i)
    
    processed_data = []
    for item in data:
        if item % 2 == 0:
            processed_data.append(item * 2)
        else:
            processed_data.append(item)
    
    result = []
    for item in processed_data:
        if item > 50:
            result.append(item)
    
    final_result = []
    for item in result:
        final_result.append(item + 1)
    
    return final_result

# Global variables (bad practice)
global_var = "This is a global variable"

# Main execution
if __name__ == "__main__":
    # Test the functions
    print(insecure_function())
    print(inefficient_function([1, 2, 3, 4, 5]))
    print(buggy_function(0, 5))  # This will return None
    print(undocumented_function(1, 2))
    print(no_type_hints(1, 2, 3))
    print(very_long_function())

