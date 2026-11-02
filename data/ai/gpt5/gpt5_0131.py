import os
import random
import string
import sys

# ---------- Configuration ----------
# Submission requires 6 rows x 7 columns and 2 players enabled
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Supported range: 2..5

TOKENS = ['X', 'O', 'V', 'H', 'M']

# ---------- Validation for configuration ----------
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26 (A-Z).")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]


# ---------- Board Utilities ----------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # Per assignment: use 'clear' (Linux/Unix)
    os.system('clear')


def column_labels(cols):
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    print(header)

    # Print grid
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def is_board_full(board):
    # If top row has no spaces, board is full
    return all(cell != " " for cell in board[0])


def find_row_for_col(board, col):
    # Return the lowest available row index for given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_token(board, col, token):
    r = find_row_for_col(board, col)
    if r is None:
        return None
    board[r][col] = token
    return r


# ---------- Win Checking ----------
def check_win_from(board, start_r, start_c, token):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Forward direction
        r, c = start_r + dr, start_c + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Backward direction
        r, c = start_r - dr, start_c - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


# ---------- Input Handling ----------
def read_column_input(valid_cols):
    labels = column_labels(valid_cols)
    labels_set = set(labels)

    while True:
        try:
            user_input = input("Player {}, please enter a column: ".format(current_token_placeholder)).strip()
        except EOFError:
            # Graceful exit on EOF
            print()
            sys.exit(0)

        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter between {} and {}.".format(labels[0], labels[-1]))
            continue

        letter = user_input.upper()
        if letter not in labels_set:
            print("Invalid input. Please enter a letter between {} and {}.".format(labels[0], labels[-1]))
            continue

        return labels.index(letter)


# ---------- Game Loop ----------
def play_game():
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        # Display board
        print_board(board)

        # Current player's token
        token = PLAYER_TOKENS[current_player_idx]

        # Prompt and validate input
        # The prompt needs to include current player's token; we pass it via a global placeholder
        global current_token_placeholder
        current_token_placeholder = token
        col = read_column_input(COLS)

        # Attempt to place the checker
        row = place_token(board, col, token)
        if row is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            print(f"Column {column_labels(COLS)[col]} is full. Player {token} loses the turn.")
            input("Press Enter to continue...")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After placing, print updated board
        print_board(board)

        # Check for win
        if check_win_from(board, row, col, token):
            print(f"Player {token} won!")
            return

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


# Placeholder used in read_column_input to show current token in prompt
current_token_placeholder = "?"

if __name__ == "__main__":
    # Initial empty board display before the first move
    print_board(create_board(ROWS, COLS))
    # Randomly selected first player is shown implicitly on first prompt
    play_game()
