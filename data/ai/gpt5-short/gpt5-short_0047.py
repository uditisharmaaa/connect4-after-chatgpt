import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = tuple("ABCDEFG")  # Must be length COLS
PLAYER_TOKENS = ("X", "O", "V", "H", "M")  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5 for number of players in this game

# =========================
# Utility functions
# =========================
def clear_screen():
    """
    Clear the terminal screen. Uses 'clear' as requested.
    Attempts a Windows fallback to 'cls' if needed.
    """
    # Primary per assignment
    if os.system("clear") != 0:
        # Fallback for Windows if 'clear' is unavailable
        os.system("cls")


def create_board(rows=ROWS, cols=COLS):
    """Create and return an empty game board (list of lists)."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the game board with column labels."""
    # Header
    print("   " + " ".join(COLUMN_LABELS))
    print("  +" + "-".join(["-"] * COLS) + "+")
    # Rows
    for r in range(ROWS):
        row_str = "  |" + "|".join(board[r]) + "|"
        print(row_str)
    print("  +" + "-".join(["-"] * COLS) + "+")


def col_label_to_index(label):
    """Convert a column label (A-G) to a 0-based column index. Returns None if invalid."""
    if not label or len(label) != 1:
        return None
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None


def is_valid_column(col, board):
    """Return True if a piece can be dropped in the given column index."""
    if col is None or not (0 <= col < COLS):
        return False
    # Column is valid if top cell is empty
    return board[0][col] == " "


def drop_piece(board, col, token):
    """
    Drop a piece with the given token into the column.
    Returns the row index where the piece landed, or None if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = token
            return row
    return None


def count_in_direction(board, start_r, start_c, dr, dc, token):
    """
    Count contiguous tokens equal to 'token' starting one step from (start_r, start_c)
    in direction (dr, dc).
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_winner(board, last_r, last_c, token):
    """
    Check if placing 'token' at (last_r, last_c) created a connect-4.
    Returns True if the player won.
    """
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # Include the last placed piece
        total += count_in_direction(board, last_r, last_c, dr, dc, token)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= 4:
            return True
    return False


def check_draw(board):
    """Return True if the board is full (draw)."""
    # If any top cell is empty, it's not a draw
    return all(board[0][c] != " " for c in range(COLS))


def get_move_input(current_token, board):
    """
    Prompt the current player for a move and validate it.
    Returns a valid column index, or None if the player chose to quit.
    """
    while True:
        user_in = input(f"Player {current_token}, choose a column (A-{COLUMN_LABELS[-1]}) or Q to quit: ").strip().upper()
        if user_in == "Q":
            return None
        col = col_label_to_index(user_in)
        if col is None:
            print(f"Invalid input. Please enter a single letter A-{COLUMN_LABELS[-1]}, or Q to quit.")
            continue
        if not is_valid_column(col, board):
            print("That column is full or invalid. Try another column.")
            continue
        return col


def validate_configuration():
    """Validate constants and configuration, exit with message if invalid."""
    if COLS != len(COLUMN_LABELS):
        print("Configuration error: COLS must match the length of COLUMN_LABELS.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Configuration error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_TOKENS):
        print("Configuration error: NUM_PLAYERS exceeds number of PLAYER_TOKENS provided.")
        sys.exit(1)
    # Ensure all tokens are single characters and distinct
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    if any((not isinstance(t, str) or len(t) != 1) for t in tokens) or len(set(tokens)) != len(tokens):
        print("Configuration error: PLAYER_TOKENS must be unique single-character symbols.")
        sys.exit(1)


def main():
    validate_configuration()
    tokens = list(PLAYER_TOKENS[:NUM_PLAYERS])

    board = create_board()
    current_idx = random.randrange(NUM_PLAYERS)  # Random first player

    # Game loop
    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {', '.join(tokens)}  |  First to connect 4 wins")
        print_board(board)
        print(f"Current turn: Player {tokens[current_idx]}")

        col = get_move_input(tokens[current_idx], board)
        if col is None:
            print("Game ended by user.")
            break

        row = drop_piece(board, col, tokens[current_idx])
        # row should not be None here due to validation, but check defensively
        if row is None:
            print("Unexpected error dropping piece. Try again.")
            continue

        # Check win
        if check_winner(board, row, col, tokens[current_idx]):
            clear_screen()
            print_board(board)
            print(f"Player {tokens[current_idx]} wins! Congratulations!")
            break

        # Check draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more valid moves.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
