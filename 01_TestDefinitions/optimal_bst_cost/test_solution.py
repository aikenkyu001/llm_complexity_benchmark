import pytest
from solution import Solution

def test_optimal_bst_basic():
    solution = Solution()
    keys = [10, 12, 20]
    freq = [34, 8, 50]
    # Optimal cost is 142
    assert solution.optimalBST(keys, freq) == 142

def test_optimal_bst_simple():
    solution = Solution()
    keys = [10, 12]
    freq = [3, 4]
    # Root 12: 4*1 + 3*2 = 10
    # Root 10: 3*1 + 4*2 = 11
    assert solution.optimalBST(keys, freq) == 10
