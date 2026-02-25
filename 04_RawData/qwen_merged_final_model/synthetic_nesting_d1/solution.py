# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def checkNested(self, x0: int) -> bool:
        # Check if x0 is greater than 0
        if x0 <= 0:
            return False
        return True