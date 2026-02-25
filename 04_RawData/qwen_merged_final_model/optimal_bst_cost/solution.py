# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def optimalBST(self, keys: List[int], freq: List[int]) -> int:
        """
        Finds the minimum cost to construct a Binary Search Tree (BST) such that the total cost of searching all keys is minimized.
        
        The cost of searching a key is its frequency multiplied by its depth in the tree (the root has depth 1).
        
        Parameters:
        keys (List[int]): A list of unique keys.
        freq (List[int]): A list of frequencies corresponding to each key.
        
        Returns:
        int: The minimum cost to construct the BST.
        """
        n = len(keys)
        
        # Create a dictionary to store the frequency of each key
        freq_dict = {key: freq[i] for i, key in enumerate(keys)}
        
        # Create a list of tuples (key, frequency) sorted by frequency
        freq_list = [(key, freq_dict[key]) for key in keys]
        freq_list.sort(key=lambda x: x[1])
        
        # Create a list of nodes with their frequencies
        nodes = [Node(key, freq_dict[key]) for key, _ in freq_list]
        
        # Create a priority queue to store the nodes
        pq = []
        for node in nodes:
            heapq.heappush(pq, (node.freq, node))
        
        # Initialize the total cost to 0
        total_cost = 0
        
        # While there are more than one nodes in the priority queue
        while len(pq) > 1:
            # Pop the two nodes with the smallest frequencies
            left_node = heapq.heappop(pq)
            right_node = heapq.heappop(pq)
            
            # Create a new node with the sum of the frequencies of the two nodes
            new_node = Node(None, left_node[1].freq + right_node[1].freq)
            new_node.left = left_node[1]
            new_node.right = right_node[1]
            
            # Push the new node back into the priority queue
            heapq.heappush(pq, (new_node.freq, new_node))
            
            # Add the cost of the new node to the total cost
            total_cost += new_node.freq
        
        # Return the total cost
        return total_cost

class Node:
    def __init__(self, key: Optional[int], freq: int):
        self.key = key
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq