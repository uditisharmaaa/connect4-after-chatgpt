import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column headers
    print("+---" * COLS + "+")  # Top border
    for row in board:  # Print each row
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")  # Row separator

def get_valid_column():
    while True:
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            return ord(column) - 65
        else:
            print("Invalid input. Please enter a letter from A to " + chr(65 + COLS - 1))

def place_checker(board, column, player):
    for row in reversed(board):  # Start checking from the bottom
        if row[column] == " ":
            row[column] = player
            return True
    return False

def check_winner(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game logic
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)

while True:
    current_player = PLAYERS[current_player_index]
    print_board(board)
    
    column = get_valid_column()
    if not place_checker(board, column, current_player):
        print("Column is full! Try again.")
        continue

    if check_winner(board, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        break

    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    current_player_index = (current_player_index + 1) % len(PLAYERS)
