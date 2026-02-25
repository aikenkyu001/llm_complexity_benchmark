import pytest
from solution import Solution

def boards_equal(board1, board2):
    for i in range(9):
        for j in range(9):
            if board1[i][j] != board2[i][j]:
                return False
    return True

def test_sudoku_v2_basic():
    solution = Solution()
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    expected_solution = [
        ["5","3","4","6","7","8","9","1","2"],
        ["6","7","2","1","9","5","3","4","8"],
        ["1","9","8","3","4","2","5","6","7"],
        ["8","5","9","7","6","1","4","2","3"],
        ["4","2","6","8","5","3","7","9","1"],
        ["7","1","3","9","2","4","8","5","6"],
        ["9","6","1","5","3","7","2","8","4"],
        ["2","8","7","4","1","9","6","3","5"],
        ["3","4","5","2","8","6","1","7","9"]
    ]
    solution.solveSudoku(board)
    assert boards_equal(board, expected_solution)

def test_sudoku_v2_hard():
    """A slightly harder board to test the heuristic's effectiveness."""
    solution = Solution()
    board = [
        [".",".","9","7","4","8",".",".","."],
        ["7",".",".",".",".",".",".",".","."],
        [".","2",".","1",".","9",".",".","."],
        [".",".","7",".",".",".","2","4","."],
        [".","6","4",".","1",".","5","9","."],
        [".","9","8",".",".",".","3",".","."],
        [".",".",".","8",".","3",".","2","."],
        [".",".",".",".",".",".",".",".","6"],
        [".",".",".","2","7","5","9",".","."]
    ]
    solution.solveSudoku(board)
    # Just check if it's a validly filled board as a proxy for success
    def is_valid_sudoku(b):
        for i in range(9):
            row = [x for x in b[i] if x != '.']
            if len(set(row)) != len(row): return False
            col = [b[j][i] for j in range(9) if b[j][i] != '.']
            if len(set(col)) != len(col): return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = [b[r][c] for r in range(i, i+3) for c in range(j, j+3) if b[r][c] != '.']
                if len(set(box)) != len(box): return False
        return all(all(c != '.' for c in row) for row in b)
    
    assert is_valid_sudoku(board)
