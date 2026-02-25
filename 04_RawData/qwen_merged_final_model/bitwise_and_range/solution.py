# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        # Find the highest power of 2 that divides both left and right
        while left < right:
            left >>= 1
            right >>= 1
        return left << right.bit_length()