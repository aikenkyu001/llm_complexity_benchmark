# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        
        # Helper function to find the parent of a node
        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        # Helper function to union two sets
        def union(x: int, y: int) -> bool:
            root_x = find(x)
            root_y = find(y)
            if root_x == root_y:
                return False
            parent[root_x] = root_y
            return True
        
        # Initialize parent array
        parent = list(range(n + 1))
        
        # Find cycles and potential duplicate edges
        cycle_edges = []
        duplicate_edge = None
        for u, v in edges:
            if find(u) == find(v):
                cycle_edges.append((u, v))
            elif union(u, v):
                duplicate_edge = (u, v)
        
        # If no cycle, return the duplicate edge
        if not cycle_edges:
            return duplicate_edge
        
        # If there is a cycle, return the last occurrence of the cycle edge
        return cycle_edges[-1]