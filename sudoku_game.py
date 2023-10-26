# sudoku_game.py

import random
from copy import deepcopy

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def is_valid_move(board, row, col, num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():
    # Create a solved Sudoku puzzle
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)

    # Create a list of shuffled numbers
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for row in board:
        for i in range(len(row)):
            if row[i] != 0:
                row[i] = numbers[row[i] - 1]

    # Remove a random number of cells while ensuring the puzzle remains solvable
    num_to_remove = random.randint(40, 50)  # Adjust the range as desired
    cells_to_remove = random.sample(range(81), num_to_remove)

    for cell in cells_to_remove:
        row, col = divmod(cell, 9)
        board[row][col] = 0

    return board
