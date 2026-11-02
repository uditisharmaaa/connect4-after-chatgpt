import os
import random
import sys

# -----------------------------
# Configuration (submission must be 6x7 and 2 players)
# -----------------------------
ROWS = 6
COLS = 7  # up to 26 supported
NUM_PLAYERS = 2  # between 2 and 5

# -----------------------------
# Constants and validations
# -----------------------------
WIN_LENGTH = 4
MAX_COLS = 26
CHECKERS = ["X", "O", "V", "H", "M"]

if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= ROWS and 1 <= COLS <= MAX_COLS):
    print(f"ROWS must be >= 1 and COLS must be between 1 and {MAX_COLS}.")
    sys.exit(1)

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]

# -----------------------------
# Utility functions
# -----------------------------
def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Column headers
    header = "  " + "   ".join(COL_LABELS)
    print(header)
    # Horizontal separator
    sep = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|"
        print(row_cells)
    print(sep)


def column_from_input(inp):
    # Expect a single letter A.. up to number of columns
    if len(inp) != 1 or not inp.isalpha():
        return None
    ch = inp.upper()
    if ch not in COL_LABELS:
        return None
    return ord(ch) - ord('A')


def lowest_empty_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, token):
    row = lowest_empty_row(board, col)
    if row is None:
        return None, None
    board[row][col] = token
    return row, col


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def count_in_direction(board, start_r, start_c, dr, dc, token):
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c):
    if last_r is None or last_c is None:
        return False
    token = board[last_r][last_c]
    if token == " ":
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        # Count both directions from the last placed position
        total = (
            count_in_direction(board, last_r, last_c, dr, dc, token) +
            count_in_direction(board, last_r, last_c, -dr, -dc, token) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))


def get_valid_input(player_token):
    # Keep asking until a syntactically valid column letter is given (input validation).
    # Note: If the chosen valid column is full, the move is lost (no re-prompt).
    while True:
        user_in = input(f"Player {player_token}, please enter a column: ").strip()
        col = column_from_input(user_in)
        if col is None:
            print("Invalid input. Please enter a single letter for a valid column (e.g., A, B, C).")
            continue
        return col


# -----------------------------
# Game loop
# -----------------------------
def main():
    board = create_board(ROWS, COLS)
    current_idx = random.randrange(NUM_PLAYERS)
    winner = None

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        token = PLAYER_TOKENS[current_idx]
        col = get_valid_input(token)

        placed_row, placed_col = drop_checker(board, col, token)
        if placed_row is None:
            # Column full => move lost
            clear_screen()
            print_board(board)
            print(f"Column {COL_LABELS[col]} is full. Player {token} loses the turn.")
        else:
            # Successful move
            clear_screen()
            print_board(board)

            if check_win(board, placed_row, placed_col):
                winner = token
                print(f"Player {winner} won!")
                break

            if board_full(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

    # End of game; no extra input required


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
