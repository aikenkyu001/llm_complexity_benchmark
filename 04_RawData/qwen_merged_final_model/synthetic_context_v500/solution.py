# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def findSecret(self, text: str) -> str:
        # Split the text into words
        words = text.split()
        
        # Check if the last word is the secret word
        if words and words[-1].isupper():
            return words[-1]
        
        # If no secret word is found, return an empty string
        return ""