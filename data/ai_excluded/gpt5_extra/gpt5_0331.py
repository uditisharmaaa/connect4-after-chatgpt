import os
import random
import string
import sys

# -------------------------
# Configuration (change if needed for testing; submission requires these defaults)
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
# -------------------------

def clear_screen():
    os.system('clear')


def get_column_labels(n):
    # Labels A, B, C, ...
    if n < 1 or n > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    return list(string.ascii_uppercase[:n])


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, col_labels):
    # Header labels
    header = "  " + "   ".join(col_labels)
    print(header)
    # Top border
    horizontal = "+" + "+".join(["---"] * len(col_labels)) + "+"
    for r in range(len(board)):
        print(horizontal)
        row_cells = []
        for c in range(len(col_labels)):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(horizontal)


def is_column_full(board, col):
    # If top-most row is not empty, column is full
    return board[0][col] != " "


def drop_checker(board, col, checker):
    # Place checker at the lowest empty row in the column.
    # Returns the row index where the checker landed, or None if column is full.
    if is_column_full(board, col):
        return None
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Should not reach here if not full


def count_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def has_won(board, last_r, last_c, checker):
    # Check four directions: horizontal, vertical, diag1, diag2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include the last placed checker
        total += count_direction(board, last_r, last_c, dr, dc, checker)
        total += count_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    # If no spaces in top row, the board is full
    return all(cell != " " for cell in board[0])


def validate_config():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLUMNS < 1 or COLUMNS > 26:
        raise ValueError("COLUMNS must be between 1 and 26.")
    if ROWS < WIN_LENGTH and COLUMNS < WIN_LENGTH:
        raise ValueError("Board too small for a win condition.")
    # Ensure we have enough checker symbols
    if NUM_PLAYERS > len(CHECKERS):
        raise ValueError("Not enough checker symbols for the number of players.")


def prompt_for_column(col_labels, current_checker):
    label_min = col_labels[0]
    label_max = col_labels[-1]
    while True:
        try:
            entry = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        except EOFError:
            # Gracefully exit on EOF
            print()
            sys.exit(0)
        except KeyboardInterrupt:
            print()
            sys.exit(0)
        if len(entry) != 1 or not entry.isalpha():
            print(f"Invalid input. Please enter a single letter between {label_min} and {label_max}.")
            continue
        if entry < label_min or entry > label_max:
            print(f"Invalid column. Please choose between {label_min} and {label_max}.")
            continue
        return entry


def main():
    validate_config()
    rows, cols = ROWS, COLUMNS
    players = CHECKERS[:NUM_PLAYERS]
    col_labels = get_column_labels(cols)
    board = create_board(rows, cols)

    # Randomly choose starting player
    current_index = random.randrange(NUM_PLAYERS)

    total_moves = 0
    while True:
        clear_screen()
        print_board(board, col_labels)

        current_checker = players[current_index]
        col_label = prompt_for_column(col_labels, current_checker)
        col_idx = ord(col_label) - ord('A')

        placed_row = drop_checker(board, col_idx, current_checker)
        if placed_row is None:
            # Column full -> turn lost
            print(f"Column {col_label} is full. Turn lost.")
            # Next player's turn
            current_index = (current_index + 1) % NUM_PLAYERS
            # Brief pause-like behavior without importing time; wait for Enter to acknowledge
            try:
                input("Press Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                print()
                sys.exit(0)
            continue

        total_moves += 1

        # Check for win
        if has_won(board, placed_row, col_idx, current_checker):
            clear_screen()
            print_board(board, col_labels)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board, col_labels)
            print("Draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
