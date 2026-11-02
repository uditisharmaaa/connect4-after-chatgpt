import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
NUM_ROWS = 6        # Number of rows (default submission requirement)
NUM_COLS = 7        # Number of columns (default submission requirement, max 26)
NUM_PLAYERS = 2     # Number of players (2 to 5)

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Order of checkers for up to 5 players
WIN_LENGTH = 4      # Number in a row needed to win (fixed at 4 per assignment)

# =========================
# Validation of constants
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
    sys.exit(1)

if not (1 <= NUM_ROWS) or not (1 <= NUM_COLS <= 26):
    print("Error: NUM_ROWS must be >= 1 and NUM_COLS must be between 1 and 26.", file=sys.stderr)
    sys.exit(1)

# Limit the active players to requested count
ACTIVE_PLAYERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# =========================
# Board utilities
# =========================
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Clear for Unix/Linux/Mac as requested
    os.system('clear')

def column_labels(cols):
    # Labels A, B, C, ...
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Top border
    horiz = "+---" * len(labels) + "+"
    for r in range(len(board)):
        print(horiz)
        row_cells = "| " + " | ".join(board[r]) + " |"
        print(row_cells)
    print(horiz)

# =========================
# Game mechanics
# =========================
def is_valid_column_label(label, cols):
    if len(label) != 1:
        return False
    if label not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index_from_label(label):
    return ord(label) - ord('A')

def find_drop_row(board, col_idx):
    # Return the row index where the checker should land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None

def drop_checker(board, col_idx, checker):
    row_idx = find_drop_row(board, col_idx)
    if row_idx is None:
        return None  # Column full
    board[row_idx][col_idx] = checker
    return row_idx

def check_win_from_cell(board, row, col, checker):
    # Check all 4 directions (each with two opposite vectors)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count the current cell
        # Expand in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Expand in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_is_full(board):
    for r in board:
        for cell in r:
            if cell == " ":
                return False
    return True

def get_player_input(current_checker, cols):
    labels = column_labels(cols)
    prompt = f"Player {current_checker}, please enter a column: "
    while True:
        user_in = input(prompt).strip().upper()
        if is_valid_column_label(user_in, cols):
            return get_column_index_from_label(user_in)
        # Invalid input: keep asking until valid (turn is not lost)
        print(f"Invalid input. Enter one of: {', '.join(labels)}")

# =========================
# Main game loop
# =========================
def main():
    random.seed()

    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_checker = ACTIVE_PLAYERS[current_player_idx]

        # Get a valid column label (exists on board). This loop does not consider full columns.
        col_idx = get_player_input(current_checker, NUM_COLS)

        # Attempt to drop checker
        drop_row = drop_checker(board, col_idx, current_checker)

        if drop_row is None:
            # Column full: invalid turn, player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col_idx]} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successful placement: check for win/draw
        clear_screen()
        print_board(board)

        if check_win_from_cell(board, drop_row, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_is_full(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
