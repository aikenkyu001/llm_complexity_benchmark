from typing import Tuple
import heapq

class Solution:
    def find_min_cost(self, start: Tuple[int, int], target: Tuple[int, int]) -> int:
        # Directions for moving right or down
        directions = [(1, 0), (0, 1)]
        
        # Priority queue to store (total_cost, x, y)
        pq = []
        heapq.heappush(pq, (0, start[0], start[1]))
        
        # Dictionary to track the minimum cost to reach each cell
        min_cost: Dict[Tuple[int, int], int] = {}
        min_cost[start] = 0
        
        while pq:
            total_cost, x, y = heapq.heappop(pq)
            
            # If we reached the target, return the total cost
            if (x, y) == target:
                return total_cost
            
            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Check bounds
                if 0 <= nx <= 100 and 0 <= ny <= 100:
                    # Calculate the cost to move to the neighbor
                    move_cost = (nx + ny) % 5 + 1
                    new_total_cost = total_cost + move_cost
                    
                    # If we find a cheaper path to this neighbor, update it
                    if (nx, ny) not in min_cost or new_total_cost < min_cost[(nx, ny)]:
                        min_cost[(nx, ny)] = new_total_cost
                        heapq.heappush(pq, (new_total_cost, nx, ny))
        
        # If no path exists to the target, return -1
        return -1