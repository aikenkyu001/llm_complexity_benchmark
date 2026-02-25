# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class Solution:
    def findSecret(self, text: str) -> str:
        """
        Finds the secret word at the very end of the given text.

        Args:
            text (str): The text containing the secret word.

        Returns:
            str: The secret word found in the text.
        """
        # Split the text by spaces to handle multiple words
        words = text.split()
        
        # Check if the last word is the secret word
        if words and words[-1].isalpha():
            return words[-1]
        
        # If no valid secret word is found, return an empty string
        return ""