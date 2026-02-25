# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

class Codec:

    def serialize(self, root: 'Node') -> str:
        """Encodes a tree to a single string."""
        if not root:
            return ""
        
        def dfs(node):
            result = str(node.val) + ","
            for child in node.children:
                result += dfs(child) + ","
            return result
        
        return dfs(root)

    def deserialize(self, data: str) -> 'Node':
        """Decodes your encoded data to tree."""
        if not data:
            return None
        
        def build_tree(nodes):
            if not nodes:
                return None
            
            val = nodes.popleft()
            if val == ",":
                return None
            
            node = Node(int(val))
            while nodes and nodes[0] != ",":
                node.children.append(build_tree(nodes))
            
            return node
        
        nodes = collections.deque(data.split(","))
        return build_tree(nodes)

class Solution:
    def serializeAndDeserializeNaryTree(self, root: 'Node') -> str:
        return Codec().serialize(root)
    
    def deserializeNaryTree(self, data: str) -> 'Node':
        return Codec().deserialize(data)