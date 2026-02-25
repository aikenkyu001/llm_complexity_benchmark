# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        # Implement the regular expression matching logic here
        # Use dynamic programming to solve the problem
        m, n = len(s), len(p)
        
        # Create a DP table with dimensions (m+1) x (n+1)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        
        # Base case: empty pattern matches empty string
        dp[0][0] = True
        
        # Handle patterns with '*' at the beginning
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]
        
        # Fill the DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                    dp[i][j] = dp[i - 1][j - 1]
                elif p[j - 1] == '*':
                    # Match zero occurrences of the preceding element
                    dp[i][j] = dp[i][j - 2]
                    # Match one or more occurrences of the preceding element
                    if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                        dp[i][j] |= dp[i - 1][j]
        
        # The result is in the bottom-right cell of the DP table
        return dp[m][n]