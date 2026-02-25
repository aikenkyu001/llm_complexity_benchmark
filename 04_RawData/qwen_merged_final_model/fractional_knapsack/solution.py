# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Item:
    def __init__(self, weight: int, value: int):
        self.weight = weight
        self.value = value
        self.ratio = value / weight

    def __lt__(self, other):
        return self.ratio > other.ratio

class Solution:
    def fractionalKnapsack(self, items: List[tuple[int, int]]) -> float:
        # Create a max-heap based on the value-to-weight ratio
        heap = []
        for weight, value in items:
            heapq.heappush(heap, Item(weight, value))

        total_value = 0.0
        current_capacity = 0

        while heap:
            item = heapq.heappop(heap)
            if current_capacity + item.weight <= capacity:
                total_value += item.value
                current_capacity += item.weight
            else:
                remaining_weight = capacity - current_capacity
                total_value += remaining_weight * item.ratio
                break

        return total_value