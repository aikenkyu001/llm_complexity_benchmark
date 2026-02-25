# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def findSecret(self, text: str) -> str:
        # Split the text by spaces to find words
        words = text.split()
        
        # Iterate through the words to find the last word
        for word in reversed(words):
            # Check if the word is a valid secret word
            if self.is_secret_word(word):
                return word
        
        # If no secret word is found, return an empty string
        return ""
    
    def is_secret_word(self, word: str) -> bool:
        # Implement logic to check if the word is a valid secret word
        # For example, check if the word is uppercase and ends with a period
        return word.isupper() and word.endswith('.')