import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    header = "  ".join(COLUMN_LABELS)
    separator = "+---" * COLUMNS + "+"
    clear_screen()
    print(f"  {header}")
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def drop_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_valid_column_input():
    while True:
        user_input = input("Please enter a column: ").strip()
        if user_input not in COLUMN_LABELS:
            print("Invalid input. Please enter a valid column letter.")
        else:
            col_index = COLUMN_LABELS.index(user_input)
            if all(board[row][col_index] != " " for row in range(ROWS)):
                print("Column is full. Choose another column.")
            else:
                return col_index

# Initialization
board = initialize_board()
current_player = random.randint(0, PLAYERS - 1)

# Game loop
while True:
    print_board(board)
    print(f"Player {CHECKERS[current_player]}'s turn.")
    col = get_valid_column_input()
    if drop_checker(board, col, CHECKERS[current_player]):
        if check_for_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS
