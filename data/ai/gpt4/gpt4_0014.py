import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + MAX_COLUMNS)]

# Functions
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column labels (A, B, ...)
    header = "   ".join(COLUMN_LABELS[:COLUMNS])
    print(f"  {header}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, columns):
    return column in COLUMN_LABELS[:columns]

def is_column_full(board, col_index):
    return board[0][col_index] != " "

def drop_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

# Main game logic
def connect4():
    # Initialize board
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    print_board(board)

    # Game loop
    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()

        # Validate input
        if not is_valid_column(user_input, COLUMNS):
            print("Invalid input. Please enter a valid column (e.g., A-G).")
            continue

        col_index = COLUMN_LABELS.index(user_input)

        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue

        # Place the checker
        drop_checker(board, col_index, current_player)
        print_board(board)

        # Check for a win
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

# Run the game
if __name__ == "__main__":
    connect4()
