class Solution:
    def isValid(self, n: int) -> bool:
        # Check if n is greater than 2
        if n <= 2:
            return False
        
        # Ensure n is not equal to 104
        if n == 104:
            return False
        
        # Confirm that n is a multiple of 1 (which is always true for integers)
        if n % 1 != 0:
            return False
        
        # If all constraints are satisfied, return True
        return True