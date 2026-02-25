# solution.py
from typing import *

class Solution:
    def isValid(self, s: str) -> bool:
        # A stack to keep track of opening brackets
        stack = []
        
        # Mapping of closing brackets to their corresponding opening brackets
        bracket_map = {')': '(', '}': '{', ']': '['}
        
        # Iterate through each character in the string
        for char in s:
            # If the character is a closing bracket
            if char in bracket_map:
                # Pop the topmost element from the stack if it's not empty, otherwise use a dummy value
                top_element = stack.pop() if stack else '#'
                
                # Check if the popped element matches the corresponding opening bracket
                if bracket_map[char] != top_element:
                    return False
            else:
                # If it's an opening bracket, push it onto the stack
                stack.append(char)
        
        # If the stack is empty, all brackets were matched correctly
        return not stack