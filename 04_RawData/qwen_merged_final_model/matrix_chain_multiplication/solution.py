# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def matrixChainOrder(self, p: List[int]) -> int:
        n = len(p)
        
        # dp[i][j] will hold the minimum number of scalar multiplications needed
        # to multiply the subsequence of matrices from i to j
        dp = [[0] * n for _ in range(n)]
        
        # Fill the dp table
        for l in range(2, n):
            for i in range(n - l + 1):
                j = i + l - 1
                dp[i][j] = float('inf')
                for k in range(i, j):
                    cost = dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]
                    dp[i][j] = min(dp[i][j], cost)
        
        return dp[0][n-1]