import pytest
from solution import Solution

def test_lcs_basic():
    solution = Solution()
    assert solution.longestCommonSubsequence("abcde", "ace") == 3

def test_lcs_identical():
    solution = Solution()
    assert solution.longestCommonSubsequence("abc", "abc") == 3

def test_lcs_no_common():
    solution = Solution()
    assert solution.longestCommonSubsequence("abc", "def") == 0

def test_lcs_partial():
    solution = Solution()
    assert solution.longestCommonSubsequence("ezupkr", "ubmrapg") == 2 # "u", "r"

def test_lcs_empty():
    solution = Solution()
    assert solution.longestCommonSubsequence("", "abc") == 0
