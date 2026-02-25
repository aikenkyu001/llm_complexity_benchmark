# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Use a min-heap to keep track of the k largest elements seen so far
        min_heap = []
        
        for num in nums:
            # Add the current number to the heap
            heapq.heappush(min_heap, num)
            
            # If the heap size exceeds k, remove the smallest element
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        
        # The root of the heap is the kth largest element
        return min_heap[0]