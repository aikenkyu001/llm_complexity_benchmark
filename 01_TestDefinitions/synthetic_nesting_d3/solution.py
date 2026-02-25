class Solution:
    def checkNested(self, x0: int, x1: int, x2: int) -> bool:
        if x0 > 0:
            if x1 > 0:
                if x2 > 0:
                    return True
        return False