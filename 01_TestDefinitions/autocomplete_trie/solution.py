from typing import List, Optional, Dict, Set, Any
import heapq
import collections

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.sentences: Dict[str, int] = {}

class Solution:
    def __init__(self):
        self.root = TrieNode()

    def initAutocomplete(self, sentences: List[str], times: List[int]) -> None:
        for sentence, time in zip(sentences, times):
            node = self.root
            for char in sentence:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.sentences[sentence] = node.sentences.get(sentence, 0) + time

    def query(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Retrieve the top 3 sentences based on frequency and lexicographical order
        top_sentences = heapq.nsmallest(3, node.sentences.items(), key=lambda x: (-x[1], x[0]))
        return [sentence for sentence, _ in top_sentences]