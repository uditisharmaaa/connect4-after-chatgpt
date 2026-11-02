import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # must be <= 26
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]  # in order

# Safety checks for configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = TOKENS[:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    # As per assignment: clear using 'clear'
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header letters
    header = "  " + "   ".join(COLUMN_LABELS)
    # Horizontal separator line
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(sep)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def input_column(prompt):
    while True:
        try:
            s = input(prompt)
        except EOFError:
            # End game gracefully on EOF
            print()
            sys.exit(0)
        except KeyboardInterrupt:
            print()
            sys.exit(0)

        s = s.strip().upper()

        # Validate: exactly one alphabetic character that is within column range
        if len(s) != 1 or not s.isalpha():
            # Invalid: numbers, symbols, multiple chars, etc.
            continue
        if s not in COLUMN_LABELS:
            # Out of board
            continue
        return COLUMN_LABELS.index(s)


def drop_checker(board, col_index, token):
    # Attempt to place token in the lowest available row in this column.
    # Returns the row index where placed, or None if column is full.
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return r
    return None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, token):
    # Directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if not in_bounds(rr, cc) or board[rr][cc] != token:
                        break
                    count += 1
                if count == 4:
                    return True
    return False


def check_draw(board):
    # Draw if no spaces left on the board
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    random.seed()
    board = create_board(ROWS, COLS)

    # Randomly select first player index
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        token = PLAYERS[current_idx]
        # Prompt current player
        col_index = input_column(f"Player {token}, please enter a column: ")

        # Try to drop the checker
        placed_row = drop_checker(board, col_index, token)

        # Clear screen and print updated (or unchanged if column full) board
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column full: invalid turn, player loses the turn
            # No need to check for a win (no change on board)
            # Proceed to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After a valid placement, check for win
        if check_win(board, token):
            print(f"Player {token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
