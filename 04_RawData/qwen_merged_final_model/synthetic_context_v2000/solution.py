# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def findSecret(self, text: str) -> str:
        # Split the text into words
        words = text.split()
        
        # Find the last word in the list
        last_word = words[-1]
        
        # Check if the last word is the secret word
        if last_word.isupper():
            return last_word
        
        # If the last word is not uppercase, return an empty string
        return ""