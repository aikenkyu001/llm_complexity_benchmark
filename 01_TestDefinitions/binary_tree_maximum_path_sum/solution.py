# solution.py
from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # Initialize the maximum sum to negative infinity
        self.max_sum = float('-inf')
        
        def helper(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            
            # Recursively get the maximum gain from the left and right subtrees
            left_gain = max(helper(node.left), 0)
            right_gain = max(helper(node.right), 0)
            
            # Price of the new path
            price_newpath = node.val + left_gain + right_gain
            
            # Update the maximum sum if the new path is better
            self.max_sum = max(self.max_sum, price_newpath)
            
            # Return the maximum gain the current node can contribute to its parent
            return node.val + max(left_gain, right_gain)
        
        helper(root)
        return self.max_sum