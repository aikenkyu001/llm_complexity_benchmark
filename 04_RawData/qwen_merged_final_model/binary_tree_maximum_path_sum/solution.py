# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            
            # Recursively find the maximum path sum for the left and right subtrees
            left_max = max(dfs(node.left), 0)
            right_max = max(dfs(node.right), 0)
            
            # The maximum path sum through the current node
            current_max_path_sum = node.val + left_max + right_max
            
            # Update the global maximum path sum
            self.global_max = max(self.global_max, current_max_path_sum)
            
            # Return the maximum path sum that can be extended upwards
            return node.val + max(left_max, right_max)
        
        # Initialize the global maximum path sum
        self.global_max = float('-inf')
        
        # Start DFS from the root
        dfs(root)
        
        return self.global_max