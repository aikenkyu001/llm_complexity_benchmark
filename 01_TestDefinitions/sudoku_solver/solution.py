from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        
        def is_valid(board, row, col, num):
            # Check if the number is not in the current row
            for i in range(9):
                if board[row][i] == num:
                    return False
            
            # Check if the number is not in the current column
            for i in range(9):
                if board[i][col] == num:
                    return False
            
            # Check if the number is not in the current 3x3 sub-box
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[i + start_row][j + start_col] == num:
                        return False
            
            return True
        
        def solve():
            for row in range(9):
                for col in range(9):
                    if board[row][col] == '.':
                        for num in '123456789':
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve():
                                    return True
                                board[row][col] = '.'
                        return False
            return True
        
        solve()