class Solution:
    def multiply(self, mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
        m = len(mat1)
        k = len(mat1[0])
        n = len(mat2[0])

        # Initialize the result matrix with zeros
        result = [[0] * n for _ in range(m)]

        # Convert mat1 to a dictionary of non-zero elements
        mat1_dict = {}
        for i in range(m):
            for j in range(k):
                if mat1[i][j] != 0:
                    if i not in mat1_dict:
                        mat1_dict[i] = []
                    mat1_dict[i].append((j, mat1[i][j]))

        # Convert mat2 to a dictionary of non-zero elements
        mat2_dict = {}
        for j in range(k):
            for l in range(n):
                if mat2[j][l] != 0:
                    if j not in mat2_dict:
                        mat2_dict[j] = []
                    mat2_dict[j].append((l, mat2[j][l]))

        # Perform matrix multiplication
        for i in range(m):
            for j in range(k):
                if j in mat1_dict and i in mat2_dict:
                    for (col1, val1) in mat1_dict[i]:
                        for (row2, val2) in mat2_dict[j]:
                            result[i][row2] += val1 * val2

        return result