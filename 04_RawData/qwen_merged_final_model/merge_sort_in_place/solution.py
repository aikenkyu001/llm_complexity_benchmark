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
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Helper function to merge two sorted lists
        def merge(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
            dummy = ListNode()
            current = dummy
            while l1 and l2:
                if l1.val < l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next
            current.next = l1 or l2
            return dummy.next
        
        # Base case: empty list or single element list
        if not head or not head.next:
            return head
        
        # Find the middle of the list
        slow = head
        fast = head
        prev_slow = None
        while fast and fast.next:
            prev_slow = slow
            slow = slow.next
            fast = fast.next.next
        
        # Split the list into two halves
        prev_slow.next = None
        
        # Recursively sort both halves
        left = self.sortList(head)
        right = self.sortList(slow)
        
        # Merge the sorted halves
        return merge(left, right)