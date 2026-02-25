# Task: word_search_ii
# Interface:
Class: Solution
Method: findWords(self, arg1, arg2)

Given an m x n board of characters and a list of strings words, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
You should use a Trie data structure to optimize the search.

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 12
- board and words consist of lowercase English letters.
- 1 <= words.length <= 3 * 10^4
- All strings in words are unique.
