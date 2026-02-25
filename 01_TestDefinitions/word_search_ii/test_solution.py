import pytest
from solution import Solution

def test_word_search_ii_basic():
    solution = Solution()
    board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    words = ["oath","pea","eat","rain"]
    assert sorted(solution.findWords(board, words)) == sorted(["eat","oath"])

def test_word_search_ii_empty():
    solution = Solution()
    assert solution.findWords([["a"]], ["b"]) == []
