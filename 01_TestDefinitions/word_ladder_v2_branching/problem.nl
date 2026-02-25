# Task: word_ladder_v2_branching
# Interface:
Class: Solution
Method: ladderLength(self, arg1, arg2, arg3)

Given two words, beginWord and endWord, and a dictionary's word list, find the length of the shortest transformation sequence from beginWord to endWord.
This is a complex version with multiple additional rules:
1. You MUST use a Bidirectional BFS to minimize the search space.
2. For each word transformation, you must check a 'forbidden_combinations' list (not provided, assume a helper `is_forbidden(word1, word2)` exists or handle it as a potential constraint).
3. The wordList can be very large; prioritize memory efficiency.
4. Return 0 if no path exists.

Constraints:
- Word length up to 20.
- wordList size up to 10^5.
- beginWord and endWord are different.
