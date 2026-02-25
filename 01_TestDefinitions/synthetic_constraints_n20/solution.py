class Solution:
    def isValid(self, n: int) -> bool:
        constraints = [
            lambda x: x > 2,
            lambda x: x != 104,
            lambda x: x % 1 == 0,
            lambda x: x > 8,
            lambda x: x != 110,
            lambda x: x % 2 == 0,
            lambda x: x > 14,
            lambda x: x != 116,
            lambda x: x % 4 == 0,
            lambda x: x > 20,
            lambda x: x != 122,
            lambda x: x % 5 == 0,
            lambda x: x > 26,
            lambda x: x != 128,
            lambda x: x % 7 == 0,
            lambda x: x > 32,
            lambda x: x != 134,
            lambda x: x % 8 == 0,
            lambda x: x > 38,
            lambda x: x != 140
        ]
        
        for constraint in constraints:
            if not constraint(n):
                return False
        
        return True