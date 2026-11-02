import os
import random
import string
import sys

# ----------------------------- Configuration -----------------------------
# Board dimensions: ROWS x COLS (max 26 columns)
ROWS = 6
COLS = 7

# Number of players (2 to 5)
NUM_PLAYERS = 2

# Player checker symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Number needed in a row to win
WIN_LENGTH = 4
# -------------------------------------------------------------------------

# --------------------------- Validation of config ------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

# Trim to number of players
PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]
# -------------------------------------------------------------------------


def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a ROWS x COLS board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and grid lines, as specified."""
    rows = len(board)
    cols = len(board[0])

    # Column header
    labels = [string.ascii_uppercase[c] for c in range(cols)]
    header = "  " + "   ".join(labels)
    print(header)

    # For each row, print separator and content lines
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def get_valid_column_input(valid_cols):
    """
    Prompt the current player for a column letter.
    Validate that input is a single letter within valid_cols.
    Re-prompt on invalid input until valid (turn is not lost).
    Returns the 0-based column index.
    """
    valid_set = set(valid_cols)
    while True:
        user_in = input().strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single uppercase letter for a column:")
            continue
        ch = user_in.upper()
        if ch not in valid_set:
            print("Invalid column. Please enter one of: " + " ".join(valid_cols))
            continue
        return valid_cols.index(ch)


def place_checker(board, col, symbol):
    """
    Place the checker in the lowest available row in the given column.
    Returns the row index where placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """Count consecutive symbols starting from (start_r, start_c), moving (dr, dc)."""
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_winner(board, last_r, last_c, symbol):
    """
    Check if placing 'symbol' at (last_r, last_c) creates a connect-WIN_LENGTH.
    Checks horizontal, vertical, and both diagonals.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]
    for dr, dc in directions:
        # Count both directions from the last placed position
        total = 1  # include the last placed
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    """The game is a draw if the top row has no empty spaces (board is full)."""
    return all(cell != " " for cell in board[0])


def main():
    board = create_board(ROWS, COLS)
    col_labels = [string.ascii_uppercase[c] for c in range(COLS)]

    # Randomly select starting player
    current_player_index = random.randrange(len(PLAYERS))

    # Initial board display before the game starts
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_symbol = PLAYERS[current_player_index]
        print(f"Player {current_symbol}, please enter a column:")
        col = get_valid_column_input(col_labels)

        # Attempt to place checker
        placed_row = place_checker(board, col, current_symbol)
        if placed_row is None:
            # Column full: player loses turn
            clear_screen()
            print_board(board)
            print(f"Column {col_labels[col]} is full. Player {current_symbol} loses the turn.")
            # Advance to next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
            continue

        # After a successful move, check for win/draw
        if check_winner(board, placed_row, col, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % len(PLAYERS)

        # Print updated board for the next turn
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
