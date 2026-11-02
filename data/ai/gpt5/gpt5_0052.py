import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                  # number of rows (height)
COLS = 7                  # number of columns (width) - max 26
NUM_PLAYERS = 2           # allowed: 2..5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4            # keep 4 per spec


# =========================
# Utility functions
# =========================
def clear_screen():
    # Clear terminal screen (Linux/Unix as per assignment)
    os.system('clear')


def column_letters(n_cols):
    # Return list of column letters from 'A'
    if n_cols > 26:
        raise ValueError("Maximum supported columns is 26.")
    return list(string.ascii_uppercase[:n_cols])


def create_board(rows, cols):
    # Board is a list of rows; each row is a list of cell strings
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    letters = column_letters(cols)

    # Header letters line (as in example)
    # Two leading spaces then each letter centered within a 3-wide cell
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        line_cells = []
        for c in range(cols):
            line_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(line_cells) + "|")
        print(sep)


def is_draw(board):
    # If top row has no spaces, the board is full
    top_row = board[0]
    return all(cell != " " for cell in top_row)


def place_checker(board, col_idx, symbol):
    # Place symbol in the lowest empty cell of column col_idx
    # Return (row_index) if placed, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = symbol
            return r
    return None


def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def check_winner(board, last_r, last_c):
    # Check 4-in-a-row for the symbol placed at (last_r, last_c)
    symbol = board[last_r][last_c]
    if symbol == " ":
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for dr, dc in directions:
        count = 1  # include the last placed piece

        # Forward direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Backward direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def get_valid_column_input(valid_letters):
    # Keep asking for input until user provides a single valid column letter.
    # The caller will handle the case where the chosen valid column is full.
    while True:
        user_in = input("Please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue
        # Accept lower/upper, normalize to upper
        letter = user_in.upper()
        if letter not in valid_letters:
            print(f"Invalid column. Choose one of: {', '.join(valid_letters)}")
            continue
        return letter


def game_loop(rows, cols, num_players):
    # Validate configuration
    if not (2 <= num_players <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= cols <= 26):
        print("COLS must be between 1 and 26.")
        sys.exit(1)

    board = create_board(rows, cols)
    letters = column_letters(cols)
    symbols = PLAYER_SYMBOLS[:num_players]

    # Randomly pick starting player
    current_idx = random.randrange(num_players)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {symbols[current_idx]}, please enter a column:")

    while True:
        # Prompt input for current player
        col_letter = get_valid_column_input(letters)
        col_idx = letters.index(col_letter)

        # Try place checker
        placed_row = place_checker(board, col_idx, symbols[current_idx])

        if placed_row is None:
            # Column full: turn is invalid, player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {col_letter} is full. Player {symbols[current_idx]} loses the turn.")
            # Next player
            current_idx = (current_idx + 1) % num_players
            print(f"Player {symbols[current_idx]}, please enter a column:")
            continue

        # After successful placement: check for win/draw
        clear_screen()
        print_board(board)

        if check_winner(board, placed_row, col_idx):
            print(f"Player {symbols[current_idx]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % num_players
        print(f"Player {symbols[current_idx]}, please enter a column:")


def main():
    random.seed()  # initialize RNG
    game_loop(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
