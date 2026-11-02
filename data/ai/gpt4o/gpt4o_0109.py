import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

# Initialize the board
def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Validate user input
def validate_input(column):
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < COLUMNS

# Drop checker in the selected column
def drop_checker(board, column, player):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = CHECKERS[player]
            return True
    return False

# Check for a win condition
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontally, vertically and diagonally
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c+i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4))) or \
               (c + 3 < COLUMNS and r + 3 < ROWS and all(board[r+i][c+i] == checker for i in range(4))) or \
               (c - 3 >= 0 and r + 3 < ROWS and all(board[r+i][c-i] == checker for i in range(4))):
                return True
    return False

# Check for draw condition (board full)
def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
    board = initialize_board()
    player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        column = input(f"Player {CHECKERS[player]}, please enter a column: ")
        if not validate_input(column):
            continue
        if not drop_checker(board, column, player):
            continue
        print_board(board)
        if check_win(board, player):
            print(f"Player {CHECKERS[player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        player = (player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
