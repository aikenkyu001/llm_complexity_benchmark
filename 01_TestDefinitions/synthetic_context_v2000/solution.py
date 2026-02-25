class Solution:
    def findSecret(self, text: str) -> str:
        # Split the text by spaces to get individual words
        words = text.split()
        # The secret word is at the very end of the text
        secret_word = words[-1]
        return secret_word