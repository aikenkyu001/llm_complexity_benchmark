# Task: Optimal BST Cost
# Interface:
Class: Solution
Method: optimalBST(self, keys: List[int], freq: List[int]) -> int

Given a sorted array of keys and their search frequencies, find the minimum cost to construct a Binary Search Tree (BST) such that the total cost of searching all keys is minimized.
The cost of searching a key is its frequency multiplied by its depth in the tree (the root has depth 1).

# Implementation Hint:
Use Dynamic Programming with a 3D state transition. Define `dp[i][j]` as the minimum cost for keys from index `i` to `j`.
The cost for a sub-range `dp[i][j]` is the sum of frequencies in that range plus the minimum value of `dp[i][k-1] + dp[k+1][j]` for all possible roots `k` in the range `[i, j]`.

Constraints:
- 1 <= n <= 100
- 1 <= frequencies[i] <= 1000
