# Connect 4 for Intro CS
# - 6 rows, 7 columns
# - Columns labeled A-G
# - 2 to 5 players (symbols from PLAYER_SYMBOLS)
# - Random first player
# - Validates input
# - Checks wins and draws
# - Uses os.system('clear') to refresh screen

import os
import random
import sys

# ----------------- Configuration Constants -----------------
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must be length COLS
EMPTY = '.'

# Player symbols in play order (up to 5 max as required)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Number of players (must be between 2 and 5, and <= len(PLAYER_SYMBOLS))
NUM_PLAYERS = 2  # Change to 3, 4, or 5 as desired

# ----------------- Utility -----------------
def clear_screen():
    # Requirement says to use 'clear'
    os.system('clear')

def create_board(rows, cols, fill=EMPTY):
    return [[fill for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Header
    print("  " + " ".join(COLUMN_LABELS[:len(board[0])]))
    # Rows
    for r in range(len(board)):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    # Footer line showing row numbers alignment (optional)
    print("  " + " ".join(COLUMN_LABELS[:len(board[0])]))

def col_from_label(label):
    try:
        return COLUMN_LABELS.index(label)
    except ValueError:
        return -1

def first_empty_row(board, col):
    # Return the row index where the piece will land in this column, or -1 if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1

def board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    rows, cols = len(board), len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, r, c, symbol):
    # Check 4 directions (each counted both ways):
    # Horizontal (0,1), Vertical (1,0), Diagonal down-right (1,1), Diagonal up-right (-1,1)
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        total = 1  # count the placed piece
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def get_valid_move(board, current_symbol):
    cols_allowed = COLUMN_LABELS[:len(board[0])]
    while True:
        raw = input(f"Player {current_symbol}, choose a column ({cols_allowed}): ").strip().upper()
        if len(raw) != 1 or raw not in cols_allowed:
            print(f"Invalid input. Enter a single letter in {cols_allowed}.")
            continue
        col = col_from_label(raw)
        row = first_empty_row(board, col)
        if row == -1:
            print("That column is full. Choose another.")
            continue
        return row, col

def validate_constants():
    assert COLS == len(COLUMN_LABELS), "COLS must match length of COLUMN_LABELS"
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
    assert NUM_PLAYERS <= len(PLAYER_SYMBOLS), "Not enough player symbols for NUM_PLAYERS"
    # Ensure EMPTY is not a player symbol
    assert EMPTY not in PLAYER_SYMBOLS, "EMPTY symbol conflicts with player symbols"
    # Ensure no duplicate player symbols among active players
    active = PLAYER_SYMBOLS[:NUM_PLAYERS]
    assert len(set(active)) == len(active), "Duplicate player symbols detected"

def main():
    validate_constants()
    board = create_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    current_index = random.randrange(NUM_PLAYERS)  # random first player
    move_count = 0
    winner = None

    while True:
        clear_screen()
        print_board(board)
        current_symbol = players[current_index]

        # Get a valid move
        r, c = get_valid_move(board, current_symbol)

        # Apply move
        board[r][c] = current_symbol
        move_count += 1

        # Check win
        if is_winning_move(board, r, c, current_symbol):
            winner = current_symbol
            clear_screen()
            print_board(board)
            print(f"Player {winner} wins! Congratulations!")
            break

        # Check draw
        if move_count == ROWS * COLS or board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
