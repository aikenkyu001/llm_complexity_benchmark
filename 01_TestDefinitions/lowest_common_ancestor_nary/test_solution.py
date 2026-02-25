import pytest
from solution import Solution

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

def test_lca_nary_basic():
    solution = Solution()
    # 3 -> [5, 1, 6]; 5 -> [6, 2, 7]; 1 -> [0, 8]
    root = Node(3, [
        Node(5, [Node(6), Node(2), Node(7)]),
        Node(1, [Node(0), Node(8)])
    ])
    p = root.children[0] # node 5
    q = root.children[1] # node 1
    assert solution.lowestCommonAncestor(root, p, q).val == 3

def test_lca_nary_descendant():
    solution = Solution()
    root = Node(3, [Node(5), Node(1)])
    p = root # node 3
    q = root.children[0] # node 5
    assert solution.lowestCommonAncestor(root, p, q).val == 3
