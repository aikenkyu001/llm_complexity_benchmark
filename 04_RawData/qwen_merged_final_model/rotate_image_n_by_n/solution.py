# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def rotate_image_n_by_n(self, matrix: List[List[int]]) -> None:
        """
        Rotate the given n x n matrix clockwise in-place.

        Args:
            matrix (List[List[int]]): The n x n matrix to be rotated.

        Returns:
            None: The matrix is modified in-place.
        """
        n = len(matrix)
        
        # Transpose the matrix
        for i in range(n):
            for j in range(i, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        # Reverse each row
        for i in range(n):
            matrix[i].reverse()