class Solution:
    def findSecret(self, text: str) -> str:
        phrase = "The secret word you are looking for is:"
        start_index = text.find(phrase)
        
        if start_index == -1:
            return ""
        
        # Move the index to the end of the phrase
        start_index += len(phrase)
        
        # Find the next newline character or the end of the string
        end_index = text.find('\n', start_index)
        if end_index == -1:
            end_index = len(text)
        
        # Extract and strip the secret word
        secret_word = text[start_index:end_index].strip()
        
        return secret_word