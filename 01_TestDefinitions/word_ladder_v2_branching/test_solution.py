import pytest
from solution import Solution

def test_word_ladder_v2_basic():
    solution = Solution()
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log","cog"]
    assert solution.ladderLength(beginWord, endWord, wordList) == 5

def test_word_ladder_v2_long():
    solution = Solution()
    beginWord = "aaaaa"
    endWord = "bbbbb"
    wordList = ["aaaab","aaabb","aabbb","abbbb","bbbbb"]
    assert solution.ladderLength(beginWord, endWord, wordList) == 6
