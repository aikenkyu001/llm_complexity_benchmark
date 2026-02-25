# solution.py
from typing import List, Optional

class Node:
    def __init__(self, val: int = 0, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children if children is not None else []

class Solution:
    def serialize(self, root: 'Optional[Node]') -> List[int]:
        """Encodes a tree to a single string."""
        serialized_list = []
        
        def dfs(node: Optional['Node']):
            if node is None:
                return
            serialized_list.append(node.val)
            for child in node.children:
                dfs(child)
            serialized_list.append(None)  # Marker for end of children
        
        dfs(root)
        return serialized_list

    def deserialize(self, data: List[int]) -> 'Optional[Node]':
        """Decodes your encoded data to tree."""
        if not data:
            return None
        
        root = Node(data[0])
        stack = [root]
        
        for val in data[1:]:
            if val is None:
                stack.pop()
            else:
                new_node = Node(val)
                stack[-1].children.append(new_node)
                stack.append(new_node)
        
        return root