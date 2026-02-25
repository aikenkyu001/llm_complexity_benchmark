import pytest
from solution import Solution

def test_word_break_v2_basic():
    solution = Solution()
    assert solution.wordBreak("leetcode", ["leet", "code"]) == True

def test_word_break_v2_complex():
    solution = Solution()
    assert solution.wordBreak("applepenapple", ["apple", "pen"]) == True
