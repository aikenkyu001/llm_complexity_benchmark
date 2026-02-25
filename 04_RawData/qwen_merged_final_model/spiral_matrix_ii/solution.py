# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        if n == 0:
            return []

        matrix = [[0] * n for _ in range(n)]
        num = 1
        top, bottom, left, right = 0, n - 1, 0, n - 1

        while top <= bottom and left <= right:
            # Fill the top row
            for i in range(left, right + 1):
                matrix[top][i] = num
                num += 1
            top += 1

            # Fill the right column
            for i in range(top, bottom + 1):
                matrix[i][right] = num
                num += 1
            right -= 1

            # Fill the bottom row
            if top <= bottom:
                for i in range(right, left - 1, -1):
                    matrix[bottom][i] = num
                    num += 1
                bottom -= 1

            # Fill the left column
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    matrix[i][left] = num
                    num += 1
                left += 1

        return matrix