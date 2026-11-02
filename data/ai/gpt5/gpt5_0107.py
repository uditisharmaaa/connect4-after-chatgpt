import os
import random
from typing import List, Optional, Tuple

# ------------------------
# Configuration constants
# ------------------------
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
WIN_LENGTH = 4

CHECKER_ORDER = ["X", "O", "V", "H", "M"]

# ------------------------
# Validation of constants
# ------------------------
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert 1 <= ROWS and 1 <= COLS <= 26, "Board must have at least 1 row and up to 26 columns."
PLAYERS = CHECKER_ORDER[:NUM_PLAYERS]


# ------------------------
# Utility functions
# ------------------------
def clear_screen() -> None:
    os.system('clear')


def column_labels(n: int) -> List[str]:
    return [chr(ord('A') + i) for i in range(n)]


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    cols = len(board[0])
    labels = column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(len(board)):
        row_cells = "|"
        for c in range(cols):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
        print("+" + ("---+" * cols))


def get_valid_column_input(valid_labels: List[str], current_checker: str) -> str:
    while True:
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip()
        if len(user_input) == 1 and user_input.isalpha():
            letter = user_input.upper()
            if letter in valid_labels:
                return letter
        print("Invalid input. Please enter a valid column letter.")


def find_available_row(board: List[List[str]], col: int) -> Optional[int]:
    # Start from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board: List[List[str]], row: int, col: int, checker: str) -> None:
    board[row][col] = checker


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], checker: str) -> bool:
    rows = len(board)
    cols = len(board[0])

    directions: List[Tuple[int, int]] = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= WIN_LENGTH:
                    return True
    return False


def check_draw(board: List[List[str]]) -> bool:
    # Draw if there is no empty cell left
    for row in board:
        if " " in row:
            return False
    return True


# ------------------------
# Main game loop
# ------------------------
def main() -> None:
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)

    while True:
        current_checker = PLAYERS[current_player_index]

        # Prompt for input
        col_letter = get_valid_column_input(labels, current_checker)
        col_index = labels.index(col_letter)

        # Attempt to place checker
        row_index = find_available_row(board, col_index)

        if row_index is None:
            # Column full, turn is lost
            print(f"Column {col_letter} is full. Turn lost.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        place_checker(board, row_index, col_index, current_checker)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
