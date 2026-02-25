import pytest
from solution import Solution

def test_nesting_true():
    sol = Solution()
    assert sol.checkNested(1, 1, 1, 1, 1) == True

def test_nesting_false():
    sol = Solution()
    assert sol.checkNested(1, 1, 1, 1, 0) == False
