import pytest
from solution import Solution

def test_fractional_knapsack_basic():
    solution = Solution()
    items = [(60, 10), (100, 20), (120, 30)]
    capacity = 50
    # Items (val/weight): (6,10), (5,20), (4,30)
    # Take all of item1 (60) and item2 (100) and 2/3 of item3 (80) -> 240
    assert solution.fractionalKnapsack(items, capacity) == 240.0

def test_fractional_knapsack_empty():
    solution = Solution()
    assert solution.fractionalKnapsack([], 10) == 0.0
