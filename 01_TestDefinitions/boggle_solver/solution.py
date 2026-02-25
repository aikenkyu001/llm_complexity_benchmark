from typing import List

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
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Build the Trie from the list of words
        trie = Trie()
        for word in words:
            trie.insert(word)
        
        m, n = len(board), len(board[0])
        result = set()
        visited = [[False] * n for _ in range(m)]
        
        def dfs(x: int, y: int, node: TrieNode, path: str) -> None:
            if node.is_end_of_word:
                result.add(path)
            
            # Explore neighbors
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                    char = board[nx][ny]
                    if char in node.children:
                        visited[nx][ny] = True
                        dfs(nx, ny, node.children[char], path + char)
                        visited[nx][ny] = False
        
        # Start DFS from each cell on the board
        for i in range(m):
            for j in range(n):
                if board[i][j] in trie.root.children:
                    visited[i][j] = True
                    dfs(i, j, trie.root.children[board[i][j]], board[i][j])
                    visited[i][j] = False
        
        return list(result)