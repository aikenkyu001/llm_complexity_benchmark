# Task: merge_sort_in_place
# Interface:
Class: Solution
Method: sortList(self, arg1)

Given the head of a linked list, return the list after sorting it in ascending order using merge sort.
The sorting must be done in-place (i.e., modifying the links, not creating new nodes where possible) and achieve O(n log n) time complexity.
The linked list node is:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Constraints:
- The number of nodes in the list is in the range [0, 5 * 10^4].
- -10^5 <= Node.val <= 10^5
