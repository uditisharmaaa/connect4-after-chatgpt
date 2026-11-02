import os
import random
import sys
import time

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players (max 5 players)
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_idx in range(num_cols):
        sys.stdout.write(f"{chr(ord('A') + col_idx)}   ")
    sys.stdout.write("\n")

    # Print the board content
    for r_idx in range(num_rows):
        sys.stdout.write("+")
        for _ in range(num_cols):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for c_idx in range(num_cols):
            sys.stdout.write(f" {board[r_idx][c_idx]} |")
        sys.stdout.write("\n")

    # Print the bottom border
    sys.stdout.write("+")
    for _ in range(num_cols):
        sys.stdout.write("---+")
    sys.stdout.write("\n")


def is_valid_column_input(col_input, num_cols):
    """
    Validates if the user's column input is a single uppercase letter
    within the valid range of columns.

    Args:
        col_input (str): The user's raw input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based index of the column if valid, None otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return None
    col_input = col_input.upper()
    if 'A' <= col_input <= chr(ord('A') + num_cols - 1):
        return ord(col_input) - ord('A')
    return None


def get_next_available_row(board, col):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col (int): The 0-based column index.

    Returns:
        int or None: The 0-based row index if a spot is available,
                     None if the column is full.
    """
    num_rows = len(board)
    for row_idx in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col] == " ":
            return row_idx
    return None


def place_checker(board, row, col, checker):
    """
    Places a checker on the board at the specified row and column.

    Args:
        board (list): The game board.
        row (int): The 0-based row index.
        col (int): The 0-based column index.
        checker (str): The checker symbol ('X', 'O', etc.).
    """
    board[row][col] = checker


def check_win(board, checker):
    """
    Checks if the given checker has won the game.
    Checks horizontally, vertically, and diagonally.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check for N in a row
    def check_sequence(r, c, dr, dc):
        count = 0
        for i in range(WIN_CONDITION):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols and board[nr][nc] == checker:
                count += 1
            else:
                break
        return count == WIN_CONDITION

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if check_sequence(r, c, 0, 1):
                return True

    # Check vertical
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols):
            if check_sequence(r, c, 1, 0):
                return True

    # Check diagonal (positive slope)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if check_sequence(r, c, 1, 1):
                return True

    # Check diagonal (negative slope)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if check_sequence(r, c, -1, 1):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_idx]

    game_over = False
    message = ""

    while not game_over:
        print_board(board)
        if message:
            print(message)
            message = "" # Clear message after printing

        current_player_checker = PLAYER_CHECKERS[current_player_idx]
        sys.stdout.write(f"Player {current_player_checker}, please enter a column: ")
        col_input = input().strip()

        col = is_valid_column_input(col_input, NUM_COLS)

        if col is None:
            message = "Invalid input. Please enter a single letter (A-{}).".format(chr(ord('A') + NUM_COLS - 1))
            continue

        row = get_next_available_row(board, col)

        if row is None:
            message = "Column {} is full. Please choose another column.".format(col_input.upper())
            continue

        # Place the checker
        place_checker(board, row, col, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    sys.stdout.write("Press Enter to exit.")
    input()


if __name__ == "__main__":
    main()
