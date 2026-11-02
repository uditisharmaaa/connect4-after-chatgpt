import os
import random
import sys

# ====== Configuration (submission requires 6x7 and 2 players enabled) ======
ROWS = 6          # number of rows (height)
COLS = 7          # number of columns (width), max 26 due to letter labels
NUM_PLAYERS = 2   # must be between 2 and 5 inclusive
TOKENS = ["X", "O", "V", "H", "M"]  # player tokens in order

# ====== Validation of configuration ======
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("COLS must be <= 26 (due to letter labeling).")
    sys.exit(1)

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]

# ====== Utility functions ======
def clear_screen():
    # Assignment requires using 'clear'
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    # Header letters
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))
    # Top border
    print("+" + "---+" * cols)
    # Rows from top to bottom
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)

def col_is_full(board, col):
    return board[0][col] != " "

def drop_checker(board, col, token):
    """
    Drops a checker into the specified column.
    Returns the row index where it landed, or None if column is full.
    """
    rows = len(board)
    if col_is_full(board, col):
        return None
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None  # Shouldn't happen due to col_is_full check

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False

def is_board_full(board):
    cols = len(board[0]) if board else 0
    for c in range(cols):
        if not col_is_full(board, c):
            return False
    return True

def prompt_for_column(valid_cols):
    """
    Prompts the user for a column letter until a valid input (one of valid_cols) is provided.
    Returns the uppercase letter chosen.
    """
    while True:
        try:
            user_input = input().strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter (e.g., A).")
            print("Please enter a column:", end=" ")
            continue
        ch = user_input
        if ch not in valid_cols:
            print("Invalid column. Please enter one of: " + ", ".join(valid_cols))
            print("Please enter a column:", end=" ")
            continue
        return ch

# ====== Game setup ======
def main():
    board = create_board(ROWS, COLS)
    col_letters = [chr(ord('A') + i) for i in range(COLS)]

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)
    # Game loop
    while True:
        token = PLAYER_TOKENS[current_player_index]
        print(f"Player {token}, please enter a column:", end=" ")

        # Get a valid column letter input
        col_letter = prompt_for_column(col_letters)
        col_index = ord(col_letter) - ord('A')

        # Attempt to drop checker
        row_placed = drop_checker(board, col_index, token)
        if row_placed is None:
            # Column was full: invalid turn, player loses the turn.
            clear_screen()
            print_board(board)
            print(f"Column {col_letter} is full. Player {token} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Before continuing, check draw (board might be full)
            if is_board_full(board):
                print("It's a draw!")
                break
            continue

        # Successful move: update screen
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, token):
            print(f"Player {token} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
