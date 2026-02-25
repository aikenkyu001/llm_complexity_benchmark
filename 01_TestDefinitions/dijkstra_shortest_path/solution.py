# solution.py
from typing import List, Dict, Tuple
import heapq

class Solution:
    def dijkstra(self, graph: Dict[int, List[Tuple[int, float]]], start_node: int, n: int) -> List[float]:
        # Initialize distances with infinity
        distances = [float('inf')] * (n + 1)
        distances[start_node] = 0
        
        # Priority queue to store the nodes to be processed
        priority_queue = [(0, start_node)]
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            # Nodes can get added to the priority queue multiple times. We only
            # process a vertex the first time we remove it from the priority queue.
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in graph.get(current_node, []):
                distance = current_distance + weight
                
                # Only consider this new path if it's better
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # Return the distances from start_node to all other nodes
        return distances[1:]