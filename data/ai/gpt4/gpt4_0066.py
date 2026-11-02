import os
import random

# Constants
ROWS = 6  # Number of rows
COLUMNS = 7  # Number of columns
NUM_PLAYERS = 2  # Number of players (can range from 2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for players
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # Column labels (A-G)

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if the move is valid
def is_valid_move(column, board):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == " "

# Place the checker in the selected column
def place_checker(column, player, board):
    col_idx = COLUMN_LABELS.index(column)
    for row in range(ROWS - 1, -1, -1):  # Place from bottom row upward
        if board[row][col_idx] == " ":
            board[row][col_idx] = CHECKERS[player]
            return True
    return False

# Check for a win condition
def check_win(board, player):
    checker = CHECKERS[player]

    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw condition
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game function
def connect4():
    # Initialize the game
    board = create_board()
    players = NUM_PLAYERS
    current_player = random.randint(0, players - 1)  # Randomly pick starting player

    # Game loop
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, it's your turn.")
        column = input("Please enter a column: ").upper()

        # Validate input
        while not is_valid_move(column, board):
            print("Invalid move. Try again.")
            column = input("Please enter a column: ").upper()

        # Place the checker
        place_checker(column, current_player, board)

        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % players

# Run the game
if __name__ == "__main__":
    connect4()
