# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        def justify_line(line: List[str], total_width: int) -> str:
            if len(line) == 1:
                return line[0].ljust(maxWidth)
            
            num_spaces = maxWidth - total_width
            space_slots = len(line) - 1
            if space_slots == 0:
                return line[0].rjust(maxWidth)
            
            spaces_per_slot = num_spaces // space_slots
            extra_spaces = num_spaces % space_slots
            
            result = []
            for word in line[:-1]:
                result.append(word)
                result.extend([' '] * (spaces_per_slot + (1 if extra_spaces > 0 else 0)))
                extra_spaces -= 1
            
            result.append(line[-1])
            
            return ''.join(result)

        result = []
        current_line = []
        current_width = 0
        
        for word in words:
            if current_width + len(word) + len(current_line) > maxWidth:
                result.append(justify_line(current_line, current_width))
                current_line = [word]
                current_width = len(word)
            else:
                current_line.append(word)
                current_width += len(word) + 1
        
        if current_line:
            result.append(justify_line(current_line, current_width, True))
        
        return result