import os
import random
import string
import sys

# ----------------------------
# Configuration (constants)
# ----------------------------
ROWS = 6                 # Number of rows (default for submission)
COLS = 7                 # Number of columns (default for submission)
NUM_PLAYERS = 2          # Supported range: 2..5 (default for submission)
WIN_LENGTH = 4           # Fixed by assignment: 4 in a row to win
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # In order as specified
MAX_COLS = 26            # Max columns due to alphabet labels A..Z

assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert 1 <= COLS <= MAX_COLS, "COLS must be between 1 and 26."

# ----------------------------
# Helpers for screen and board
# ----------------------------

def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Return a list of uppercase column labels starting at 'A'."""
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    """Print the board with column headers and cell borders."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header labels
    print("  " + "   ".join(labels))
    # Top border
    print("+" + ("---+" * cols))

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))


def is_board_full(board):
    """Return True if the board has no empty cells."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def valid_input_letter(inp, cols):
    """
    Validate that inp is a single alphabetic letter within the current column range.
    Return the column index if valid, else None.
    """
    if not inp or len(inp) != 1 or not inp.isalpha():
        return None
    inp = inp.upper()
    labels = column_labels(cols)
    if inp not in labels:
        return None
    return labels.index(inp)


def drop_checker(board, col_idx, symbol):
    """
    Attempt to place 'symbol' in column col_idx.
    The checker falls to the lowest available row.
    Return (placed, row_index) where:
      - placed is True if checker was placed, False if column is full
      - row_index is the row where it was placed, or None if not placed
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = symbol
            return True, r
    return False, None


# ----------------------------
# Win and draw checking
# ----------------------------

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, r, c, dr, dc, symbol):
    """
    Check WIN_LENGTH in a row starting from (r, c) moving by (dr, dc).
    """
    rows = len(board)
    cols = len(board[0])
    for k in range(WIN_LENGTH):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc, rows, cols) or board[rr][cc] != symbol:
            return False
    return True


def check_winner(board, symbol):
    """
    Check if the given symbol has a winning sequence on the board.
    Directions: horizontal (0,1), vertical (1,0), diag down-right (1,1), diag up-right (-1,1)
    """
    rows = len(board)
    cols = len(board[0])
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                if check_win_from_cell(board, r, c, dr, dc, symbol):
                    return True
    return False


# ----------------------------
# Game loop
# ----------------------------

def main():
    # Initialize board and player symbols
    board = create_board(ROWS, COLS)
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        # Check for draw (board full) before next move
        if is_board_full(board):
            print("It's a draw!")
            break

        current_symbol = symbols[current_player_idx]
        prompt = f"Player {current_symbol}, please enter a column: "

        # Get a valid column letter (within range). Invalid letters prompt again (turn not lost).
        while True:
            user_inp = input(prompt).strip()
            col_idx = valid_input_letter(user_inp, COLS)
            if col_idx is None:
                # Invalid input type/character/out of range -> ask again (turn not lost)
                continue
            else:
                # We have a valid column index; now try to drop the checker.
                placed, _ = drop_checker(board, col_idx, current_symbol)
                # Clear and print the updated board regardless
                clear_screen()
                print_board(board)

                if not placed:
                    # Column full: turn is invalid and the player loses the turn
                    # Do not place, move on to next player
                    # No win/draw check since nothing changed
                    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                    break
                else:
                    # Successful placement, check for win
                    if check_winner(board, current_symbol):
                        print(f"Player {current_symbol} won!")
                        return
                    # Check for draw after a valid placement
                    if is_board_full(board):
                        print("It's a draw!")
                        return
                    # Next player's turn
                    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                    break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)
