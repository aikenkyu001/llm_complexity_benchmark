# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def primMST(self, graph: Dict[int, List[tuple]], n: int) -> int:
        # Initialize the priority queue with the first node and its neighbors
        pq = []
        for neighbor, weight in graph[0]:
            heapq.heappush(pq, (weight, neighbor))
        
        # Initialize the visited set and the total weight
        visited = {0}
        total_weight = 0
        
        # Continue until all nodes are visited
        while pq:
            weight, node = heapq.heappop(pq)
            
            # If the node has already been visited, skip it
            if node in visited:
                continue
            
            # Mark the node as visited
            visited.add(node)
            
            # Add the weight of the edge to the total weight
            total_weight += weight
            
            # Add the neighbors of the current node to the priority queue
            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (weight, neighbor))
        
        # Return the total weight of the MST
        return total_weight