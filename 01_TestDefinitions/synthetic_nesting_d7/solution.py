class Solution:
    def checkNested(self, x0: int, x1: int, x2: int, x3: int, x4: int, x5: int, x6: int) -> bool:
        return (x0 > 0 and 
                (x1 > 0 and 
                 (x2 > 0 and 
                  (x3 > 0 and 
                   (x4 > 0 and 
                    (x5 > 0 and 
                     (x6 > 0)))))))