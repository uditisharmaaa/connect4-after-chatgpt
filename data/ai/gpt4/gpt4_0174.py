import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Creates an empty board with given rows and columns."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop_checker(board, col, symbol):
    """Drops the checker in the lowest available position in the given column."""
    for row in reversed(board):  # Start from the bottom row
        if row[col] == " ":
            row[col] = symbol
            return True
    return False  # Column is full

def is_valid_column(col):
    """Checks if the column character is valid."""
    return col.isalpha() and ord(col.upper()) - 65 in range(COLS)

def is_column_full(board, col):
    """Checks if a specific column is full."""
    return board[0][col] != " "

def check_winner(board, symbol):
    """Checks if a player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
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

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Initialization
    num_players = 2  # Set this to the number of players (between 2 and MAX_PLAYERS)
    symbols = PLAYER_SYMBOLS[:num_players]
    board = create_board(ROWS, COLS)
    print_board(board)

    # Randomly choose the first player
    current_player = random.randint(0, num_players - 1)

    while True:
        # Show player's turn
        print(f"Player {symbols[current_player]}, please enter a column:")
        col_input = input().strip().upper()

        # Validate input
        if not is_valid_column(col_input):
            print("Invalid column. Try again.")
            continue

        col = ord(col_input) - 65  # Convert letter to column index
        if is_column_full(board, col):
            print("Column is full. Try again.")
            continue

        # Drop the checker
        drop_checker(board, col, symbols[current_player])
        print_board(board)

        # Check for a win
        if check_winner(board, symbols[current_player]):
            print(f"Player {symbols[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
