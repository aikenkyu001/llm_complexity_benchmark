import pytest
from solution import Solution

def test_permutations_basic():
    solution = Solution()
    nums = [1, 1, 2]
    expected = [[1,1,2],[1,2,1],[2,1,1]]
    result = solution.permuteUnique(nums)
    assert sorted(result) == sorted(expected)

def test_permutations_single():
    solution = Solution()
    assert solution.permuteUnique([1]) == [[1]]
