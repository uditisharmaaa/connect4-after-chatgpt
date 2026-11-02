import os
import random
import string
import sys

# ----------------------------- Configuration ---------------------------------
# Submission requires 6 rows x 7 columns and 2 players enabled.
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# Checker symbols in order for up to 5 players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# ------------------------------ Validation -----------------------------------
# Basic validation of configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

# ------------------------------ Utilities ------------------------------------
def clear_screen():
    """
    Clears the terminal screen to keep the board view tidy.
    Uses 'clear' for Unix/Linux terminals.
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Creates a 2D list representing the board initialized with spaces.
    Board indexing: board[row][col], row 0 is top, row rows-1 is bottom.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the board with column headers labeled A.. and rows with grid lines.
    """
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal border
    border = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(border)
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(border)


def get_valid_column_input(cols, prompt):
    """
    Prompt the user for a valid column letter.
    Keeps asking until a valid letter within A.. is entered.
    Returns the 0-based column index.
    """
    valid_letters = set(string.ascii_uppercase[:cols])
    while True:
        user_input = input(prompt).strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        ch = user_input.upper()
        if ch not in valid_letters:
            print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[cols-1]}.")
            continue
        return ord(ch) - ord('A')


def find_drop_row(board, col):
    """
    Given a column index, find the lowest available row index to place a checker.
    Returns the row index if available, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row and move upwards to find first empty slot
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, symbol):
    """
    Places a checker in the specified column if possible.
    Returns (row_index, col_index) if placed, or (None, None) if the column is full.
    """
    r = find_drop_row(board, col)
    if r is None:
        return None, None
    board[r][col] = symbol
    return r, col


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive checkers matching 'symbol' starting from (start_r, start_c)
    moving in direction (dr, dc). Includes the starting cell.
    """
    rows, cols = len(board), len(board[0])
    r, c = start_r, start_c
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, symbol):
    """
    Checks if placing 'symbol' at (last_r, last_c) created a 4-in-a-row.
    Considers horizontal, vertical, and two diagonals.
    """
    if last_r is None or last_c is None:
        return False

    # Directions: (dr, dc) pairs; we count both directions around the last move.
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right / up-left
        (1, -1),  # Diagonal down-left / up-right
    ]

    for dr, dc in directions:
        # Count including the last placed checker: forward and backward directions minus 1 to avoid double counting last cell
        total = (
            check_win_from(board, last_r, last_c, dr, dc, symbol) +
            check_win_from(board, last_r, last_c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False


def check_draw(board):
    """
    The game is a draw if no empty spaces remain on the board.
    """
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current, num_players):
    return (current + 1) % num_players


# --------------------------------- Game --------------------------------------
def main():
    rows, cols = ROWS, COLS
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    board = create_board(rows, cols)

    # Randomly select the starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    winner_symbol = None
    while True:
        # Current player's turn
        player_symbol = symbols[current_player]

        # Prompt for input (validated)
        prompt = f"Player {player_symbol}, please enter a column: "
        col_idx = get_valid_column_input(cols, prompt)

        # Try to place checker
        row_idx, placed_col_idx = place_checker(board, col_idx, player_symbol)

        # Clear screen and reprint board after the action (regardless of success)
        clear_screen()
        print_board(board)

        if row_idx is None:
            # Column full: invalid turn, player loses the turn
            print(f"Column {string.ascii_uppercase[col_idx]} is full. Turn lost.")
            # After a lost turn, check if draw (board could be full already).
            if check_draw(board):
                break
            # Move to next player
            current_player = next_player_index(current_player, NUM_PLAYERS)
            continue

        # Check for win
        if check_win(board, row_idx, placed_col_idx, player_symbol):
            winner_symbol = player_symbol
            break

        # Check for draw
        if check_draw(board):
            break

        # Next player's turn
        current_player = next_player_index(current_player, NUM_PLAYERS)

    # Game over message
    if winner_symbol is not None:
        print(f"Player {winner_symbol} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
