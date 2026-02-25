from typing import List, Optional, Dict, Set, Any
import heapq
import collections

class Solution:
    def primMST(self, graph: Dict[int, List[tuple]], n: int) -> int:
        if not graph or n <= 0:
            return 0
        
        # Priority queue to store edges with their weights
        pq = []
        # Set to keep track of visited nodes
        visited = set()
        # Start from node 0
        start_node = 0
        # Add all edges from the starting node to the priority queue
        for neighbor, weight in graph.get(start_node, []):
            heapq.heappush(pq, (weight, start_node, neighbor))
        
        mst_weight = 0
        visited.add(start_node)
        
        while pq:
            weight, u, v = heapq.heappop(pq)
            
            # If the destination node has not been visited, add it to the MST
            if v not in visited:
                mst_weight += weight
                visited.add(v)
                
                # Add all edges from the newly added node to the priority queue
                for neighbor, weight in graph.get(v, []):
                    if neighbor not in visited:
                        heapq.heappush(pq, (weight, v, neighbor))
        
        # If we have visited all nodes, return the MST weight
        if len(visited) == n:
            return mst_weight
        
        # If the graph is not fully connected, return 0
        return 0