import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
# Board dimensions (rows x cols). Submission requires 6x7.
ROWS = 6
COLS = 7  # must be <= 26 to fit A..Z labels
# Number of players (2 to 5). Submission requires 2.
NUM_PLAYERS = 2
# Required in-a-row to win (fixed at 4 for this assignment).
REQUIRED_TO_WIN = 4

# Symbols for players in order. Supports up to 5 players.
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def clear_screen():
    """Clear the terminal screen (Unix/Linux expected per assignment)."""
    os.system('clear')


def create_board(rows, cols):
    """Create an empty board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Return a list of column labels ['A', 'B', ...]."""
    return list(string.ascii_uppercase[:cols])


def print_board(board, labels):
    """Print the board with headers and grid, as specified."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header line with column letters
    header = "  " + "   ".join(labels)
    horiz = "+" + ("---+" * cols)

    print(header)
    print(horiz)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(horiz)


def pick_starting_player(num_players):
    """Randomly pick the index of the starting player."""
    return random.randrange(num_players)


def is_valid_input(user_input, valid_labels):
    """Validate that input is a single valid column letter."""
    if not user_input or len(user_input) != 1:
        return False
    return user_input in valid_labels


def find_drop_row(board, col_idx):
    """
    Find the row index where a checker should drop in the given column.
    Returns the row index if available; None if the column is full.
    """
    rows = len(board)
    # Start from bottom row moving upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None


def drop_checker(board, col_idx, symbol):
    """Place the checker in the lowest available spot in the column."""
    r = find_drop_row(board, col_idx)
    if r is None:
        return None
    board[r][col_idx] = symbol
    return r


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, symbol, needed):
    """
    Count consecutive checkers matching symbol starting from (start_r, start_c)
    moving in direction (dr, dc). Return True if at least `needed` in a row.
    """
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        if count >= needed:
            return True
        r += dr
        c += dc
    return False


def is_winning_move(board, row, col, symbol, needed=REQUIRED_TO_WIN):
    """
    Check if placing `symbol` at (row, col) creates a winning line.
    Checks horizontal, vertical, and both diagonals.
    """
    rows, cols = len(board), len(board[0])

    # Directions to check (for each, we'll expand both ways by scanning starts)
    # Instead, for efficiency, check 4 principal directions with a method that
    # counts in both directions from the last move.
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1  # count the current piece
        # Extend forward
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Extend backward
        r, c = row - dr, col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= needed:
            return True
    return False


def board_full(board):
    """Return True if no spaces remain on the board."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def prompt_for_column(current_symbol, valid_labels):
    """
    Prompt the current player until a valid column label is entered.
    Returns the uppercase column label.
    """
    while True:
        user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        if is_valid_input(user_input, valid_labels):
            return user_input
        else:
            print("Invalid input. Please enter a single valid uppercase letter corresponding to a column.")


def main():
    # Validate configuration
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    labels = column_labels(COLS)
    label_to_index = {label: idx for idx, label in enumerate(labels)}

    board = create_board(ROWS, COLS)
    current_player_idx = pick_starting_player(NUM_PLAYERS)

    # Initial board print
    clear_screen()
    print_board(board, labels)

    # Game loop
    while True:
        current_symbol = symbols[current_player_idx]

        # Prompt for valid letter input
        col_label = prompt_for_column(current_symbol, set(labels))
        col_idx = label_to_index[col_label]

        # Attempt to drop checker
        drop_row = drop_checker(board, col_idx, current_symbol)

        # Clear and print updated board after the attempt
        clear_screen()
        print_board(board, labels)

        if drop_row is None:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {col_label} is full. Player {current_symbol} loses the turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for a win
        if is_winning_move(board, drop_row, col_idx, current_symbol, REQUIRED_TO_WIN):
            print(f"Player {current_symbol} won!")
            break

        # Check for a draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
