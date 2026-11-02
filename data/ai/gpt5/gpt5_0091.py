import os
import random
import string
import sys

# ---------- Configuration (Submission requires 6 rows x 7 cols and 2 players) ----------
ROWS = 6
COLS = 7  # Max 26 (A..Z)
NUM_PLAYERS = 2  # Supported: 2..5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# ---------- Validation of configuration ----------
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


# ---------- Game logic functions ----------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # Linux/Unix as per assignment
    os.system("clear")


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column labels
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(labels)
    print(header)
    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"
    # Rows
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def column_from_input(inp, cols):
    if not inp:
        return None
    ch = inp.strip().upper()
    if len(ch) != 1:
        return None
    if ch < "A" or ch >= chr(ord("A") + cols):
        return None
    return ord(ch) - ord("A")


def drop_checker(board, col, checker):
    # Place checker in the lowest available row in given column.
    # Return placed row index or None if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        if count >= WIN_COUNT:
            return True
        r += dr
        c += dc
    return False


def check_win(board, checker):
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
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                # Only need to check if enough space remains for a win
                end_r = r + (WIN_COUNT - 1) * dr
                end_c = c + (WIN_COUNT - 1) * dc
                if not in_bounds(end_r, end_c, rows, cols):
                    continue
                if check_direction(board, r, c, dr, dc, checker):
                    return True
    return False


def check_draw(board):
    # Draw if top row has no spaces (board full)
    return all(cell != " " for cell in board[0])


# ---------- Main game loop ----------
def main():
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    print_board(board)

    while True:
        current_player = PLAYERS[current_idx]
        try:
            # Display prompt with current player
            print(f"Player {current_player}, please enter a column:")
            user_inp = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame terminated.")
            return

        # Validate input (re-prompt until valid letter)
        col = column_from_input(user_inp, COLS)
        while col is None:
            print_board(board)
            print("Invalid input. Please enter a valid column letter (e.g., A-G).")
            print(f"Player {current_player}, please enter a column:")
            try:
                user_inp = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGame terminated.")
                return
            col = column_from_input(user_inp, COLS)

        # Try to place checker
        placed_row = drop_checker(board, col, current_player)
        if placed_row is None:
            # Column full, lose turn
            print_board(board)
            label = string.ascii_uppercase[col]
            print(f"Column {label} is full. Player {current_player} loses the turn.")
            # Check for draw even after a lost turn (board state unchanged, but safe)
            if check_draw(board):
                print("It's a draw!")
                return
            # Next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move: show updated board
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            return

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
