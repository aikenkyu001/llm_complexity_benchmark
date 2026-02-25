# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Sort intervals by their start time
        intervals.sort(key=lambda x: x[0])
        
        merged = []
        current_interval = intervals[0]
        
        for interval in intervals[1:]:
            if interval[0] <= current_interval[1]:
                # Merge intervals
                current_interval[1] = max(current_interval[1], interval[1])
            else:
                # Add the current merged interval to the result
                merged.append(current_interval)
                current_interval = interval
        
        # Add the last merged interval
        merged.append(current_interval)
        
        return merged