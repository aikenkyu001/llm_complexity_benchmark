import pytest
from solution import Solution

def test_bitwise_and_basic():
    solution = Solution()
    assert solution.rangeBitwiseAnd(5, 7) == 4 # 101 & 110 & 111 = 100 (4)

def test_bitwise_and_zero():
    solution = Solution()
    assert solution.rangeBitwiseAnd(0, 1) == 0

def test_bitwise_and_large():
    solution = Solution()
    assert solution.rangeBitwiseAnd(1, 2147483647) == 0
