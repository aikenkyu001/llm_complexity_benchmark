from typing import List

class Solution:
    def optimalBST(self, keys: List[int], freq: List[int]) -> int:
        n = len(keys)
        
        # If no keys are provided, return 0
        if n == 0:
            return 0
        
        # Step 1: Create a prefix sum array to store the cumulative frequencies
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + freq[i]
        
        # Step 2: Initialize the dp table where dp[i][j] is the minimum cost of BST from keys[i] to keys[j]
        dp = [[0] * n for _ in range(n)]
        
        # Fill the dp table
        for length in range(1, n + 1):  # length is the length of the subarray
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Step 3: Calculate the cost for each possible root k in the range [i, j]
                dp[i][j] = float('inf')
                total_freq = prefix_sum[j + 1] - prefix_sum[i]
                
                for k in range(i, j + 1):
                    left_cost = dp[i][k - 1] if k > i else 0
                    right_cost = dp[k + 1][j] if k < j else 0
                    cost = total_freq + left_cost + right_cost
                    
                    if cost < dp[i][j]:
                        dp[i][j] = cost
        
        # The minimum cost to construct the BST for all keys is stored in dp[0][n-1]
        return dp[0][n - 1]