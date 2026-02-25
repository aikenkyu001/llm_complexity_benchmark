# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def checkNested(self, x0: int, x1: int, x2: int, x3: int, x4: int) -> bool:
        # Check if x0 is greater than 0
        if x0 <= 0:
            return False
        
        # Check if x1 is greater than 0
        if x1 <= 0:
            return False
        
        # Check if x2 is greater than 0
        if x2 <= 0:
            return False
        
        # Check if x3 is greater than 0
        if x3 <= 0:
            return False
        
        # Check if x4 is greater than 0
        if x4 <= 0:
            return False
        
        # All conditions are met
        return True