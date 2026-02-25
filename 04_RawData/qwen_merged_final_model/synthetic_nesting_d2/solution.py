# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def checkNested(self, x0: int, x1: int) -> bool:
        """
        Check if both x0 and x1 are greater than 0.

        Args:
            x0 (int): The first integer to check.
            x1 (int): The second integer to check.

        Returns:
            bool: True if both x0 and x1 are greater than 0, otherwise False.
        """
        # Check if x0 is greater than 0
        if x0 <= 0:
            return False
        
        # Check if x1 is greater than 0
        if x1 <= 0:
            return False
        
        # If both conditions are met, return True
        return True