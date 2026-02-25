# Task: sparse_matrix_multiplication
# Interface:
Class: Solution
Method: multiply(self, arg1, arg2)

Given two sparse matrices mat1 of size m x k and mat2 of size k x n, return the result of mat1 x mat2.
A matrix is sparse if most of its elements are 0. You should optimize the multiplication for sparse matrices.

Constraints:
- m == mat1.length
- k == mat1[i].length == mat2.length
- n == mat2[i].length
- 1 <= m, n, k <= 100
- -100 <= mat1[i][j], mat2[i][j] <= 100
