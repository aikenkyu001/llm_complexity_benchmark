import pytest
from solution import Solution

def test_word_ladder_basic():
    """
    Test a basic case where a path exists.
    """
    solution = Solution()
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log","cog"]
    expected = 5
    assert solution.ladderLength(beginWord, endWord, wordList) == expected

def test_word_ladder_no_path():
    """
    Test a case where no path exists.
    """
    solution = Solution()
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log"]
    expected = 0
    assert solution.ladderLength(beginWord, endWord, wordList) == expected

def test_word_ladder_same_word():
    """
    Test a case where begin and end words are the same.
    """
    solution = Solution()
    beginWord = "hit"
    endWord = "hit"
    wordList = ["hot","dot","dog","lot","log","cog"]
    expected = 1
    assert solution.ladderLength(beginWord, endWord, wordList) == expected

def test_word_ladder_short_list():
    """
    Test with a shorter word list.
    """
    solution = Solution()
    beginWord = "a"
    endWord = "c"
    wordList = ["a","b","c"]
    expected = 2
    assert solution.ladderLength(beginWord, endWord, wordList) == expected

def test_word_ladder_not_in_list():
    """
    Test case where endWord is not in the wordList.
    It should still work if a transformation sequence is possible.
    The problem statement implies endWord must be in the list for a successful transformation.
    Let's assume the provided solution code will handle this gracefully.
    If ladderLength returns 0, it means no path was found, which is correct.
    """
    solution = Solution()
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log"] # "cog" is missing
    expected = 0 # No path to "cog"
    assert solution.ladderLength(beginWord, endWord, wordList) == expected
