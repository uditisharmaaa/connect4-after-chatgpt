import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Extend this for more players if needed

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("|" + "|".join(row) + "|")
        print("+" + "---+" * COLS)

def get_valid_input():
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            col_index = ord(column) - 65
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full, please choose another column.")
        else:
            print("Invalid input, please enter a letter A-G.")

def place_checker(col_index):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = current_player
            return True
    return False

def check_win():
    # Check horizontal, vertical, and diagonal for wins
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == current_player and board[r][c + 1] == current_player and \
               board[r][c + 2] == current_player and board[r][c + 3] == current_player:
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == current_player and board[r + 1][c] == current_player and \
               board[r + 2][c] == current_player and board[r + 3][c] == current_player:
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == current_player and board[r + 1][c + 1] == current_player and \
               board[r + 2][c + 2] == current_player and board[r + 3][c + 3] == current_player:
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == current_player and board[r - 1][c + 1] == current_player and \
               board[r - 2][c + 2] == current_player and board[r - 3][c + 3] == current_player:
                return True

    return False

def check_draw():
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game loop
board = create_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col_index = get_valid_input()
    place_checker(col_index)
    print_board(board)

    if check_win():
        print(f"Player {current_player} won!")
        break

    if check_draw():
        print("It's a draw!")
        break

    # Switch player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
