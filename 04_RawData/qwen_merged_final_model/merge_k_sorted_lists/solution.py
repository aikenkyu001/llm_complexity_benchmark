# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Priority queue to store nodes with their values and indices
        pq = []
        
        # Initialize the priority queue with the first element of each list
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(pq, (node.val, i, node))
        
        # Dummy head for the result list
        dummy_head = ListNode()
        current = dummy_head
        
        # Merge the lists
        while pq:
            val, i, node = heapq.heappop(pq)
            current.next = ListNode(val)
            current = current.next
            
            # Add the next node from the same list to the priority queue
            if node.next:
                heapq.heappush(pq, (node.next.val, i, node.next))
        
        return dummy_head.next