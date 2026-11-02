# Connect 4 (6x7) with 2–5 players for Intro CS
# - Columns labeled A-G
# - Player tokens are set by constants (X, O, V, H, M)
# - Random first player
# - Validates input and column fullness
# - Detects wins (4 in a row) and draws
# - Clears screen each turn with os.system('clear')
#
# Run this file with Python 3.

import os
import random
import sys

# ----------------------------
# Configuration constants
# ----------------------------
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must match NUM_COLS
EMPTY = "."                # Character to show empty cells

# Tokens for up to 5 players. Use the first NUM_PLAYERS from this list.
PLAYER_TOKENS = ("X", "O", "V", "H", "M")

# Set how many players are active in this match (between 2 and 5).
NUM_PLAYERS = 2  # You can change this to 3, 4, or 5 as desired.


# ----------------------------
# Utility and game functions
# ----------------------------

def clear_screen():
    """Clear the terminal screen using the Unix 'clear' command."""
    os.system('clear')


def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    """Create an empty board: a list of rows, each a list of cells."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board, players, current_idx):
    """Print the column labels, then the board grid."""
    header = "  " + " ".join(COLUMN_LABELS[:len(board[0])])
    print(header)
    for r in range(len(board)):
        print(f"{r+1} " + " ".join(board[r]))
    print()
    turn_info = f"Turn: Player {players[current_idx]}"
    print(turn_info)


def drop_token(board, col_index, token):
    """
    Drop a token into a column.
    Returns the row index where the token landed, or None if the column is full.
    """
    # Start from bottom row, find the first empty cell.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            board[row][col_index] = token
            return row
    return None  # Column is full


def in_bounds(r, c, rows, cols):
    """Check if (r, c) is inside the board."""
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    """
    Check if the given token has 4 in a row anywhere on the board.
    Directions to check:
      - Right (0, +1)
      - Down (+1, 0)
      - Down-Right (+1, +1)
      - Down-Left (+1, -1)
    """
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                # Try to extend 3 more steps in this direction
                for step in range(1, 4):
                    nr, nc = r + dr * step, c + dc * step
                    if not in_bounds(nr, nc, rows, cols):
                        break
                    if board[nr][nc] != token:
                        break
                    count += 1
                if count >= 4:
                    return True
    return False


def check_draw(board):
    """A draw occurs when no empty cells remain on the top row (board is full)."""
    # If any cell in the top row is EMPTY, it's not a draw.
    return all(cell != EMPTY for cell in board[0])


def get_col_index_from_input(user_input):
    """
    Convert a column letter (A-G) to a zero-based column index.
    Returns an integer index if valid, or None otherwise.
    """
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if user_input not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(user_input)


def validate_configuration():
    """Ensure constants are set correctly before starting the game."""
    if NUM_COLS != len(COLUMN_LABELS):
        raise ValueError("NUM_COLS must match the length of COLUMN_LABELS.")
    if not (2 <= NUM_PLAYERS <= len(PLAYER_TOKENS)):
        raise ValueError(f"NUM_PLAYERS must be between 2 and {len(PLAYER_TOKENS)}.")


def main():
    # Validate configuration
    try:
        validate_configuration()
    except ValueError as e:
        print("Configuration error:", e)
        sys.exit(1)

    # Active players for this game (first NUM_PLAYERS from PLAYER_TOKENS)
    players = list(PLAYER_TOKENS[:NUM_PLAYERS])

    # Create the game board
    board = create_board()

    # Randomize the first player
    current_idx = random.randint(0, len(players) - 1)

    # Game loop
    try:
        while True:
            clear_screen()
            print_board(board, players, current_idx)

            # Prompt the current player for a move
            token = players[current_idx]
            prompt = f"Player {token}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}), or Q to quit: "
            user_input = input(prompt).strip()

            # Allow the user to quit
            if user_input.lower() == 'q':
                clear_screen()
                print_board(board, players, current_idx)
                print("Game ended by user.")
                break

            # Validate column input
            col_index = get_col_index_from_input(user_input)
            if col_index is None:
                print(f"Invalid input. Please enter a single letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
                input("Press Enter to continue...")
                continue

            # Attempt to drop the token
            row_landed = drop_token(board, col_index, token)
            if row_landed is None:
                print("That column is full. Choose another column.")
                input("Press Enter to continue...")
                continue

            # Check for a win
            if check_win(board, token):
                clear_screen()
                print_board(board, players, current_idx)
                print(f"Player {token} wins! Congratulations!")
                break

            # Check for a draw
            if check_draw(board):
                clear_screen()
                print_board(board, players, current_idx)
                print("It's a draw! The board is full.")
                break

            # Next player's turn
            current_idx = (current_idx + 1) % len(players)

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        clear_screen()
        print("Game interrupted. Goodbye!")


if __name__ == "__main__":
    main()
