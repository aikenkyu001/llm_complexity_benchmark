import pytest
from solution import Solution

def test_valid_parentheses_basic():
    solution = Solution()
    assert solution.isValid("()") == True
    assert solution.isValid("()[]{}") == True
    assert solution.isValid("(]") == False

def test_valid_parentheses_nested():
    solution = Solution()
    assert solution.isValid("([{}])") == True
    assert solution.isValid("(((((())))))") == True

def test_valid_parentheses_complex_fail():
    solution = Solution()
    assert solution.isValid("({[)]})") == False
