# solution.py
from typing import Optional

# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

class Solution:
    def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
        # Helper function to perform DFS and find paths to p and q
        def dfs(node: 'Node', target: 'Node', path: List['Node']) -> bool:
            if node is None:
                return False
            path.append(node)
            if node == target:
                return True
            for child in node.children:
                if dfs(child, target, path):
                    return True
            path.pop()
            return False
        
        # Find paths from root to p and q
        path_p = []
        path_q = []
        
        dfs(root, p, path_p)
        dfs(root, q, path_q)
        
        # Compare the paths to find the lowest common ancestor
        i = 0
        while i < len(path_p) and i < len(path_q) and path_p[i] == path_q[i]:
            i += 1
        
        return path_p[i - 1]