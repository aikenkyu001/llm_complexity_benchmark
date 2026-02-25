from typing import List, Optional, Dict, Set

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

class Solution:
    def __init__(self):
        self.trie = Trie()
    
    def log_split(self, index: int) -> None:
        # This method should be implemented to log the split points
        print(f"Split at index {index}")
    
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        if not wordDict or not s:
            return False
        
        # Build the Trie from the dictionary
        for word in wordDict:
            self.trie.insert(word)
        
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True  # Base case: empty string can be segmented
        
        # Dynamic Programming with memoization
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and self.trie.search(s[j:i]):
                    dp[i] = True
                    self.log_split(j)
                    break
        
        return dp[n]

# Example usage:
# solution = Solution()
# result = solution.wordBreak("leetcode", ["leet", "code"])
# print(result)  # Output: True