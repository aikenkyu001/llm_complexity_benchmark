import pytest
from solution import Solution

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

def is_same_tree(root1, root2):
    if not root1 and not root2: return True
    if not root1 or not root2: return False
    if root1.val != root2.val: return False
    if len(root1.children) != len(root2.children): return False
    return all(is_same_tree(c1, c2) for c1, c2 in zip(root1.children, root2.children))

def test_tree_serialize_basic():
    codec = Solution()
    # Tree: 1 -> [3, 2, 4]; 3 -> [5, 6]
    root = Node(1, [
        Node(3, [Node(5), Node(6)]),
        Node(2),
        Node(4)
    ])
    serialized = codec.serialize(root)
    deserialized = codec.deserialize(serialized)
    assert is_same_tree(root, deserialized)

def test_tree_serialize_none():
    codec = Solution()
    assert codec.deserialize(codec.serialize(None)) is None
