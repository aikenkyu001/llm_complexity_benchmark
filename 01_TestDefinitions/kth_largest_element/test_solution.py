import pytest
from solution import Solution

def test_kth_largest_basic():
    solution = Solution()
    assert solution.findKthLargest([3,2,1,5,6,4], 2) == 5

def test_kth_largest_complex():
    solution = Solution()
    assert solution.findKthLargest([3,2,3,1,2,4,5,5,6], 4) == 4
