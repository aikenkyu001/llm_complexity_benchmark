# Task: merge_k_sorted_lists
# Interface:
Class: Solution
Method: mergeKLists(self, arg1)

You are given an array of k linked-lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.
The linked list node is:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i].val <= 10^4
- lists[i] is sorted in ascending order.
- The total sum of lists[i].length will not exceed 10^4.
