import os
import random
import string
import sys

# Configuration constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7   # Max 26 (A-Z)
NUM_PLAYERS = 2  # Supports 2–5

# Allowed player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row needed to win
WIN_COUNT = 4


def clear_screen():
    # As per assignment requirement
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Top border line
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep_line)
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep_line)


def get_column_input(max_cols, current_player_checker):
    max_letter = string.ascii_uppercase[max_cols - 1]
    while True:
        try:
            inp = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        except EOFError:
            # If input stream closes, exit gracefully
            sys.exit(0)
        if len(inp) != 1:
            print("Invalid input. Enter a single letter corresponding to a column.")
            continue
        if inp < "A" or inp > max_letter:
            print(f"Invalid column. Please enter a letter between A and {max_letter}.")
            continue
        return ord(inp) - ord('A'), inp  # return both index and letter for messages


def place_checker(board, col, checker):
    # Place at lowest empty row in the given column. Return row index or None if full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, r, c, checker):
    # Check all 4 directions (pairs of opposite directions)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # include the placed checker
        total += count_in_direction(board, r, c, dr, dc, checker)
        total += count_in_direction(board, r, c, -dr, -dc, checker)
        if total >= WIN_COUNT:
            return True
    return False


def is_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Validate configuration
    cols = max(1, min(COLS, 26))  # enforce A-Z limit
    rows = ROWS
    num_players = max(2, min(NUM_PLAYERS, 5))
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)

    # Randomly choose the starting player
    current_player_index = random.randrange(num_players)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col_idx, col_letter = get_column_input(cols, current_checker)

        placed_row = place_checker(board, col_idx, current_checker)

        # Clear and print updated board after the attempt
        clear_screen()
        print_board(board)

        if placed_row is None:
            print(f"Column {col_letter} is full. Turn lost.")
            # Turn is lost; move to next player
            current_player_index = (current_player_index + 1) % num_players
            continue

        # Check for win
        if check_win(board, placed_row, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

    # End of game


if __name__ == "__main__":
    main()
