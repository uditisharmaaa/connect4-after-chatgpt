import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = 2  # Number of players
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Get the lowest available row in a column
def get_available_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            return row
    return -1

# Check for a win (horizontal, vertical, diagonal)
def check_winner(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][c] == symbol for c in range(col, col + 4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[r][col] == symbol for r in range(row, row + 4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Get valid column input from player
def get_valid_column_input(board):
    while True:
        col_input = input("Please enter a column (e.g., A-G): ").strip().upper()
        if col_input in COLUMN_LABELS:
            col = COLUMN_LABELS.index(col_input)
            if get_available_row(board, col) != -1:
                return col
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select starting player
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}'s turn.")
        col = get_valid_column_input(board)
        row = get_available_row(board, col)
        board[row][col] = CHECKERS[current_player]
        print_board(board)

        # Check for win or draw
        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate turn
        current_player = (current_player + 1) % PLAYERS

# Setup game
def main():
    if PLAYERS < 2 or PLAYERS > MAX_PLAYERS:
        print(f"Error: Number of players must be between 2 and {MAX_PLAYERS}.")
        return
    if COLS > 26:
        print("Error: Number of columns must not exceed 26.")
        return
    play_game()

if __name__ == "__main__":
    main()
