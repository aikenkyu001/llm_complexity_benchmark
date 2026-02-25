# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

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

class Solution:
    def wordBreak_v2_context_4k(self, s: str, wordDict: List[str]) -> bool:
        trie = Trie()
        for word in wordDict:
            if word:
                trie.insert(word)

        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and trie.search(s[j:i]):
                    dp[i] = True
                    break

        return dp[n]

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word