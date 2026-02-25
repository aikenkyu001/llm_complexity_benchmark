import pytest
from solution import Solution

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def test_max_path_sum_basic():
    solution = Solution()
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert solution.maxPathSum(root) == 6

def test_max_path_sum_negative():
    solution = Solution()
    root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    # Path: 15 -> 20 -> 7 => 42
    assert solution.maxPathSum(root) == 42
