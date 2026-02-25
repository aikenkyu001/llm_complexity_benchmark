import pytest
from solution import Solution

def test_matrix_chain_basic():
    solution = Solution()
    # Matrices: 10x30, 30x5, 5x60
    p = [10, 30, 5, 60]
    # (10*30*5) + (10*5*60) = 1500 + 3000 = 4500
    assert solution.matrixChainOrder(p) == 4500

def test_matrix_chain_longer():
    solution = Solution()
    p = [40, 20, 30, 10, 30]
    # Optimal: (40*20*30) + (40*30*10) + (40*10*30) = 24000+12000+12000 = 48000
    # or others... minimum is 26000
    assert solution.matrixChainOrder(p) == 26000
