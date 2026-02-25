from typing import List

class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = [0] * (n + 1)
        candidate1 = None
        candidate2 = None
        
        # Step 1: Find the node with two parents
        for u, v in edges:
            if parent[v] != 0:
                candidate1 = [parent[v], v]
                candidate2 = [u, v]
                parent[v] = -1  # Mark this edge as invalid temporarily
            else:
                parent[v] = u
        
        # Step 2: Find the cycle using union-find
        def find(x):
            if x != root[x]:
                root[x] = find(root[x])
            return root[x]
        
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return False
            root[rx] = ry
            return True
        
        # Initialize union-find structure
        root = list(range(n + 1))
        
        for u, v in edges:
            if u == candidate2[0] and v == candidate2[1]:
                continue  # Skip the invalid edge temporarily
            if not union(u, v):
                return [u, v]
        
        # If no cycle is found, return the first candidate
        return candidate1 if candidate1 else []