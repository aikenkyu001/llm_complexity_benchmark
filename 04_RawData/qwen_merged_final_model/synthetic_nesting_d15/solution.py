# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def checkNested(self, x0: int, x1: int, x2: int, x3: int, x4: int, x5: int, x6: int, x7: int, x8: int, x9: int, x10: int, x11: int, x12: int, x13: int, x14: int) -> bool:
        # Check each condition sequentially, returning False as soon as any condition fails.
        if x0 <= 0:
            return False
        if x1 <= 0:
            return False
        if x2 <= 0:
            return False
        if x3 <= 0:
            return False
        if x4 <= 0:
            return False
        if x5 <= 0:
            return False
        if x6 <= 0:
            return False
        if x7 <= 0:
            return False
        if x8 <= 0:
            return False
        if x9 <= 0:
            return False
        if x10 <= 0:
            return False
        if x11 <= 0:
            return False
        if x12 <= 0:
            return False
        if x13 <= 0:
            return False
        if x14 <= 0:
            return False
        
        # If all conditions are met, return True
        return True