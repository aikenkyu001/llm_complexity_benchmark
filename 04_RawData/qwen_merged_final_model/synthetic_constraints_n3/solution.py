# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def isValid(self, n: int) -> bool:
        # Check if n > 2
        if n <= 2:
            return False
        
        # Check if n != 104
        if n == 104:
            return False
        
        # Check if n % 1 == 0
        if n % 1 != 0:
            return False
        
        # If all checks pass, return True
        return True