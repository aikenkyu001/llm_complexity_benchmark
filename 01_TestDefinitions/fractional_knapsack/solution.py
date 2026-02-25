from typing import List, Tuple

class Solution:
    def fractionalKnapsack(self, items: List[Tuple[int, int]], capacity: int) -> float:
        # Calculate the value-to-weight ratio for each item
        items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
        
        total_value = 0.0
        
        for value, weight in items:
            if capacity == 0:
                break
            if weight <= capacity:
                # If the item can be taken completely
                total_value += value
                capacity -= weight
            else:
                # If the item cannot be taken completely, take a fraction of it
                fraction = capacity / weight
                total_value += value * fraction
                break
        
        return total_value