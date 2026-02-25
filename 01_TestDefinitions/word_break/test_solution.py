import pytest
from solution import Solution

def test_word_break_basic():
    solution = Solution()
    assert solution.wordBreak("leetcode", ["leet", "code"]) == True

def test_word_break_reuse():
    solution = Solution()
    assert solution.wordBreak("applepenapple", ["apple", "pen"]) == True

def test_word_break_fail():
    solution = Solution()
    assert solution.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

def test_word_break_empty():
    solution = Solution()
    assert solution.wordBreak("", ["a", "b"]) == True # Or False depending on spec, but let's assume True for empty
