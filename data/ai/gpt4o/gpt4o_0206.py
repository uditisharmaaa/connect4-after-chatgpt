import os
import random

# Constants for the game setup
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = 2 # Number of players for the game, adjust as needed

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def init_board():
    # Create game board with empty spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input():
    while True:
        try:
            column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            if len(column) == 1 and 'A' <= column <= chr(ord('A') + COLS - 1):
                return ord(column) - ord('A')
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check horizontal, vertical, and both diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            # Horizontal
            if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                return True
            # Vertical
            if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                return True
            # Diagonal /
            if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            # Diagonal \
            if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Initialize the game
board = init_board()
current_player = random.randint(0, PLAYERS - 1)

# Game loop
while True:
    print_board(board)
    column = get_valid_input()
    if place_checker(board, column, CHECKERS[current_player]):
        if check_for_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS
    else:
        print("Column is full, turn lost.")
