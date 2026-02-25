# solution.py
from typing import List, Optional, Dict, Set, Any
import heapq
import collections

class Node:
    def __init__(self, row: int, col: int, candidates: Set[str]):
        self.row = row
        self.col = col
        self.candidates = candidates

class Solution:
    def solveSudoku_v2_nesting(self, board: List[List[str]]) -> None:
        # Helper function to get possible candidates for a given cell
        def get_possible_candidates(row: int, col: int) -> Set[str]:
            candidates = set('123456789')
            # Check row
            for c in board[row]:
                if c != '.':
                    candidates.discard(c)
            # Check column
            for r in range(9):
                if board[r][col] != '.':
                    candidates.discard(board[r][col])
            # Check sub-box
            sub_box_row, sub_box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(sub_box_row, sub_box_row + 3):
                for j in range(sub_box_col, sub_box_col + 3):
                    if board[i][j] != '.':
                        candidates.discard(board[i][j])
            return candidates

        # Helper function to select the next cell with the fewest candidates
        def select_next_cell() -> Optional[Node]:
            min_candidates = float('inf')
            min_node = None
            for row in range(9):
                for col in range(9):
                    if board[row][col] == '.':
                        candidates = get_possible_candidates(row, col)
                        if len(candidates) < min_candidates:
                            min_candidates = len(candidates)
                            min_node = Node(row, col, candidates)
            return min_node

        # Main solver function
        def solve():
            if all('.' not in row for row in board):
                return True
            node = select_next_cell()
            if node is None:
                return False
            for candidate in node.candidates:
                board[node.row][node.col] = candidate
                if solve():
                    return True
                board[node.row][node.col] = '.'
            return False

        solve()