# Task: minimum_spanning_tree_prim
# Interface:
Class: Solution
Method: primMST(self, graph: Dict[int, List[Tuple[int, int]]], n: int) -> int

Given a weighted, undirected connected graph with n vertices (labeled 0 to n-1), find the sum of the weights of the edges in its Minimum Spanning Tree using Prim's algorithm.
The graph is represented as an adjacency list: `graph[u] = [(v, weight), ...]` where u is the source node, v is the destination, and weight is the edge weight.

# Important:
The function MUST accept TWO arguments: `graph` and `n`.

# Implementation Hint:
Use a priority queue (min-heap) to store edges or nodes. Initialize a `visited` array or set of size `n`. 
Start by marking node 0 as visited and adding its neighbors to the heap.

Constraints:
- 1 <= n <= 1000
- 1 <= weight <= 1000
