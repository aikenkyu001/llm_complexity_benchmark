from typing import List, Set

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Solves the Sudoku puzzle in-place.
        
        :param board: A 9x9 list of strings representing the Sudoku board.
        """
        self.board = board
        self.solve()

    def solve(self) -> bool:
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True
        row, col = empty_cell

        for num in '123456789':
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = '.'
        return False

    def find_empty_cell(self) -> Optional[Tuple[int, int]]:
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == '.':
                    return (row, col)
        return None

    def is_valid(self, row: int, col: int, num: str) -> bool:
        # Check the row
        for i in range(9):
            if self.board[row][i] == num:
                return False
        
        # Check the column
        for i in range(9):
            if self.board[i][col] == num:
                return False
        
        # Check the 3x3 sub-box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        
        return True