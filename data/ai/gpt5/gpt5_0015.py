import os
import random
import string
import sys

# =========================
# Configuration (Constants)
# =========================
ROWS = 6                # Default submission requirement: 6 rows
COLS = 7                # Default submission requirement: 7 columns (A-G)
NUM_PLAYERS = 2         # Default submission requirement: 2 players
TOKENS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Safety checks for constraints
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5 inclusive.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26 inclusive.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")


# =========================
# Board Utilities
# =========================
def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def column_labels(cols):
    """Return a list of column labels 'A'.. up to number of columns."""
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    """Pretty-print the board with column labels as specified."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header
    clear_screen()
    print("  " + "   ".join(labels))
    print("+" + ("---+" * cols))

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))


def is_within_board(row, col, rows, cols):
    """Check if (row, col) is inside the board."""
    return 0 <= row < rows and 0 <= col < cols


def drop_checker(board, col_index, token):
    """
    Attempt to drop a checker into the given column.
    Returns the row index where placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row going up
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return r
    return None  # Column full


# =========================
# Win and Draw Checking
# =========================
def check_direction(board, start_r, start_c, dr, dc, token):
    """
    Count consecutive 'token' checkers starting from (start_r, start_c)
    moving in direction (dr, dc).
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    count = 0
    while is_within_board(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, row, col):
    """
    After placing at (row, col), check if that move made 4 in a row in any direction.
    """
    token = board[row][col]
    if token == " ":
        return False

    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        # Count both positive and negative directions, subtract 1 to avoid double-count current cell
        count_pos = check_direction(board, row, col, dr, dc, token)
        count_neg = check_direction(board, row, col, -dr, -dc, token)
        if (count_pos + count_neg - 1) >= 4:
            return True

    return False


def is_draw(board):
    """The game is a draw if no empty cells exist in the top row (i.e., all columns are full)."""
    # If any top cell is empty, it's not a draw
    return all(cell != " " for cell in board[0])


# =========================
# Input Handling
# =========================
def prompt_for_column(current_player_token, cols):
    """
    Prompt the user for a valid column letter. Keep asking until valid.
    Returns the zero-based column index.
    """
    labels = column_labels(cols)
    label_set = set(labels)

    while True:
        try:
            user_input = input(f"Player {current_player_token}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting game.")
            sys.exit(0)

        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter between {labels[0]} and {labels[-1]}.")
            continue

        ch = user_input.upper()
        if ch not in label_set:
            print(f"Invalid input. Please enter a letter between {labels[0]} and {labels[-1]}.")
            continue

        return labels.index(ch)


# =========================
# Game Loop
# =========================
def main():
    # Setup players
    players = TOKENS[:NUM_PLAYERS]

    # Create board
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Print initial board
    print_board(board)

    # Main game loop
    while True:
        current_token = players[current_player_index]

        # Prompt for column input (validated)
        col_index = prompt_for_column(current_token, COLS)

        # Try to place the checker
        placed_row = drop_checker(board, col_index, current_token)

        # Column full: player loses the turn
        if placed_row is None:
            print_board(board)
            labels = column_labels(COLS)
            print(f"Column {labels[col_index]} is full. Player {current_token} loses the turn.")
            # Next player
            current_player_index = (current_player_index + 1) * 1 % NUM_PLAYERS
            continue

        # Print updated board
        print_board(board)

        # Check for win
        if is_winning_move(board, placed_row, col_index):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
