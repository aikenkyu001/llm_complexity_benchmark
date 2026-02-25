import pytest
from solution import Solution

def test_interval_merge_basic():
    solution = Solution()
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    assert solution.merge(intervals) == [[1,6],[8,10],[15,18]]

def test_interval_merge_overlap():
    solution = Solution()
    intervals = [[1,4],[4,5]]
    assert solution.merge(intervals) == [[1,5]]

def test_interval_merge_empty():
    solution = Solution()
    assert solution.merge([]) == []
