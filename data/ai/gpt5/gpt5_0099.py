import os
import random
import string
import sys

# -----------------------------
# Configuration (as constants)
# -----------------------------
ROWS = 6                     # Number of rows (default submission: 6)
COLS = 7                     # Number of columns (default submission: 7) - max 26
NUM_PLAYERS = 2              # Number of players (2 to 5; default submission: 2)
TOKENS = ["X", "O", "V", "H", "M"]  # Tokens in order for up to 5 players
WIN_LENGTH = 4               # Always 4 to win

# Safety checks for configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

# -----------------------------
# Utility / Game Functions
# -----------------------------
def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    # Create a 2D board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Labels A, B, C, ... up to number of columns (max 26)
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Print column headers
    print("  " + "   ".join(labels))

    # Print top border
    print("+" + "---+" * cols)

    # Print each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)

def get_player_tokens(n_players):
    return TOKENS[:n_players]

def find_next_open_row(board, col):
    # Return the lowest available row index in the given column, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def inside(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def check_winner(board, piece):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != piece:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and inside(board, rr, cc) and board[rr][cc] == piece:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return True
    return False

def board_full(board):
    # If any top row cell (or any cell) is empty, board is not full
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def read_valid_column_input(valid_cols_set, last_label):
    # Continuously prompt until a syntactically valid label is provided
    # Valid input: single uppercase letter within available labels
    # We'll accept lowercase input for convenience and convert to uppercase.
    while True:
        user_in = input().strip()
        if not user_in:
            print(f"Invalid input. Please enter a column (A-{last_label}):")
            continue
        val = user_in.upper()
        if len(val) != 1 or val not in valid_cols_set:
            print(f"Invalid input. Please enter a column (A-{last_label}):")
            continue
        return val

# -----------------------------
# Main Game Loop
# -----------------------------
def main():
    # Initialize game
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)
    label_to_col = {label: idx for idx, label in enumerate(labels)}
    valid_cols_set = set(labels)

    player_tokens = get_player_tokens(NUM_PLAYERS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)

    while True:
        current_token = player_tokens[current_player_idx]
        print(f"Player {current_token}, please enter a column:")
        col_label = read_valid_column_input(valid_cols_set, labels[-1])
        col = label_to_col[col_label]

        # Attempt to place the checker
        row = find_next_open_row(board, col)
        if row is None:
            # Column full: invalid turn, player loses the turn
            # Reprint board with message, then continue to next player
            print_board(board)
            print(f"Column {col_label} is full. Player {current_token} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the piece
        drop_piece(board, row, col, current_token)

        # Print updated board
        print_board(board)

        # Check for win
        if check_winner(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
