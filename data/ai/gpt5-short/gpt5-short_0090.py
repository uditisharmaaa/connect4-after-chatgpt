# Connect 4 (6x7) with 2–5 players for Intro CS
# - Columns labeled A–G
# - Players use symbols from PLAYER_SYMBOLS in order
# - Number of players set by NUM_PLAYERS (2–5)
# - Random first player
# - Validates input and checks for wins/draws
# - Clears screen with os.system('clear') each turn

import os
import random
import sys

# ==========================
# Configuration constants
# ==========================
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A', 'B', ..., 'G']

# Symbols available for players (in order). Adjust if you like.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Set how many players are in the game (between 2 and 5).
NUM_PLAYERS = 2  # Change to 3, 4, or 5 if desired.

# Character used for empty cells
EMPTY = '.'


# ==========================
# Utility functions
# ==========================
def clear_screen():
    """Clear the terminal screen (Unix/macOS)."""
    os.system('clear')


def create_board():
    """Create an empty board as a list of lists (ROWS x COLS) filled with EMPTY."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board, current_player_symbol=None, first_player_symbol=None):
    """Print the board with column labels. Optionally show current and first player info."""
    # Header
    print('  ' + ' '.join(COLUMN_LABELS))
    # Rows (top to bottom)
    for r in range(ROWS):
        print(f'{ROWS - r} ' + ' '.join(board[r]))
    # Footer line for clarity
    print('  ' + ' '.join(COLUMN_LABELS))
    if first_player_symbol is not None:
        print(f'First player this game: {first_player_symbol}')
    if current_player_symbol is not None:
        print(f"Current player: {current_player_symbol}")


def letter_to_col(letter):
    """Convert column letter (A-G) to column index 0-6. Returns None if invalid."""
    if len(letter) != 1:
        return None
    letter = letter.upper()
    if letter in COLUMN_LABELS:
        return ord(letter) - ord('A')
    return None


def get_next_open_row(board, col):
    """Return the row index where a piece will land in the given column, or None if column is full."""
    # Start from bottom (last row) and find first EMPTY
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def apply_move(board, col, symbol):
    """Drop a piece with 'symbol' into column 'col'. Returns (row, col) or raises ValueError if invalid."""
    if not (0 <= col < COLS):
        raise ValueError("Column out of range.")
    row = get_next_open_row(board, col)
    if row is None:
        raise ValueError("Column is full.")
    board[row][col] = symbol
    return row, col


def count_direction(board, row, col, dr, dc, symbol):
    """
    Count consecutive pieces matching 'symbol' starting at (row, col),
    moving in direction (dr, dc), inclusive of starting cell.
    """
    r, c = row, col
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, row, col, symbol):
    """
    Check if placing 'symbol' at (row, col) creates a connect-4 in any direction.
    We count both directions for each axis and subtract 1 to avoid double-counting the start.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = (
            count_direction(board, row, col, dr, dc, symbol) +
            count_direction(board, row, col, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False


def is_draw(board):
    """Return True if the board is full (no EMPTY cells in top row)."""
    # If any cell in the top row is EMPTY, then there is still room
    return all(board[0][c] != EMPTY for c in range(COLS))


def validate_settings():
    """Validate NUM_PLAYERS and PLAYER_SYMBOLS configuration."""
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Error: Not enough PLAYER_SYMBOLS for NUM_PLAYERS.", file=sys.stderr)
        sys.exit(1)
    # Ensure symbols are 1-char and unique for clarity
    if any(len(s) != 1 for s in PLAYER_SYMBOLS[:NUM_PLAYERS]):
        print("Error: PLAYER_SYMBOLS must be single-character strings.", file=sys.stderr)
        sys.exit(1)
    if len(set(PLAYER_SYMBOLS[:NUM_PLAYERS])) != NUM_PLAYERS:
        print("Error: PLAYER_SYMBOLS must be unique.", file=sys.stderr)
        sys.exit(1)


def prompt_for_move(current_symbol):
    """
    Prompt the current player for a move.
    - Accepts a single letter A-G (case-insensitive).
    - Keeps prompting until valid.
    Returns column index (0-6).
    """
    while True:
        raw = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
        col = letter_to_col(raw)
        if col is None:
            print("Invalid input. Please enter a letter A-G.")
            continue
        return col


# ==========================
# Game loop
# ==========================
def play_game():
    validate_settings()
    board = create_board()

    # Determine player order and random starting index
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    start_index = random.randrange(NUM_PLAYERS)
    current_index = start_index

    # Keep a copy of who started for display
    first_player_symbol = players[start_index]

    while True:
        clear_screen()
        print_board(board, current_player_symbol=players[current_index], first_player_symbol=first_player_symbol)

        # Get a valid move (column with space)
        while True:
            col = prompt_for_move(players[current_index])
            try:
                # Test if move is possible without committing first
                row = get_next_open_row(board, col)
                if row is None:
                    print("That column is full. Try a different one.")
                    continue
                # Apply move
                row, col = apply_move(board, col, players[current_index])
                break
            except ValueError as e:
                print(f"Invalid move: {e}")

        # After move, clear and reprint board so the move is visible immediately
        clear_screen()
        print_board(board, current_player_symbol=players[current_index], first_player_symbol=first_player_symbol)

        # Check for win
        if is_winning_move(board, row, col, players[current_index]):
            print(f"Player {players[current_index]} wins! Connect 4 achieved.")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw! The board is full.")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
