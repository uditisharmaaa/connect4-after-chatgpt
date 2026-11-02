import os
import random
import string
import sys

# -----------------------------
# Configuration (constants)
# -----------------------------
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 per specification

# -----------------------------
# Validation of configuration
# -----------------------------
if COLUMNS < 1 or COLUMNS > 26:
    print("Error: COLUMNS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if NUM_PLAYERS > len(CHECKERS):
    print("Error: Not enough checker symbols for the number of players.")
    sys.exit(1)

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


# -----------------------------
# Game utility functions
# -----------------------------
def clear_screen():
    # Per assignment requirement: use os.system('clear')
    os.system('clear')


def create_board(rows, cols):
    # Create a rows x cols board initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (A, B, C, ...)
    headers = list(string.ascii_uppercase[:cols])
    header_line = "  " + "   ".join(headers)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header_line)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep_line)


def column_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1 or not letter.isalpha():
        return None
    idx = ord(letter) - ord('A')
    return idx if 0 <= idx < COLUMNS else None


def get_valid_column_input(current_player_symbol):
    # Prompt until the user provides a valid column letter within range
    while True:
        user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip()
        # Treat empty as invalid
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        idx = column_letter_to_index(user_input)
        if idx is None:
            print("Invalid input. Please enter a valid column letter within the board range.")
            continue
        return idx


def drop_checker(board, col_idx, symbol):
    # Attempt to drop a checker into the specified column.
    # Returns the (row, col) position if placed, or None if column is full.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = symbol
            return (row, col_idx)
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, last_row, last_col, symbol):
    # Check for WIN_LENGTH in a row including last placed symbol.
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # count the last placed piece
        # check forward direction
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # check backward direction
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False


def check_draw(board):
    # The game is a draw if there is no space left on the board
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# -----------------------------
# Main Game Loop
# -----------------------------
def main():
    board = create_board(ROWS, COLUMNS)
    # Randomly select the first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_idx]

        # Get a valid column letter from the current player
        col_idx = get_valid_column_input(current_symbol)

        # Try to place the checker
        placement = drop_checker(board, col_idx, current_symbol)

        clear_screen()
        print_board(board)

        if placement is None:
            # Column is full; player loses the turn
            col_letter = string.ascii_uppercase[col_idx]
            print(f"Column {col_letter} is full. Player {current_symbol} loses the turn.")
            # Move to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for a win after a successful move
        last_row, last_col = placement
        if check_win(board, last_row, last_col, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
