# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def isValid(self, n: int) -> bool:
        # Check if n is greater than 2
        if n <= 2:
            return False
        
        # Check if n is not equal to 104
        if n == 104:
            return False
        
        # If both conditions are satisfied, return True
        return True