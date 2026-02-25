# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def checkNested(self, x0: int, x1: int, x2: int, x3: int) -> bool:
        # Check if all conditions are met
        if x0 > 0 and x1 > 0 and x2 > 0 and x3 > 0:
            return True
        else:
            return False