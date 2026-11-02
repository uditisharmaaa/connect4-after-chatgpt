import os
import random
import string
import sys

# =======================
# Configuration constants
# =======================
ROWS = 6              # number of rows (height)
COLS = 7              # number of columns (width), max 26
NUM_PLAYERS = 2       # number of players, between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]  # in order

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]


# =======================
# Utility / Game functions
# =======================
def clear_screen():
    # As per assignment, use Unix clear
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0

    # Column headers (A, B, C, ...)
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal separator line
    line = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(line)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(line)


def column_from_input(user_input, cols):
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return None


def get_valid_column_input(cols):
    letters = string.ascii_uppercase[:cols]
    prompt = f"Please enter a column ({letters[0]}-{letters[-1]}): "
    while True:
        s = input(prompt).strip().upper()
        idx = column_from_input(s, cols)
        if idx is not None:
            return idx
        print("Invalid input. Enter a single letter within the board range.")


def drop_checker(board, col, checker):
    # Place the checker in the lowest empty row in the given column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, delta_r, delta_c, checker):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + delta_r, start_c + delta_c
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += delta_r
        c += delta_c
    return count


def check_win(board, last_r, last_c, checker):
    # Check lines through (last_r, last_c) in 4 directions
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # include the last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, checker)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= 4:
            return True
    return False


def is_draw(board):
    # Draw if no spaces in the top row (or any row)
    for row in board:
        if " " in row:
            return False
    return True


def game_loop():
    board = create_board(ROWS, COLS)
    # Random starting player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial display before the game starts
    clear_screen()
    print_board(board)

    while True:
        current_checker = PLAYER_TOKENS[current_idx]
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_column_input(COLS)

        # Attempt to drop the checker
        placed_row = drop_checker(board, col, current_checker)

        # After action, clear and reprint board
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column full, player loses turn
            col_letter = string.ascii_uppercase[col]
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Check for win from the last placed position
        if check_win(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


def main():
    # As per submission requirements: 6x7 board, 2 players enabled by the constants above.
    game_loop()


if __name__ == "__main__":
    main()
