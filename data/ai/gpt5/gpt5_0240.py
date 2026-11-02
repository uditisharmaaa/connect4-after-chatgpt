import os
import random
import string
import sys

# -------- Configuration (can be changed for testing; submission requires below defaults) --------
ROWS = 6          # number of rows (submission: 6)
COLUMNS = 7       # number of columns (submission: 7, max 26)
NUM_PLAYERS = 2   # between 2 and 5 (submission: 2)
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]  # in order; only first NUM_PLAYERS are used

# Safety checks on configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLUMNS <= 26):
    print("COLUMNS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

TOKENS = PLAYER_TOKENS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLUMNS])

# -------- Board Utilities --------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Works on Linux/Unix terminals; as required by the assignment
    os.system('clear')

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column labels
    header = "  " + "   ".join(COL_LABELS[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# -------- Game Mechanics --------
def find_row_for_col(board, col_idx):
    # Return the lowest available row index for this column; or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None

def is_valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if ch not in COL_LABELS:
        return False
    return True

def check_win_from_cell(board, start_r, start_c, dr, dc, token):
    rows = len(board)
    cols = len(board[0])
    for k in range(4):
        r = start_r + dr * k
        c = start_c + dc * k
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != token:
            return False
    return True

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    # Horizontal (dr=0, dc=1)
    for r in range(rows):
        for c in range(cols - 3):
            if check_win_from_cell(board, r, c, 0, 1, token):
                return True

    # Vertical (dr=1, dc=0)
    for r in range(rows - 3):
        for c in range(cols):
            if check_win_from_cell(board, r, c, 1, 0, token):
                return True

    # Diagonal down-right (dr=1, dc=1)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if check_win_from_cell(board, r, c, 1, 1, token):
                return True

    # Diagonal down-left (dr=1, dc=-1)
    for r in range(rows - 3):
        for c in range(3, cols):
            if check_win_from_cell(board, r, c, 1, -1, token):
                return True

    return False

def prompt_for_column(current_token):
    while True:
        try:
            user_input = input(f"Player {current_token}, please enter a column: ").strip()
        except EOFError:
            # If input stream closes, treat as exit
            print()
            sys.exit(0)

        if not is_valid_column_input(user_input):
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        return user_input.upper()

def game_loop():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_token = TOKENS[current_player_idx]
        col_label = prompt_for_column(current_token)
        col_idx = COL_LABELS.index(col_label)

        target_row = find_row_for_col(board, col_idx)

        if target_row is None:
            # Column is full: turn is invalid and the player loses the turn
            print(f"Column {col_label} is full. Player {current_token} loses the turn.")
            # Pause briefly waiting for Enter to make it visible
            try:
                input("Press Enter to continue...")
            except EOFError:
                pass
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        board[target_row][col_idx] = current_token

        # After move, clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

def main():
    # Print initial info and start the game
    # Random first player is already handled in game_loop
    game_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
