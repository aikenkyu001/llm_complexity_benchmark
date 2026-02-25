import pytest
from solution import Solution

def test_regex_basic():
    solution = Solution()
    assert solution.isMatch("aa", "a") == False
    assert solution.isMatch("aa", "a*") == True
    assert solution.isMatch("ab", ".*") == True

def test_regex_complex():
    solution = Solution()
    assert solution.isMatch("aab", "c*a*b") == True
    assert solution.isMatch("mississippi", "mis*is*p*.") == False
