# Task: Word Ladder
# Interface:
Class: Solution
Method: ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int

# Objective:
A transformation sequence from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:
- Every adjacent pair of words differs by a single letter.
- Every `si` for `1 <= i <= sk` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.
- `sk == endWord`.
Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, or 0 if no such sequence exists.

# Strategy Hint:
Use Breadth-First Search (BFS) to find the shortest path. To efficiently find neighbors, consider pre-processing the word list or checking words with one-letter variations.

# Constraints:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All words in wordList are unique.
