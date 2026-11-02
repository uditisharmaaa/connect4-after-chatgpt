import os
import random

# ====== Constants (adjustable, but submission uses these defaults) ======
ROWS = 6                  # number of rows (default 6)
COLS = 7                  # number of columns (default 7, max 26)
NUM_PLAYERS = 2           # number of players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4            # always 4 in a row to win
MAX_COLS = 26             # do not exceed 26 columns (A-Z)

# ====== Safety checks on constants ======
if COLS > MAX_COLS:
    COLS = MAX_COLS
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Create a rows x cols board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Print column headers (A, B, C, ...)
    # Example: "  A   B   C ..."
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)

    # Separator line: +---+---+...
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"

    for r in range(len(board)):
        print(sep)
        # Row content: | X |   | O | ...
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def get_lowest_empty_row(board, col):
    # Return the index of the lowest empty row in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, row, col, token):
    board[row][col] = token


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, token):
    # Count consecutive tokens in a given direction (including start cell)
    count = 0
    r, c = start_r, start_c
    rows, cols = len(board), len(board[0])
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, token):
    rows, cols = len(board), len(board[0])
    # Directions to check: right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                # Count in positive direction
                pos = check_direction(board, r, c, dr, dc, token)
                # Count in negative direction (excluding starting cell to avoid double count)
                neg = check_direction(board, r - dr, c - dc, -dr, -dc, token)
                if pos + neg >= WIN_LENGTH:
                    return True
    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_valid_column_input(cols):
    # Prompt until input is a valid column letter within range.
    # Does not handle full column (that's treated as a lost turn separately).
    while True:
        user_in = input().strip()
        if not user_in:
            print("Invalid input. Please enter a column letter:")
            continue
        user_in = user_in.upper()
        if len(user_in) != 1 or not ('A' <= user_in <= chr(ord('A') + cols - 1)):
            print("Invalid input. Please enter a valid column letter:")
            continue
        return ord(user_in) - ord('A'), user_in


def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display before the game starts
    clear_screen()
    print_board(board)

    while True:
        current_token = PLAYER_TOKENS[current_player_index]
        print(f"Player {current_token}, please enter a column:")

        col_index, col_label = get_valid_column_input(COLS)

        # Try to place the checker
        row_index = get_lowest_empty_row(board, col_index)

        if row_index is None:
            # Column is full; lose the turn
            clear_screen()
            print_board(board)
            print(f"Column {col_label} is full. Player {current_token} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place checker
        place_checker(board, row_index, col_index, current_token)

        # After move: clear and show board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
