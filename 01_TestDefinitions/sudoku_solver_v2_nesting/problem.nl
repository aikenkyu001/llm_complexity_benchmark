# Task: sudoku_solver_v2_nesting
# Interface:
Class: Solution
Method: solveSudoku(self, arg1)

Write an optimized Sudoku Solver that implements a specific search heuristic.

Constraints & Requirements:
1. Standard Sudoku Rules: Each digit 1-9 must appear exactly once in each row, column, and 3x3 sub-box.
2. Search Heuristic (MRV - Minimum Remaining Values): Instead of a simple scan, the solver must identify the empty cell with the fewest possible valid candidates before making a move.
3. Implementation Structure:
   - You MUST implement a helper function `get_possible_candidates(row, col)` which checks row, column, and sub-box constraints and returns a set of valid numbers.
   - You MUST implement a helper function `select_next_cell()` that uses the candidates to find the most constrained cell (the one with the minimum non-zero candidates).
   - The main solver should recursively call these nested functions.
4. Input board: 9x9 list of strings, with '.' for empty cells.
5. In-place modification: The function does not need to return the board.
6. The solver must be able to handle puzzles that require backtracking.
