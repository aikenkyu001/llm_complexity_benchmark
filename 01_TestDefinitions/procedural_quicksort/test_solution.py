import pytest
from solution import Solution

def test_quicksort_basic():
    solution = Solution()
    arr = [10, 7, 8, 9, 1, 5]
    solution.quickSort(arr)
    assert arr == [1, 5, 7, 8, 9, 10]

def test_quicksort_empty():
    solution = Solution()
    arr = []
    solution.quickSort(arr)
    assert arr == []

def test_quicksort_duplicates():
    solution = Solution()
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    solution.quickSort(arr)
    assert arr == [1, 1, 2, 3, 4, 5, 5, 6, 9]
