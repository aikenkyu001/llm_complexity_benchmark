import pytest
from solution import Solution

def test_prim_basic():
    solution = Solution()
    # graph[u] = [(v, weight), ...]
    graph = {
        0: [(1, 2), (3, 6)],
        1: [(0, 2), (2, 3), (3, 8), (4, 5)],
        2: [(1, 3), (4, 7)],
        3: [(0, 6), (1, 8), (4, 9)],
        4: [(1, 5), (2, 7), (3, 9)]
    }
    # MST Edges: (0,1,2), (1,2,3), (1,4,5), (0,3,6) -> Sum = 16
    assert solution.primMST(graph, 5) == 16

def test_prim_simple():
    solution = Solution()
    graph = {
        0: [(1, 10)],
        1: [(0, 10)]
    }
    assert solution.primMST(graph, 2) == 10
