class Solution:
    def isValid(self, n: int) -> bool:
        """
        Determine if the integer n satisfies both constraints.

        :param n: Integer to be checked.
        :return: True if both conditions are met, otherwise return False.
        """
        # Check if n is greater than 2
        if n <= 2:
            return False
        
        # Check if n is not equal to 104
        if n == 104:
            return False
        
        # If both conditions are satisfied
        return True