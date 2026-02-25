class Solution:
    def findSecret(self, text: str) -> str:
        lines = text.split('\n')
        for line in reversed(lines):
            if line.startswith("The secret word you are looking for is: "):
                return line.split(": ")[1]
        return ""