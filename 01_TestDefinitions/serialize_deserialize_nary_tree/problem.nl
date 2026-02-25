Design an algorithm to serialize and deserialize an N-ary tree. An N-ary tree is a rooted tree in which each node has no more than N children. 
Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
The N-ary tree node structure is:
```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children # List[Node]
```

Constraints:
- The total number of nodes is between 0 and 10^4.
- 0 <= Node.val <= 10^4
- The height of the N-ary tree is less than or equal to 1000.
