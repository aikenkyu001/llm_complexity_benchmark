# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        trie = Trie()
        for word in words:
            trie.insert(word)

        m, n = len(board), len(board[0])
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        def dfs(x: int, y: int, node: TrieNode, path: List[str], visited: Set[tuple[int, int]]) -> None:
            if node.is_word:
                result.add(''.join(path))
                node.is_word = False  # Mark as visited to avoid revisiting

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    path.append(board[nx][ny])
                    dfs(nx, ny, node.children.get(board[nx][ny]), path, visited)
                    path.pop()
                    visited.remove((nx, ny))

        result = set()
        for i in range(m):
            for j in range(n):
                dfs(i, j, trie.root, [board[i][j]], {(i, j)})

        return list(result)