import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7            # Max 26
NUM_PLAYERS = 2     # 2 to 5
WIN_COUNT = 4

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# =========================
# Utility and game logic
# =========================

def clear_screen():
    # Clear screen on Unix/Linux
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(n):
    # Labels A.. up to 26
    return list(string.ascii_uppercase[:n])

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    print(border)
    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(border)

def find_drop_row(board, col_idx):
    # Return the row index where the checker should land, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None

def is_within(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_COUNT and is_within(board, nr, nc) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= WIN_COUNT:
                    return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_valid_input(cols):
    labels = column_labels(cols)
    prompt = "Please enter a column: "
    while True:
        try:
            user_in = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        if len(user_in) != 1:
            print(f"Invalid input. Enter a single letter between {labels[0]} and {labels[-1]}.")
            continue
        letter = user_in.upper()
        if letter not in labels:
            print(f"Invalid column. Enter a letter between {labels[0]} and {labels[-1]}.")
            continue
        return labels.index(letter), letter

def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)

    while True:
        current_symbol = symbols[current]
        labels = column_labels(COLS)
        print(f"Player {current_symbol}, please enter a column:")
        col_idx, col_label = get_valid_input(COLS)

        # Attempt to place checker
        row_idx = find_drop_row(board, col_idx)
        if row_idx is None:
            # Column full: lose the turn
            print_board(board)
            print(f"Column {col_label} is full. Player {current_symbol} loses the turn.")
            # Switch to next player
            current = (current + 1) % NUM_PLAYERS
            continue

        # Place checker
        board[row_idx][col_idx] = current_symbol

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
