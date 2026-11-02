import os
import random
import sys

# ====== Configuration Constants ======
ROWS = 6                # Number of rows (default submission requires 6)
COLS = 7                # Number of columns (default submission requires 7, max 26)
NUM_PLAYERS = 2         # Number of players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4          # Players need 4 in a row to win

# ====== Validation of Configuration ======
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26 or COLS < 1:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


# ====== Game Functions ======
def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels (A..)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def is_valid_column_input(s):
    # Accept a single alphabetic character; we will check bounds separately
    if not s or len(s.strip()) == 0:
        return False
    s = s.strip()
    if len(s) != 1:
        return False
    return s.isalpha()


def get_column_index_from_input(s):
    # Convert letter to column index (A->0, B->1, ...)
    letter = s.strip().upper()
    idx = ord(letter) - ord('A')
    return idx


def column_is_full(board, col):
    return board[0][col] != " "


def drop_checker(board, col, symbol):
    # Place symbol in the lowest available row in the column.
    # Returns the row index where the checker was placed, or None if column full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None


def check_win(board, last_row, last_col, symbol):
    # Check for 4 in a row through (last_row, last_col) in all directions.
    directions = [
        (0, 1),    # horizontal
        (1, 0),    # vertical
        (1, 1),    # diag down-right
        (1, -1),   # diag down-left
    ]

    rows = len(board)
    cols = len(board[0])

    def count_dir(r, c, dr, dc):
        count = 0
        rr, cc = r, c
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        return count

    for dr, dc in directions:
        # Count both directions from the last placed checker, subtract 1 to avoid double-counting center
        total = count_dir(last_row, last_col, dr, dc) + count_dir(last_row, last_col, -dr, -dc) - 1
        if total >= WIN_LENGTH:
            return True
    return False


def check_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_idx]
        # Prompt and validate input (repeat until valid letter inside board)
        while True:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip()
            if not is_valid_column_input(user_input):
                print("Invalid input. Please enter a single letter corresponding to a column.")
                continue
            col_idx = get_column_index_from_input(user_input)
            if not (0 <= col_idx < COLS):
                print("Invalid column. Please enter a letter within the board range.")
                continue
            break  # valid input format and within board

        # Attempt to drop checker
        if column_is_full(board, col_idx):
            print(f"Column {chr(ord('A') + col_idx)} is full. Turn lost.")
            # Switch player due to losing the turn
            current_player_idx = (current_player_idx + 1) * 1 % NUM_PLAYERS
            # Show board again for clarity
            clear_screen()
            print_board(board)
            continue

        placed_row = drop_checker(board, col_idx, current_symbol)

        # Update display
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, placed_row, col_idx, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
