import os
import random
import string
import sys

# =========================
# Configuration (Submission requires 6x7 and 2 players)
# =========================
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # In order

# =========================
# Validation of configuration
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


# =========================
# Board utilities
# =========================
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # As required by assignment (Linux/Unix)
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    border = "+" + "---+" * cols
    for r in range(rows):
        print(border)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(border)


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def drop_checker(board, col, checker):
    """
    Attempts to drop 'checker' into column 'col'.
    Returns the row index where the checker lands, or None if column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None


# =========================
# Input handling
# =========================
def get_valid_column_input(num_cols):
    """
    Prompts the user until a valid column letter (A.. up to num_cols) is entered.
    Returns the zero-based column index.
    """
    valid_letters = [string.ascii_uppercase[i] for i in range(num_cols)]
    while True:
        user_in = input("Please enter a column: ").strip().upper()
        if len(user_in) != 1:
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue
        if user_in not in valid_letters:
            print(f"Invalid column. Valid columns are: {', '.join(valid_letters)}")
            continue
        return valid_letters.index(user_in)


# =========================
# Win checking
# =========================
def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


# =========================
# Game loop
# =========================
def main():
    board = create_board(ROWS, COLS)

    # Initial print to show empty board
    print_board(board)

    # Randomly select starting player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        current_checker = PLAYERS[current_idx]
        print(f"Player {current_checker}, it's your turn.")
        # If board is already full at turn start, it's a draw
        if is_board_full(board):
            print("It's a draw! The board is full.")
            break

        # Ask for column input (validated)
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_column_input(COLS)

        # Attempt to drop checker
        row_placed = drop_checker(board, col, current_checker)
        if row_placed is None:
            # Column full: lose the turn
            print_board(board)
            col_letter = string.ascii_uppercase[col]
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After placing, print updated board
        print_board(board)

        # Check win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if is_board_full(board):
            print("It's a draw! The board is full.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
