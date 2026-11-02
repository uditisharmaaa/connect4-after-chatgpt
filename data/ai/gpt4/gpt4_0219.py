import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Creates an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')
    # Print column headers (A, B, C, etc.)
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + COLS)))
    print("+" + "---+" * COLS)
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column, board):
    """Checks if a column is valid and has space for a checker."""
    return 0 <= column < COLS and board[0][column] == " "

def drop_checker(board, col, symbol):
    """Drops the checker into the correct position in the column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return

def check_win(board, player_symbol):
    """Checks for a win horizontally, vertically, or diagonally."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (board full)."""
    for row in board:
        if " " in row:
            return False
    return True

def get_column_from_input(player_symbol):
    """Prompts the current player for a column."""
    while True:
        try:
            column = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
            if len(column) != 1 or not ('A' <= column <= chr(ord('A') + COLS - 1)):
                raise ValueError("Invalid column. Please enter a valid letter.")
            return ord(column) - ord('A')
        except ValueError as e:
            print(e)

def main():
    # Initialize the game
    board = create_board(ROWS, COLS)
    num_players = 2
    player_symbols = PLAYER_SYMBOLS[:num_players]

    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)

    # Start the game
    print_board(board)
    while True:
        # Prompt the current player for a column
        col = get_column_from_input(player_symbols[current_player])

        # Check if the column is valid
        if not is_valid_column(col, board):
            print("Column is full or invalid. Try again.")
            continue

        # Drop the checker in the column
        drop_checker(board, col, player_symbols[current_player])
        print_board(board)

        # Check for a win
        if check_win(board, player_symbols[current_player]):
            print(f"Player {player_symbols[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
