# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        result = []
        nums.sort()
        
        def backtrack(path, remaining):
            if not remaining:
                result.append(path[:])
                return
            
            for i in range(len(remaining)):
                if i > 0 and remaining[i] == remaining[i - 1]:
                    continue
                
                path.append(remaining[i])
                backtrack(path, remaining[:i] + remaining[i+1:])
                path.pop()
        
        backtrack([], nums)
        return result