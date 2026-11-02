import os
import random
import string

# ------------------------------- #
# CONFIGURABLE CONSTANTS
NUM_ROWS = 6         # For the standard game, 6 rows
NUM_COLS = 7         # For the standard game, 7 columns (max 26 allowed)
NUM_PLAYERS = 2      # Number of players (2-5 supported)
WIN_COUNT = 4        # How many in a row to win
MAX_COLS = 26        # Should not exceed 26 for letter labeling
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 player symbols

# ------------------------------- #
# BOARD INITIALIZATION & PRINTING

def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board to the terminal."""
    os.system('clear')  # Clear the terminal screen before each print

    cols = len(board[0])
    # Column labels (A, B, C, ..., max G for 7)
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

# ------------------------------- #
# GAME LOGIC

def get_valid_column(board, current_symbols):
    """Prompt the player for a valid column input and return its index."""
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        col_input = input(f"Player {current_symbols}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_letters:
            print(f"Invalid input! Please enter a letter between A and {valid_letters[-1]}.")
            continue
        col_idx = ord(col_input) - ord('A')
        # Is the column full?
        if board[0][col_idx] != " ":
            print("Column is full! You lose your turn.")
            return None  # Signal the turn should be lost
        else:
            return col_idx

def place_checker(board, col, symbol):
    """
    Place a checker of 'symbol' in the given column.
    Returns True if placed, False if a problem (i.e. column full).
    The checker occupies the lowest empty cell in that column.
    """
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return True
    return False  # Column full, but this should not generally happen due to input checking

def is_win(board, row_idx, col_idx, symbol):
    """
    Check if placing symbol at (row_idx, col_idx) resulted in a win.
    Check all directions: horizontal, vertical, both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Includes the placed symbol
        # Check in the positive direction
        r, c = row_idx + dr, col_idx + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row_idx - dr, col_idx - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        # Win if enough in a row
        if count >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    """True if the board is completely full."""
    return all(cell != " " for cell in board[0])

def get_next_empty_row(board, col):
    """
    Return the row index where the checker would land in column `col`.
    If column is full, returns -1.
    """
    for i in range(len(board)-1, -1, -1):
        if board[i][col] == " ":
            return i
    return -1

# ------------------------------- #
# MAIN GAME LOOP

def main():
    # Board and player setup
    assert 2 <= NUM_PLAYERS <= 5, "Only 2-5 players supported!"
    assert 1 <= NUM_COLS <= MAX_COLS, "Too many columns!"
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    board = create_board(NUM_ROWS, NUM_COLS)
    # Randomize the starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {player_symbols[current_player]} begins!")

    while True:
        symbol = player_symbols[current_player]
        # Input loop: get valid column or signal loss of turn if full
        col_idx = get_valid_column(board, symbol)
        if col_idx is None:
            # Column full - lose turn
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)  # Keep up-to-date
            continue

        row_idx = get_next_empty_row(board, col_idx)
        if row_idx == -1:
            # Should not happen as get_valid_column checks top cell
            print("Unexpected error: Column full after input validation.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        board[row_idx][col_idx] = symbol  # Place the checker

        print_board(board)

        # Check for a win
        if is_win(board, row_idx, col_idx, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
