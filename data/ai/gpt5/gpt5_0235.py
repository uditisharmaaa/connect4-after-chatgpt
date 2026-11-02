import os
import random
import string
import sys

# -------------------- Configuration --------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
CLEAR_CMD = 'clear'  # Works on Linux/Unix terminals

# -------------------- Validation of Configuration --------------------
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > 26 or COLS < 1:
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# -------------------- Board Utilities --------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    try:
        os.system(CLEAR_CMD)
    except Exception:
        pass  # In case clear isn't available, continue without clearing.

def print_board(board):
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(sep)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def find_available_row(board, col):
    # Returns the index of the lowest available row in the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, token):
    r = find_available_row(board, col)
    if r is None:
        return False
    board[r][col] = token
    return True

# -------------------- Game Logic --------------------
def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, token):
    # Check all directions for WIN_LENGTH in a row for the given token
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return True
    return False

def check_draw(board):
    # Draw if no empty spaces remain
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def prompt_for_column(player_token):
    # Keep asking until valid input (letter within range)
    while True:
        try:
            user_input = input(f"Player {player_token}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting game.")
            sys.exit(0)

        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue

        letter = user_input.upper()
        if len(letter) != 1:
            print("Please enter a single column letter (e.g., A, B, C).")
            continue

        if letter not in COLUMN_LABELS:
            print(f"Invalid column. Choose from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue

        return COLUMN_LABELS.index(letter)

# -------------------- Main Game Loop --------------------
def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        player_token = PLAYER_TOKENS[current_player_idx]

        # Prompt and validate input (only re-prompt for invalid input format/range)
        col = prompt_for_column(player_token)

        # Attempt to place the checker
        if not place_checker(board, col, player_token):
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            col_letter = COLUMN_LABELS[col]
            print(f"Column {col_letter} is full. Player {player_token} loses the turn.")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a valid placement, check game state
        clear_screen()
        print_board(board)

        if check_win(board, player_token):
            print(f"Player {player_token} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
