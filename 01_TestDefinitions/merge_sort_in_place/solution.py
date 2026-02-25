# solution.py
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        
        # Find the middle of the list using the slow and fast pointer technique
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Split the list into two halves
        mid = slow.next
        slow.next = None
        
        # Recursively sort both halves
        left = self.sortList(head)
        right = self.sortList(mid)
        
        # Merge the sorted halves
        return self.merge(left, right)

    def merge(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        
        # If there are remaining nodes in either list, append them
        tail.next = l1 or l2
        
        return dummy.next