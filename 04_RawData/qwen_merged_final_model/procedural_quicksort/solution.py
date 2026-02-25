# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def quickSort(self, arr: List[int]) -> None:
        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def quicksort_recursive(low: int, high: int) -> None:
            if low < high:
                pi = partition(low, high)
                quicksort_recursive(low, pi - 1)
                quicksort_recursive(pi + 1, high)

        quicksort_recursive(0, len(arr) - 1)