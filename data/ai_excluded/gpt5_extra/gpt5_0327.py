import os
import random
import string
import sys

# ---------- Configuration (constants) ----------
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 per assignment

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

PLAYER_MARKS = CHECKERS[:NUM_PLAYERS]


# ---------- Utility functions ----------
def clear_screen():
    os.system('clear')


def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        row_cells = "|" + "|".join([f" {board[r][c]} " for c in range(cols)]) + "|"
        print(row_cells)
    print(border)


def col_letter_to_index(letter, cols):
    letter = letter.upper()
    if len(letter) != 1:
        return None
    if letter < 'A' or letter >= chr(ord('A') + cols):
        return None
    return ord(letter) - ord('A')


def get_valid_column_input(cols, current_player_mark):
    # Keep asking until input is a valid column letter in range
    while True:
        user_in = input(f"Player {current_player_mark}, please enter a column: ").strip().upper()
        idx = col_letter_to_index(user_in, cols)
        if idx is None:
            print("Invalid input. Please enter a single uppercase letter within the board range.")
            continue
        return idx, user_in  # return both index and original letter


def drop_checker(board, col, mark):
    # Place at lowest available row in the column; return row index or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = mark
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board, row, col, mark):
    # Check 4 in a row including (row, col)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include the last placed checker

        # forward direction
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == mark:
            count += 1
            r += dr
            c += dc

        # backward direction
        r, c = row - dr, col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == mark:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def board_full(board):
    return all(cell != " " for row in board for cell in row)


# ---------- Game loop ----------
def main():
    board = make_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    # Game loop
    while True:
        current_mark = PLAYER_MARKS[current_player]

        # Print board before each player's turn (already printed at start, but do again for clarity)
        print_board(board)

        # Ask for valid column letter; invalid inputs re-prompt without losing turn
        col_idx, col_letter = get_valid_column_input(COLS, current_mark)

        # Try to drop checker; if column full, turn is invalid and the player loses the turn
        placed_row = drop_checker(board, col_idx, current_mark)
        if placed_row is None:
            print(f"Column {col_letter} is full. Turn lost.")
            input("Press Enter to continue...")
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # After a valid move, print updated board
        print_board(board)

        # Check for win
        if check_win_from(board, placed_row, col_idx, current_mark):
            print(f"Player {current_mark} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
