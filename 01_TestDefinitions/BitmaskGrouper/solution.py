from typing import List

class Solution:
    def groupNums(self, nums: List[int]) -> List[List[int]]:
        # Sort nums in descending order based on their bit count
        nums.sort(key=lambda x: bin(x).count('1'), reverse=True)
        
        groups = []
        while nums:
            # Start a new group with the first element
            current_group = [nums.pop(0)]
            
            # Try to add more elements to the current group
            i = 0
            while i < len(nums):
                if all(num & current_group[0] != 0 for num in current_group):
                    current_group.append(nums.pop(i))
                else:
                    i += 1
            
            groups.append(current_group)
        
        return groups