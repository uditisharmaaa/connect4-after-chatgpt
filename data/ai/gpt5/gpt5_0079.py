import os
import random
import string
import sys

# ====== Configurable constants (submission requires 6 rows x 7 cols and 2 players) ======
N_ROWS = 6
N_COLS = 7   # Max 26
N_PLAYERS = 2  # Between 2 and 5

# ====== Derived/validated settings ======
CHECKERS_ORDER = ['X', 'O', 'V', 'H', 'M']

if not (2 <= N_PLAYERS <= 5):
    print("Error: N_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= N_ROWS) or not (1 <= N_COLS <= 26):
    print("Error: Board must have at least 1 row and 1-26 columns.")
    sys.exit(1)

PLAYERS = CHECKERS_ORDER[:N_PLAYERS]
EMPTY = " "

# ====== Utility functions ======
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def is_board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    clear_screen()
    print(header)
    print(sep)
    for r in range(rows):
        line_cells = []
        for c in range(cols):
            cell = board[r][c]
            line_cells.append(f" {cell} ")
        print("|" + "|".join(line_cells) + "|")
        print(sep)

def col_from_input(s):
    # Returns column index or None if invalid
    if not s or len(s.strip()) == 0:
        return None
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s < 'A' or s > chr(ord('A') + N_COLS - 1):
        return None
    return ord(s) - ord('A')

def get_valid_column_input(current_checker):
    # Keep asking until a syntactically valid, in-range column letter is entered
    while True:
        user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        col = col_from_input(user_in)
        if col is None:
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
            continue
        return col

def find_lowest_empty_row(board, col):
    # Return the row index of the lowest empty cell in the column, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_win_from_cell(board, row, col, checker):
    # Check 4 in a row including this cell in all directions
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # current cell
        # forward
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def has_winner(board, last_move_row, last_move_col, checker):
    # If no move was made (e.g., column full), skip
    if last_move_row is None or last_move_col is None:
        return False
    return check_win_from_cell(board, last_move_row, last_move_col, checker)

def game_draw(board):
    return is_board_full(board)

# ====== Main game loop ======
def main():
    board = create_board(N_ROWS, N_COLS)

    # Randomly select first player index
    current_player_idx = random.randint(0, N_PLAYERS - 1)

    # Initial display
    print_board(board)

    while True:
        current_checker = PLAYERS[current_player_idx]

        # Prompt for a valid column input (valid letter and within board)
        col = get_valid_column_input(current_checker)

        # Attempt to place; if column is full, lose turn
        row = find_lowest_empty_row(board, col)
        last_row = None
        last_col = None

        if row is None:
            # Column full: invalid turn, lose turn
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            input("Press Enter to continue...")
            # No placement, no win can occur, no draw change
        else:
            # Place checker
            place_checker(board, row, col, current_checker)
            last_row, last_col = row, col

        # Print updated board after the turn
        print_board(board)

        # Check for win only if a piece was placed
        if last_row is not None:
            if has_winner(board, last_row, last_col, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw (board full and no winner)
            if game_draw(board):
                print("The game is a draw.")
                break

        # Advance to next player
        current_player_idx = (current_player_idx + 1) % N_PLAYERS

if __name__ == "__main__":
    main()
