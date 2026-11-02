import os
import random
import sys

# -----------------------------
# Configuration (changeable)
# -----------------------------
ROWS = 6            # Number of rows (e.g., 6)
COLS = 7            # Number of columns (e.g., 7), max 26
NUM_PLAYERS = 2     # Number of players (2 to 5)

# -----------------------------
# Constants (do not change)
# -----------------------------
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "
WIN_LENGTH = 4      # Always 4-in-a-row to win


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def validate_configuration():
    """Validate initial configuration constants."""
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if ROWS < 1:
        raise ValueError("ROWS must be at least 1.")


def create_board(rows, cols):
    """Create a rows x cols board filled with spaces."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Return list of column labels ['A', 'B', ...]."""
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    """Print the board with headers and grid."""
    rows = len(board)
    cols = len(board[0]) if rows else 0
    labels = column_labels(cols)

    # Header row
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    # Each row
    for r in range(rows):
        line_cells = []
        for c in range(cols):
            line_cells.append(board[r][c])
        print("| " + " | ".join(line_cells) + " |")
        print("+" + ("---+" * cols))


def valid_column_input(inp, cols):
    """Validate that inp is a single letter corresponding to a column."""
    if not inp:
        return False
    inp = inp.strip().upper()
    if len(inp) != 1:
        return False
    if not ('A' <= inp <= chr(ord('A') + cols - 1)):
        return False
    return True


def get_column_index(inp):
    """Convert a column label to a zero-based index."""
    return ord(inp.strip().upper()) - ord('A')


def find_drop_row(board, col):
    """Return the row index where a checker would land in col, or None if full."""
    for r in range(len(board) - 1, -1, -1):  # start from bottom
        if board[r][col] == EMPTY:
            return r
    return None


def drop_checker(board, col, checker):
    """Place the checker in the specified column. Return (row, col) or None if column full."""
    r = find_drop_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return (r, col)


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, checker):
    """Count consecutive checkers from (start_r, start_c) in direction (dr, dc)."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def has_won(board, last_r, last_c):
    """Check if placing at (last_r, last_c) resulted in a win."""
    checker = board[last_r][last_c]
    if checker == EMPTY:
        return False

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for dr, dc in directions:
        # Count in both positive and negative directions, minus 1 to avoid double-counting the origin
        total = (
            check_direction(board, last_r, last_c, dr, dc, checker) +
            check_direction(board, last_r, last_c, -dr, -dc, checker) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    """Return True if the board is full (no EMPTY cells)."""
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def prompt_for_column(current_checker, cols):
    """Prompt the current player for a valid column letter. Repeat until valid."""
    labels = column_labels(cols)
    while True:
        inp = input(f"Player {current_checker}, please enter a column: ").strip()
        if valid_column_input(inp, cols):
            col = get_column_index(inp)
            return col
        else:
            print(f"Invalid input. Enter one of: {', '.join(labels)}")


def game_loop(rows, cols, players):
    """Main game loop."""
    board = create_board(rows, cols)
    checkers = CHECKERS[:players]
    current_idx = random.randrange(players)

    # Initial print before the game starts
    clear_screen()
    print_board(board)

    while True:
        current_checker = checkers[current_idx]

        # Prompt for valid column input
        col = prompt_for_column(current_checker, cols)

        # Attempt to drop checker
        drop_result = drop_checker(board, col, current_checker)
        if drop_result is None:
            # Column is full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            col_label = chr(ord('A') + col)
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            current_idx = (current_idx + 1) % players
            # Continue to next player's turn
            continue

        last_r, last_c = drop_result

        # Clear and show updated board after a successful move
        clear_screen()
        print_board(board)

        # Check for win
        if has_won(board, last_r, last_c):
            print(f"Player {current_checker} won!")
            return

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_idx = (current_idx + 1) % players


def main():
    try:
        validate_configuration()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    random.seed()  # Seed from system time or OS entropy
    game_loop(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
