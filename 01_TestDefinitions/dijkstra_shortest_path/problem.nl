# Task: Dijkstra Shortest Path
# Interface:
Class: Solution
Method: dijkstra(self, graph: Dict[int, List[Tuple[int, int]]], start_node: int, n: int) -> List[float]

Given a weighted, undirected graph and a starting node, return the shortest distance to all other nodes from the source.
The graph is represented as an adjacency list: `graph[u] = [(v, weight), ...]`.
If a node is unreachable, the distance should be infinity (represented as a very large integer or float('inf')).

Constraints:
- The number of nodes is between 1 and 1000.
- Weights are non-negative.

