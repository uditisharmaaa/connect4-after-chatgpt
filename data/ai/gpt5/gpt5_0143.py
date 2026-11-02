import os
import random
import sys

# =========================
# Configuration (Constants)
# =========================
ROWS = 6
COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

PLAYER_TOKENS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Number of checkers in a row needed to win

# =========================
# Validation of Constants
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26 (inclusive).")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

TOKENS_IN_PLAY = PLAYER_TOKENS[:NUM_PLAYERS]


# =========================
# Utility Functions
# =========================
def clear_screen():
    # Per assignment, use clear; fallback for other OS if needed
    try:
        os.system('clear')
    except Exception:
        os.system('cls')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A, B, C, ...
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def parse_column_input(user_input, cols):
    if not user_input:
        return None
    s = user_input.strip().upper()
    if len(s) != 1:
        return None
    if not ('A' <= s <= 'Z'):
        return None
    idx = ord(s) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None


def find_lowest_empty_row(board, col_idx):
    # Returns row index where the checker should land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None


def board_full(board):
    # Draw if no spaces left anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
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
                rr, cc = r, c
                for _ in range(WIN_LENGTH - 1):
                    rr += dr
                    cc += dc
                    if 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token:
                        count += 1
                    else:
                        break
                if count >= WIN_LENGTH:
                    return True
    return False


# =========================
# Game Loop
# =========================
def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)  # Random first player

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        current_token = TOKENS_IN_PLAY[current_player_idx]
        prompt = f"Player {current_token}, please enter a column: "
        col_idx = None

        # Ask until valid input character (does not lose turn for invalid input)
        while True:
            user_in = input(prompt)
            parsed = parse_column_input(user_in, COLS)
            if parsed is None:
                print("Invalid input. Enter a single letter for a valid column (e.g., A, B, C).")
                continue
            col_idx = parsed
            break

        # Try to place checker
        row_idx = find_lowest_empty_row(board, col_idx)
        if row_idx is None:
            # Column full: turn is invalid and is lost
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col_idx)} is full. Player {current_token} loses the turn.")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[row_idx][col_idx] = current_token

        # Print updated board
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
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
