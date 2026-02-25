from typing import List, Tuple

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
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Build the Trie from the list of words
        trie = Trie()
        for word in words:
            trie.insert(word)
        
        m, n = len(board), len(board[0])
        result: Set[str] = set()
        visited: List[List[bool]] = [[False] * n for _ in range(m)]
        
        def dfs(x: int, y: int, path: str, node: TrieNode) -> None:
            if node.is_end_of_word:
                result.add(path)
            
            # Mark the current cell as visited
            visited[x][y] = True
            
            # Explore all 4 possible directions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and board[nx][ny] in node.children:
                    dfs(nx, ny, path + board[nx][ny], node.children[board[nx][ny]])
            
            # Unmark the current cell as visited (backtrack)
            visited[x][y] = False
        
        # Start DFS from each cell in the board
        for i in range(m):
            for j in range(n):
                if board[i][j] in trie.root.children:
                    dfs(i, j, board[i][j], trie.root.children[board[i][j]])
        
        return list(result)