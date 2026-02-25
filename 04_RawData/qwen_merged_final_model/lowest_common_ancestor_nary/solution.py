# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

class Solution:
    def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
        # Helper function to find the path from root to a given node
        def find_path(node, target, path):
            if not node:
                return False
            path.append(node)
            if node == target:
                return True
            for child in node.children:
                if find_path(child, target, path):
                    return True
            path.pop()
            return False

        # Find paths from root to p and q
        path_p = []
        path_q = []
        find_path(root, p, path_p)
        find_path(root, q, path_q)

        # Find the last common node in the paths
        lca = None
        for i in range(min(len(path_p), len(path_q))):
            if path_p[i] == path_q[i]:
                lca = path_p[i]
            else:
                break

        return lca