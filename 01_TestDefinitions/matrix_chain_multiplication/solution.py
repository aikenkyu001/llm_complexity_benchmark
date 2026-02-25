class Solution:
    def matrixChainOrder(self, p: List[int]) -> int:
        n = len(p)
        
        # Create a table to store results of subproblems
        dp = [[0 for _ in range(n)] for _ in range(n)]
        
        # L is chain length. The value of L increases from 2 to n-1.
        for L in range(2, n):
            # i is the starting index of the subarray
            for i in range(1, n - L + 1):
                j = i + L - 1
                dp[i][j] = float('inf')
                
                # q is used to store the result of subproblems
                for k in range(i, j):
                    q = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]
                    
                    if q < dp[i][j]:
                        dp[i][j] = q
        
        # The result is stored in dp[1][n-1]
        return dp[1][n - 1]