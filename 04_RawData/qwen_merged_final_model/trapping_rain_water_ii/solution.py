# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def trapRainWaterII(self, heightMap: List[List[int]]) -> int:
        if not heightMap or not heightMap[0]:
            return 0
        
        rows, cols = len(heightMap), len(heightMap[0])
        visited = set()
        pq = []
        
        # Add all border cells to the priority queue
        for i in range(rows):
            heapq.heappush(pq, (heightMap[i][0], i, 0))
            heapq.heappush(pq, (heightMap[i][cols - 1], i, cols - 1))
            visited.add((i, 0))
            visited.add((i, cols - 1))
        for j in range(cols):
            heapq.heappush(pq, (heightMap[0][j], 0, j))
            heapq.heappush(pq, (heightMap[rows - 1][j], rows - 1, j))
            visited.add((0, j))
            visited.add((rows - 1, j))
        
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        total_water = 0
        
        while pq:
            height, x, y = heapq.heappop(pq)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_height = max(height, heightMap[nx][ny])
                    total_water += max(0, new_height - heightMap[nx][ny])
                    heapq.heappush(pq, (new_height, nx, ny))
        
        return total_water