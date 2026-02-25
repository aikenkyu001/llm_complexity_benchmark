# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Implement the wordBreak function here
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for word in wordDict:
                if i >= len(word) and dp[i - len(word)] and s[i - len(word):i] == word:
                    dp[i] = True
                    break
        
        return dp[n]