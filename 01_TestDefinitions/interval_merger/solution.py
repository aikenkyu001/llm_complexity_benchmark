# solution.py
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        # Sort intervals based on the start time
        intervals.sort(key=lambda x: x[0])

        merged = [intervals[0]]

        for current in intervals[1:]:
            last_merged = merged[-1]
            if current[0] <= last_merged[1]:  # Overlapping intervals
                last_merged[1] = max(last_merged[1], current[1])
            else:
                merged.append(current)

        return merged