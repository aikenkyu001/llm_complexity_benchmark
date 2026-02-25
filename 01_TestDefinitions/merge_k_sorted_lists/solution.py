# solution.py
from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Min-heap to store the head nodes of each list along with their indices
        min_heap = []
        
        # Initialize the heap with the head node of each list
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(min_heap, (lst.val, i))
        
        # Dummy node to simplify the process of building the merged list
        dummy = ListNode()
        current = dummy
        
        while min_heap:
            # Pop the smallest element from the heap
            val, idx = heapq.heappop(min_heap)
            
            # Add the smallest node to the merged list
            current.next = ListNode(val)
            current = current.next
            
            # Move to the next node in the original list and push it to the heap if it exists
            lists[idx] = lists[idx].next
            if lists[idx]:
                heapq.heappush(min_heap, (lists[idx].val, idx))
        
        # Return the head of the merged list
        return dummy.next