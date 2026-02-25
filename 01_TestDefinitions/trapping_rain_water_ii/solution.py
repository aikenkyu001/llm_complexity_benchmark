from typing import List

class Solution:
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        if not heightMap or not heightMap[0]:
            return 0
        
        m, n = len(heightMap), len(heightMap[0])
        if m < 3 or n < 3:
            return 0
        
        # Initialize a min-heap to store the boundary cells
        heap = []
        visited = set()
        
        # Add all boundary cells to the heap and mark them as visited
        for i in range(m):
            heapq.heappush(heap, (heightMap[i][0], i, 0))
            heapq.heappush(heap, (heightMap[i][n-1], i, n-1))
            visited.add((i, 0))
            visited.add((i, n-1))
        
        for j in range(n):
            heapq.heappush(heap, (heightMap[0][j], 0, j))
            heapq.heappush(heap, (heightMap[m-1][j], m-1, j))
            visited.add((0, j))
            visited.add((m-1, j))
        
        # Initialize the amount of water trapped
        water_trapped = 0
        
        # Process the heap until it's empty
        while heap:
            height, x, y = heapq.heappop(heap)
            
            # Check all four possible directions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visited:
                    # Calculate the water trapped at this cell
                    water_trapped += max(0, height - heightMap[nx][ny])
                    
                    # Push the new cell to the heap with the updated height
                    heapq.heappush(heap, (max(height, heightMap[nx][ny]), nx, ny))
                    
                    # Mark the cell as visited
                    visited.add((nx, ny))
        
        return water_trapped