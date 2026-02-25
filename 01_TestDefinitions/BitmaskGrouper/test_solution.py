import pytest
from solution import Solution

def test_bitmask_grouper_basic():
    solution = Solution()
    nums = [1, 2, 4, 8]
    # Bitwise AND of any two is 0. So 4 groups.
    result = solution.groupNums(nums)
    assert len(result) == 4

def test_bitmask_grouper_merge():
    solution = Solution()
    nums = [3, 1, 6, 2]
    # 3 & 1 = 1 (!= 0), 6 & 2 = 2 (!= 0)
    # Possible groups: [[3, 1], [6, 2]]
    result = solution.groupNums(nums)
    assert len(result) == 2
