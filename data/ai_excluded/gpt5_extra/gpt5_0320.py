import os
import random
import string
import sys

# -------------------------
# Configuration (constants)
# -------------------------
ROWS = 6
COLS = 7          # Max 26 (A-Z)
NUM_PLAYERS = 2   # Supported: 2 to 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4    # Always 4, regardless of number of players

# Basic validations for configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26 or COLS < 1:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]


# -------------------------
# Utility functions
# -------------------------
def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Header with column letters
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Grid
    horizontal = "+" + ("---+" * cols)
    for r in range(rows):
        print(horizontal)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horizontal)


def column_from_input(inp, cols):
    if len(inp) != 1:
        return None
    ch = inp.upper()
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return None
    return ord(ch) - ord('A')


def place_checker(board, col, symbol):
    # Place from bottom-most empty cell upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def check_win(board, row, col, symbol):
    # Count consecutive symbols including (row, col) in each direction pair
    def count_dir(dr, dc):
        r, c = row + dr, col + dc
        cnt = 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            cnt += 1
            r += dr
            c += dc
        return cnt

    # Directions: horizontal (0,1), vertical (1,0), diag1 (1,1), diag2 (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


# -------------------------
# Game loop
# -------------------------
def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)
    status_message = None

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        # Show any status message from previous turn (e.g., column full)
        if status_message:
            print(status_message)
            status_message = None

        # Prompt for input and validate letter selection
        prompt = f"Player {PLAYERS[current_player_idx]}, please enter a column: "
        user_inp = input(prompt).strip()

        # Keep asking until valid column letter (within board). Do NOT lose turn for invalid input.
        while True:
            col = column_from_input(user_inp, COLS)
            if col is not None:
                break
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            user_inp = input(prompt).strip()

        # Attempt to place checker
        symbol = PLAYERS[current_player_idx]
        placed_row = place_checker(board, col, symbol)

        # If column is full: lose turn
        if placed_row is None:
            col_letter = user_inp.upper()
            status_message = f"Column {col_letter} is full. Turn lost."
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            # Loop continues to next player
            continue

        # Successful placement: check for win
        if check_win(board, placed_row, col, symbol):
            clear_screen()
            print_board(board)
            print(f"Player {symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Print updated board for next prompt
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
