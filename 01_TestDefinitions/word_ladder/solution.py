from typing import List, Set

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        # Create a set for quick lookup of words in the word list
        word_set = set(wordList)
        
        # Initialize BFS queue with the start word and level 1
        queue = collections.deque([(beginWord, 1)])
        
        # Perform BFS
        while queue:
            current_word, level = queue.popleft()
            
            # Try to transform each character of the current word
            for i in range(len(current_word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = current_word[:i] + c + current_word[i+1:]
                    
                    if next_word == endWord:
                        return level + 1
                    
                    if next_word in word_set:
                        queue.append((next_word, level + 1))
                        word_set.remove(next_word)
        
        # If no transformation sequence is found
        return 0