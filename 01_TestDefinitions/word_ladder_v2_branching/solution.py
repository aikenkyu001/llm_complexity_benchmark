from typing import List, Set, Dict

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        # Helper function to check if two words differ by exactly one character
        def is_forbidden(word1: str, word2: str) -> bool:
            diff_count = 0
            for c1, c2 in zip(word1, word2):
                if c1 != c2:
                    diff_count += 1
                    if diff_count > 1:
                        return True
            return False
        
        # Initialize the bidirectional BFS
        forward_queue = collections.deque([beginWord])
        backward_queue = collections.deque([endWord])
        forward_visited = {beginWord}
        backward_visited = {endWord}
        level = 2
        
        while forward_queue and backward_queue:
            if len(forward_queue) > len(backward_queue):
                forward_queue, backward_queue = backward_queue, forward_queue
                forward_visited, backward_visited = backward_visited, forward_visited
            
            for _ in range(len(forward_queue)):
                current_word = forward_queue.popleft()
                
                # Generate all possible one-character transformations
                for i in range(len(current_word)):
                    for j in 'abcdefghijklmnopqrstuvwxyz':
                        next_word = current_word[:i] + j + current_word[i+1:]
                        
                        if next_word in backward_visited:
                            return level
                        
                        if next_word in wordList and next_word not in forward_visited:
                            if not is_forbidden(current_word, next_word):
                                forward_queue.append(next_word)
                                forward_visited.add(next_word)
            
            level += 1
        
        return 0