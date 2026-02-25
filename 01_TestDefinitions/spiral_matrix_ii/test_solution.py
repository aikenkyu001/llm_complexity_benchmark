import pytest
from solution import Solution

def test_spiral_ii_basic():
    solution = Solution()
    assert solution.generateMatrix(3) == [[1,2,3],[8,9,4],[7,6,5]]

def test_spiral_ii_one():
    solution = Solution()
    assert solution.generateMatrix(1) == [[1]]
