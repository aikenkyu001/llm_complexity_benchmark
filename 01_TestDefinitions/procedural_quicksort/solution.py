class Solution:
    def quickSort(self, arr: List[int]) -> None:
        """
        Sorts the input array in-place using the QuickSort algorithm.
        
        Parameters:
        arr (List[int]): The list of integers to be sorted.
        """
        self._quickSortHelper(arr, 0, len(arr) - 1)

    def _quickSortHelper(self, arr: List[int], low: int, high: int) -> None:
        if low < high:
            pi = self._partition(arr, low, high)
            self._quickSortHelper(arr, low, pi - 1)
            self._quickSortHelper(arr, pi + 1, high)

    def _partition(self, arr: List[int], low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1