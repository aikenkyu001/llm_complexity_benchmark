# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        if k < 1 or k > len(nums):
            return -1
        
        # Use a min-heap to keep track of the top k largest elements
        min_heap = []
        
        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        
        # The root of the heap is the kth largest element
        return min_heap[0]