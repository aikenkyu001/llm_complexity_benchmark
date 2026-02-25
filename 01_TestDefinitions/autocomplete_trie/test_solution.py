import pytest
from solution import Solution

def test_autocomplete_basic():
    sentences = ["i love you", "island", "ironman", "i love leetcode"]
    times = [5, 3, 2, 2]
    # In a real scenario, this might be a class. Let's assume a class AutocompleteSystem.
    # For this task, we will simplify it to a method.
    solution = Solution()
    solution.initAutocomplete(sentences, times)
    
    assert solution.query("i") == ["i love you", "island", "i love leetcode"]
    assert solution.query("i love ") == ["i love you", "i love leetcode"]
    assert solution.query("i love you ") == []
