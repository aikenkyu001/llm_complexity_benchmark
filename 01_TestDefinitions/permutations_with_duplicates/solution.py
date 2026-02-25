from typing import List
from itertools import permutations

class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        # Generate all unique permutations using a set to filter duplicates
        unique_perms = set(permutations(nums))
        # Convert the set back to a list of lists and return
        return [list(perm) for perm in unique_perms]