class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Rotates the given n x n 2D matrix by 90 degrees clockwise in-place.
        
        :param matrix: List[List[int]] - The input matrix to be rotated.
        """
        n = len(matrix)
        
        # Transpose the matrix
        for i in range(n):
            for j in range(i, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        # Reverse each row
        for i in range(n):
            matrix[i].reverse()