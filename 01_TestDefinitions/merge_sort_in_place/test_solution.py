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

def test_merge_sort_basic():
    solution = Solution()
    head = from_list([4, 2, 1, 3])
    result = solution.sortList(head)
    assert to_list(result) == [1, 2, 3, 4]

def test_merge_sort_empty():
    solution = Solution()
    assert solution.sortList(None) is None
