import pytest
from solution import Solution

def test_boggle_basic():
    solution = Solution()
    board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    words = ["oath","pea","eat","rain"]
    result = solution.findWords(board, words)
    assert sorted(result) == sorted(["eat","oath"])

def test_boggle_none():
    solution = Solution()
    board = [["a","b"],["c","d"]]
    words = ["abcd"]
    assert solution.findWords(board, words) == []

def test_boggle_overlap():
    solution = Solution()
    board = [["a","b"],["a","a"]]
    words = ["aba","baa","aaa","ab"]
    result = solution.findWords(board, words)
    assert sorted(result) == sorted(["aaa","aba","baa", "ab"])
