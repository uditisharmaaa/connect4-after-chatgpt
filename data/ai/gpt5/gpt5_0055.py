import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
NUM_ROWS = 6          # Default assignment setting: 6 rows
NUM_COLS = 7          # Default assignment setting: 7 columns (max 26)
PLAYERS_COUNT = 2     # Default assignment setting: 2 players (supports 2 to 5)

WIN_LENGTH = 4        # Always 4 in a row to win (per assignment)
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Player tokens in order

# =========================
# Validation of configuration
# =========================
def validate_configuration():
    if not (2 <= PLAYERS_COUNT <= 5):
        print("Error: PLAYERS_COUNT must be between 2 and 5.")
        sys.exit(1)
    if NUM_COLS < 1 or NUM_COLS > 26:
        print("Error: NUM_COLS must be between 1 and 26.")
        sys.exit(1)
    if NUM_ROWS < 1:
        print("Error: NUM_ROWS must be at least 1.")
        sys.exit(1)

# =========================
# Utility functions
# =========================
def clear_screen():
    # As per assignment requirement: use Unix clear
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels (A, B, C, ...)
    labels = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(labels)
    print(header)

    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Rows (top to bottom)
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def is_valid_column_input(user_input, num_cols):
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:num_cols]:
        return False
    return True

def col_index_from_letter(letter):
    return ord(letter) - ord('A')

def column_full(board, col):
    # Column is full if the top-most cell is not a space
    return board[0][col] != " "

def drop_checker(board, col, token):
    """
    Attempts to drop a checker into the given column.
    Returns the (row, col) where the checker was placed, or None if column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, token):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    L = WIN_LENGTH

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == token:
                count += 1
                if count >= L:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == token:
                count += 1
                if count >= L:
                    return True
            else:
                count = 0

    # Diagonal (down-right)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            # Try to extend L-1 steps down-right
            ok = True
            for k in range(1, L):
                rr = r + k
                cc = c + k
                if rr >= rows or cc >= cols or board[rr][cc] != token:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal (up-right)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            # Try to extend L-1 steps up-right
            ok = True
            for k in range(1, L):
                rr = r - k
                cc = c + k
                if rr < 0 or cc >= cols or board[rr][cc] != token:
                    ok = False
                    break
            if ok:
                return True

    return False

# =========================
# Game loop
# =========================
def main():
    validate_configuration()

    rows = NUM_ROWS
    cols = NUM_COLS
    tokens = TOKENS[:PLAYERS_COUNT]

    board = create_board(rows, cols)

    # Randomly pick starting player index
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Gameplay loop
    while True:
        current_token = tokens[current_player_idx]
        prompt = f"Player {current_token}, please enter a column: "

        # Get valid input (re-prompt until valid letter within bounds)
        while True:
            user_input = input(prompt).strip().upper()
            if is_valid_column_input(user_input, cols):
                break
            else:
                clear_screen()
                print_board(board)
                # Show helpful message and re-prompt; turn is not lost
                valid_range = f"A to {string.ascii_uppercase[cols - 1]}"
                print(f"Invalid input. Please enter a single uppercase letter from {valid_range}.")

        col = col_index_from_letter(user_input)

        # If column is full, the turn is invalid and the player loses the turn
        if column_full(board, col):
            clear_screen()
            print_board(board)
            print(f"Column {user_input} is full. Player {current_token} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue

        # Place checker
        drop_checker(board, col, current_token)

        # Update display
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
