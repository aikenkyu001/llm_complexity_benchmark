import pytest
from solution import Solution

def test_redundant_ii_cycle():
    solution = Solution()
    edges = [[1,2], [1,3], [2,3]]
    assert solution.findRedundantDirectedConnection(edges) == [2,3]

def test_redundant_ii_complex():
    solution = Solution()
    edges = [[1,2], [2,3], [3,4], [4,1], [1,5]]
    assert solution.findRedundantDirectedConnection(edges) == [4,1]

def test_redundant_ii_two_parents():
    solution = Solution()
    edges = [[2,1], [3,1], [4,2], [1,4]]
    assert solution.findRedundantDirectedConnection(edges) == [2,1]
