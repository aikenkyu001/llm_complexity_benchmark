# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

# Define any helper classes here if needed

class TrieNode:
    def __init__(self):
        self.children = {}
        self.hotness = 0
        self.sentences = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, sentence: str, count: int) -> None:
        node = self.root
        for char in sentence:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.hotness += count
            node.sentences.add(sentence)

    def search(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return sorted(node.sentences, key=lambda x: (-node.hotness, x))

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]) -> None:
        self.trie = Trie()
        for sentence, count in zip(sentences, times):
            self.trie.insert(sentence, count)
        self.current_prefix = ""

    def input(self, c: str) -> List[str]:
        if c == "#":
            self.trie.insert(self.current_prefix, 1)
            self.current_prefix = ""
            return []
        self.current_prefix += c
        return self.trie.search(self.current_prefix)

class Solution:
    def initAutocomplete(self, sentences: List[str], times: List[int]) -> AutocompleteSystem:
        return AutocompleteSystem(sentences, times)