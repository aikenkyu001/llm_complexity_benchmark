# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def multiply(self, mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
        """
        Multiply two sparse matrices.

        Args:
            mat1 (List[List[int]]): The first matrix.
            mat2 (List[List[int]]): The second matrix.

        Returns:
            List[List[int]]: The product of the two matrices.
        """
        m, n, k = len(mat1), len(mat1[0]), len(mat2[0])
        result = [[0] * k for _ in range(m)]

        # Helper function to convert a row or column to a dictionary of non-zero elements
        def to_dict(matrix, i):
            return {j: val for j, val in enumerate(matrix[i]) if val != 0}

        # Convert both matrices to dictionaries of non-zero elements
        mat1_dict = [to_dict(mat1, i) for i in range(m)]
        mat2_dict = [to_dict(mat2, j) for j in range(k)]

        # Perform matrix multiplication using the dictionaries
        for i in range(m):
            for j in range(k):
                for col in mat1_dict[i]:
                    if col in mat2_dict[j]:
                        result[i][j] += mat1_dict[i][col] * mat2_dict[j][col]

        return result