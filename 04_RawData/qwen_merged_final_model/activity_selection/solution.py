# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def maxActivities(self, activities: List[List[int]]) -> int:
        """
        Select the maximum number of activities that can be performed by a single person.
        
        Activities must be selected such that no two activities overlap.
        
        Parameters:
        activities (List[List[int]]): A list of lists where each sublist contains two integers [start, finish].
        
        Returns:
        int: The number of activities that can be selected.
        """
        # Sort activities by their finish time
        activities.sort(key=lambda x: x[1])
        
        # Initialize a heap to keep track of the end times of selected activities
        heap = []
        
        # Iterate through each activity
        for start, finish in activities:
            # If the heap is empty or the current activity starts after the earliest ending activity ends
            if not heap or start >= heap[0]:
                # Add the finish time of the current activity to the heap
                heapq.heappush(heap, finish)
            else:
                # Remove the earliest ending activity from the heap
                heapq.heappop(heap)
        
        # The size of the heap is the number of non-overlapping activities
        return len(heap)