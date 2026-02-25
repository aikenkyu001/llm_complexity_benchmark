class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        # Initialize an n x n matrix with zeros
        matrix = [[0] * n for _ in range(n)]
        
        # Define the directions for moving right, down, left, and up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_index = 0
        
        # Start from the top-left corner of the matrix
        row, col = 0, 0
        
        for num in range(1, n * n + 1):
            # Place the current number in the matrix
            matrix[row][col] = num
            
            # Calculate the next position based on the current direction
            next_row = row + directions[direction_index][0]
            next_col = col + directions[direction_index][1]
            
            # Check if the next position is out of bounds or already filled
            if (next_row < 0 or next_row >= n or 
                next_col < 0 or next_col >= n or 
                matrix[next_row][next_col] != 0):
                # Change direction to the next one in the list
                direction_index = (direction_index + 1) % 4
                next_row = row + directions[direction_index][0]
                next_col = col + directions[direction_index][1]
            
            # Move to the next position
            row, col = next_row, next_col
        
        return matrix