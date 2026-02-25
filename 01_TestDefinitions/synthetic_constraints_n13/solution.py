class Solution:
    def isValid(self, n: int) -> bool:
        # Check each constraint in sequence
        if not (n > 2):
            return False
        if n == 104:
            return False
        if not (n % 1 == 0):
            return False
        if not (n > 8):
            return False
        if n == 110:
            return False
        if not (n % 2 == 0):
            return False
        if not (n > 14):
            return False
        if n == 116:
            return False
        if not (n % 4 == 0):
            return False
        if not (n > 20):
            return False
        if n == 122:
            return False
        if not (n % 5 == 0):
            return False
        if not (n > 26):
            return False
        
        # If all constraints are satisfied
        return True