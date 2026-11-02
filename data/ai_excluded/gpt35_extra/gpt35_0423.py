import os
import random
import sys

# === CONSTANTS ===
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# Adjust these for submission requirements:
NUM_PLAYERS = 2
PLAYERS_IN_GAME = PLAYERS[:NUM_PLAYERS]
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]

# === FUNCTIONS ===


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    # Board is ROWS rows x COLS columns.
    # board[row][col] addressing. row 0 top, row ROWS-1 bottom.
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COL_LABELS))
    # Print top border
    line_sep = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line_sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|"
        print(row_cells)
    print(line_sep)


def valid_column_input(col_input):
    # Must be single uppercase letter in range of board columns
    if len(col_input) != 1:
        return False
    if col_input not in COL_LABELS:
        return False
    return True


def column_index(col_input):
    return ord(col_input) - ord('A')


def place_checker(board, col, checker):
    """
    Places checker in the column col.
    Returns True if successful, else False (column full).
    """
    # Start placement from bottom row upwards
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full


def check_win(board, checker):
    # Check horizontal, vertical and diagonal for WIN_COUNT
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c + offset] == checker for offset in range(WIN_COUNT)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r + offset][c] == checker for offset in range(WIN_COUNT)):
                return True
    # diagonal down-right
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(WIN_COUNT)):
                return True
    # diagonal up-right
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r - offset][c + offset] == checker for offset in range(WIN_COUNT)):
                return True
    return False


def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))


def input_column(current_player):
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not valid_column_input(user_input):
            # invalid input - retry
            continue
        col = column_index(user_input)
        if col < 0 or col >= COLS:
            # outside board
            continue
        return col


def main():
    board = create_board(ROWS, COLS)
    # Random starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        curr_checker = PLAYERS_IN_GAME[current_player_idx]

        # Get valid column input
        col = input_column(curr_checker)

        # Attempt to place checker, if fail (column full), lose turn
        success = place_checker(board, col, curr_checker)
        if not success:
            # Player loses turn silently, no reinput:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_win(board, curr_checker):
            print(f"Player {curr_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit()
