# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def dijkstra(self, graph: Dict[int, List[tuple]], start_node: int, n: int) -> List[float]:
        # Initialize the priority queue with the start node and its distance
        pq = [(0, start_node)]
        # Dictionary to store the shortest distance to each node
        dist = {node: float('inf') for node in range(1, n + 1)}
        dist[start_node] = 0
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            
            # If the current distance is greater than the stored distance, skip this node
            if current_dist > dist[current_node]:
                continue
            
            # Explore neighbors
            for neighbor, weight in graph[current_node]:
                new_dist = current_dist + weight
                
                # If a shorter path is found, update the distance and push it into the priority queue
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # Return the list of shortest distances
        return [dist[node] for node in range(1, n + 1)]