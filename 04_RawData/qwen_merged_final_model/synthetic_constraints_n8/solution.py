# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def isValid(self, n: int) -> bool:
        # Check if n satisfies all the given constraints
        constraints = [
            n > 2,
            n != 104,
            n % 1 == 0,
            n > 8,
            n != 110,
            n % 2 == 0,
            n > 14,
            n != 116
        ]
        
        # Return True if all constraints are satisfied, False otherwise
        return all(constraints)