import pytest
from solution import Solution

def test_sparse_matrix_basic():
    solution = Solution()
    mat1 = [[1,0,0],[-1,0,3]]
    mat2 = [[7,0,0],[0,0,0],[0,0,1]]
    expected = [[7,0,0],[-7,0,3]]
    assert solution.multiply(mat1, mat2) == expected

def test_sparse_matrix_zero():
    solution = Solution()
    mat1 = [[0]]
    mat2 = [[0]]
    assert solution.multiply(mat1, mat2) == [[0]]
