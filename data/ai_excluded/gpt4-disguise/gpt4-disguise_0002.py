import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# Functions
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col):
    return col.isalpha() and len(col) == 1 and 0 <= ord(col.upper()) - 65 < COLS

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal top-left to bottom-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal bottom-left to top-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
board = create_board()
current_player = random.randint(0, PLAYERS - 1)

print_board(board)
while True:
    print(f"Player {CHECKERS[current_player]}, please enter a column:")
    col_input = input().upper()
    
    if not is_valid_column(col_input):
        print("Invalid input. Please enter an uppercase letter within the board range.")
        continue

    col = ord(col_input) - 65
    if not drop_checker(board, col, CHECKERS[current_player]):
        print("Column is full. Try a different one.")
        continue

    print_board(board)

    if check_winner(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    
    if is_draw(board):
        print("The game is a draw!")
        break

    current_player = (current_player + 1) % PLAYERS
