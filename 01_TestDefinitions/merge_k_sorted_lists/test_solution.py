import pytest
from solution import Solution

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(arr):
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for i in range(1, len(arr)):
        curr.next = ListNode(arr[i])
        curr = curr.next
    return head

def test_merge_k_basic():
    solution = Solution()
    lists = [
        from_list([1, 4, 5]),
        from_list([1, 3, 4]),
        from_list([2, 6])
    ]
    result = solution.mergeKLists(lists)
    assert to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]

def test_merge_k_empty():
    solution = Solution()
    assert solution.mergeKLists([]) is None
    assert solution.mergeKLists([None]) is None
