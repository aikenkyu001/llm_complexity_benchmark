# Task: lowest_common_ancestor_nary
# Interface:
Class: Solution
Method: lowestCommonAncestor(self, arg1, arg2, arg3)

Given an n-ary tree, find the lowest common ancestor (LCA) of two given nodes.
According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself)."
The N-ary tree node is:
```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children # List[Node]
```

Constraints:
- The number of nodes in the tree is in the range [2, 10^4].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q will exist in the tree.
