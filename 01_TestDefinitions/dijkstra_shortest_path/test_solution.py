import pytest
from solution import Solution

def test_dijkstra_basic():
    solution = Solution()
    # graph[u] = [(v, weight), ...]
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    result = solution.dijkstra(graph, 0, 4)
    assert result == [0, 3, 1, 4] # distances to 0, 1, 2, 3

def test_dijkstra_unreachable():
    solution = Solution()
    graph = {0: [(1, 2)], 1: [], 2: []}
    result = solution.dijkstra(graph, 0, 3)
    assert result[0] == 0
    assert result[1] == 2
    assert result[2] == float('inf')
