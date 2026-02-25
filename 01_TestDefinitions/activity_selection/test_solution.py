import pytest
from solution import Solution

def test_activity_selection_basic():
    solution = Solution()
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
    # Max activities: (1,4), (5,7), (8,11), (12,14) -> 4
    assert solution.maxActivities(activities) == 4

def test_activity_selection_sorted():
    solution = Solution()
    activities = [(1, 2), (2, 3), (3, 4)]
    assert solution.maxActivities(activities) == 3
