import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# =========================
# Derived/global constants
# =========================
PLAYER_MARKS_ALL = ['X', 'O', 'V', 'H', 'M']
PLAYER_MARKS = PLAYER_MARKS_ALL[:max(2, min(5, NUM_PLAYERS))]
COLS = max(1, min(26, COLS))  # Safety clamp
ROWS = max(1, ROWS)  # Safety clamp
COL_LABELS = [string.ascii_uppercase[i] for i in range(COLS)]

# =========================
# Utility functions
# =========================
def clear_screen():
    # As required, clear with 'clear' (Unix-like). Fall back to printing newlines.
    try:
        os.system('clear')
    except Exception:
        print("\n" * 100)


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header = "  " + "   ".join(COL_LABELS[:cols])
    print(header)

    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def get_column_input():
    while True:
        user_input = input("Please enter a column (A-{}): ".format(COL_LABELS[COLS - 1])).strip().upper()
        if len(user_input) != 1 or user_input not in COL_LABELS[:COLS]:
            print("Invalid input. Enter a single letter between A and {}.".format(COL_LABELS[COLS - 1]))
            continue
        return COL_LABELS.index(user_input)


def lowest_empty_row(board, col):
    # Return the lowest available row index in column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, row, col, mark):
    board[row][col] = mark


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, mark):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == mark:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, mark):
    # Check 4 in a row around the last placed checker
    # Directions: horizontal, vertical, diag1 (\), diag2 (/)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include last placed
        total += count_in_direction(board, last_r, last_c, dr, dc, mark)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, mark)
        if total >= 4:
            return True
    return False


def check_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current_idx, total_players):
    return (current_idx + 1) % total_players


def game_setup():
    if len(PLAYER_MARKS) < 2 or len(PLAYER_MARKS) > 5:
        print("Configuration error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS > 26:
        print("Configuration error: COLS must be at most 26.")
        sys.exit(1)
    return create_board(ROWS, COLS)


def main():
    board = game_setup()
    players = PLAYER_MARKS
    current_player_idx = random.randrange(len(players))

    # Initial board print and prompt statement
    print_board(board)

    winner = None
    while True:
        current_mark = players[current_player_idx]
        print(f"Player {current_mark}, please enter a column:")

        # Get a valid column letter input
        col = get_column_input()

        row = lowest_empty_row(board, col)
        if row is None:
            # Column full: invalid move, lose the turn
            print_board(board)
            print(f"Column {COL_LABELS[col]} is full. Player {current_mark} loses the turn.")
            current_player_idx = next_player_index(current_player_idx, len(players))
            continue

        # Place the checker
        place_checker(board, row, col, current_mark)

        # Show updated board
        print_board(board)

        # Check for win
        if check_win(board, row, col, current_mark):
            winner = current_mark
            print(f"Player {winner} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(players))

    # End of game
    # No extra input/output


if __name__ == "__main__":
    main()
