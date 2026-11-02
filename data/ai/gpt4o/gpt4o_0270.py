import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support up to 5 players
COLUMN_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(COLUMN_LABELS[:COLUMNS]))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(column):
    return 0 <= column < COLUMNS

def is_column_full(board, column):
    return board[0][column] != ' '

def get_valid_column_input():
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) == 1 and user_input in COLUMN_LABELS[:COLUMNS]:
            column = COLUMN_LABELS.index(user_input)
            if not is_column_full(board, column):
                return column
        print("Invalid column, try again.")

def place_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = checker
            return

def check_winner(board, checker):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(is_column_full(board, c) for c in range(COLUMNS))

def toggle_player(current_player, player_count):
    return (current_player + 1) % player_count

# Initialize game
board = create_board()
current_player = random.randint(0, PLAYER_COUNT - 1)

# Main game loop
clear_screen()
print_board(board)

while True:
    print(f"Player {CHECKERS[current_player]}'s turn.")
    
    # Get player input
    column = get_valid_column_input()
    
    # Place checker
    place_checker(board, column, CHECKERS[current_player])
    
    # Clear and print the board
    clear_screen()
    print_board(board)
    
    # Check win condition
    if check_winner(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    
    # Check draw condition
    if is_draw(board):
        print("The game is a draw!")
        break
    
    # Switch player
    current_player = toggle_player(current_player, PLAYER_COUNT)
