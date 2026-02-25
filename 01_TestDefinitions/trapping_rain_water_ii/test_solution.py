import pytest
from solution import Solution

def test_trapping_ii_basic():
    solution = Solution()
    heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]
    assert solution.trapRainWater(heightMap) == 4

def test_trapping_ii_flat():
    solution = Solution()
    heightMap = [[1,1,1],[1,1,1],[1,1,1]]
    assert solution.trapRainWater(heightMap) == 0
