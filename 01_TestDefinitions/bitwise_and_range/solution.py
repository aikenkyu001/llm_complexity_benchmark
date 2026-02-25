class Solution:
    def rangeBitwiseAnd(self, arg1: int, arg2: int) -> int:
        shift = 0
        # Find the common prefix bits
        while arg1 != arg2:
            arg1 >>= 1
            arg2 >>= 1
            shift += 1
        # Append zeros to the right
        return arg1 << shift