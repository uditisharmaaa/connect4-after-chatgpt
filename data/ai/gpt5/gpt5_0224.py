import os
import random
import string
import sys

# ----------------------------
# Configuration (constants)
# ----------------------------
ROWS = 6
COLS = 7    # Max 26
NUM_PLAYERS = 2  # Supports 2..5 players
CHECKERS = ["X", "O", "V", "H", "M"]  # In order, use first NUM_PLAYERS

# Safety checks for configuration
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# ----------------------------
# Board utilities
# ----------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    # Header with column letters
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Top border line
    border = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(border)
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(border)

# ----------------------------
# Game mechanics
# ----------------------------
def col_from_input(user_input):
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return None

def is_column_full(board, col):
    return board[0][col] != " "

def drop_checker(board, col, token):
    # Drops token into the lowest available row in column col
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None  # Column full

def check_winner(board, last_row, last_col, token):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]

    for dr, dc in directions:
        count = 1  # include last placed
        # forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

# ----------------------------
# Main game loop
# ----------------------------
def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {PLAYER_TOKENS[current_player_idx]}, please enter a column:")

    winner = None

    while True:
        # Input phase (validate non-empty, single letter in range)
        user_in = input().strip()
        col = col_from_input(user_in)

        # If invalid input, keep asking until valid (turn not lost)
        while col is None:
            print("Invalid input. Please enter a valid column letter:")
            user_in = input().strip()
            col = col_from_input(user_in)

        token = PLAYER_TOKENS[current_player_idx]

        # Attempt to place checker
        placed_row = None
        if not is_column_full(board, col):
            placed_row = drop_checker(board, col, token)
            # placed_row will not be None here
        else:
            # Column full: turn is invalid and the player loses the turn
            pass

        # Clear screen and print updated (or unchanged) board
        clear_screen()
        print_board(board)

        # If placed, check for winner and draw
        if placed_row is not None:
            if check_winner(board, placed_row, col, token):
                winner = token
                print(f"Player {winner} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break

        # Move to next player (column-full case still advances turn)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        next_token = PLAYER_TOKENS[current_player_idx]
        if placed_row is None:
            # Inform about lost turn due to full column
            chosen_label = COLUMN_LABELS[col]
            print(f"Column {chosen_label} is full. Turn lost.")

        print(f"Player {next_token}, please enter a column:")

if __name__ == "__main__":
    main()
