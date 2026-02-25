class Solution:
    def findSecret(self, text: str) -> str:
        # Split the text into words
        words = text.split()
        # The secret word is the last word in the list
        secret_word = words[-1]
        return secret_word