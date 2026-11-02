import random
import os

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

# Initialize the board
board = [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(NUM_COLUMNS)))
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

def drop_checker(column_idx, player_symbol):
    for row_idx in reversed(range(NUM_ROWS)):
        if board[row_idx][column_idx] == " ":
            board[row_idx][column_idx] = player_symbol
            return True
    return False

def check_win():
    # Check horizontal win
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if row[col] != " " and row[col] == row[col + 1] == row[col + 2] == row[col + 3]:
                return True

    # Check vertical win
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] != " " and board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != " " and board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] != " " and board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return True

    return False

def check_draw():
    for row in board:
        if " " in row:
            return False
    return True

def get_valid_column():
    while True:
        column_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        if len(column_input) == 1 and column_input.isalpha():
            column_idx = ord(column_input) - ord('A')
            if 0 <= column_idx < NUM_COLUMNS:
                return column_idx
        print("Invalid input. Please choose a valid column.")

# Randomly select first player
random.shuffle(PLAYER_SYMBOLS)
current_player = 0
current_symbol = PLAYER_SYMBOLS[current_player]

# Printing initial board
print_board()

# Game loop
while True:
    column = get_valid_column()
    if drop_checker(column, current_symbol):
        print_board()
        if check_win():
            print(f"Player {current_symbol} won!")
            break
        if check_draw():
            print("The game is a draw!")
            break
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS
        current_symbol = PLAYER_SYMBOLS[current_player]
    else:
        print("Column is full. Please choose another column.")
