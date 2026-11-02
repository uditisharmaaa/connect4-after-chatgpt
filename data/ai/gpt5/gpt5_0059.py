import os
import random
import string
from typing import List, Optional, Tuple

# ========= Configuration (you may change these for testing) =========
ROWS = 6                   # Number of rows (default 6)
COLS = 7                   # Number of columns (default 7, max 26)
NUM_PLAYERS = 2            # Number of players (2 to 5)
WIN_LEN = 4                # Number of connected checkers to win (fixed at 4)
CHECKER_ORDER = ["X", "O", "V", "H", "M"]  # Player checkers in order
# ====================================================================

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= ROWS and 1 <= COLS <= 26):
    raise ValueError("ROWS must be >= 1 and COLS must be between 1 and 26.")

PLAYERS = CHECKER_ORDER[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen() -> None:
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    for r in range(ROWS):
        print(sep)
        row_cells = "|"
        for c in range(COLS):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
    print(sep)


def find_lowest_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    # Return the row index where a checker would land in the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    row = find_lowest_empty_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return (row, col)


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win_from_cell(board: List[List[str]], row: int, col: int, checker: str) -> bool:
    # Check all 4 directions: horizontal, vertical, diag down-right, diag down-left
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # include the starting cell
        # Check forward
        r, c = row + dr, col + dc
        while in_bounds(r, c) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward
        r, c = row - dr, col - dc
        while in_bounds(r, c) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LEN:
            return True
    return False


def check_win(board: List[List[str]], last_move: Optional[Tuple[int, int]]) -> Optional[str]:
    # If we know the last move, only check from there for efficiency
    if last_move is not None:
        r, c = last_move
        checker = board[r][c]
        if checker != " " and check_win_from_cell(board, r, c, checker):
            return checker
        return None
    # Fallback: scan all cells (not usually necessary)
    for r in range(ROWS):
        for c in range(COLS):
            ch = board[r][c]
            if ch != " " and check_win_from_cell(board, r, c, ch):
                return ch
    return None


def check_draw(board: List[List[str]]) -> bool:
    # Draw if no empty cells remain
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def get_column_input() -> int:
    while True:
        user_input = input("Please enter a column: ").strip()
        if len(user_input) != 1:
            print("Invalid input. Enter a single letter corresponding to a column.")
            continue
        ch = user_input.upper()
        if ch not in COLUMN_LABELS:
            print(f"Invalid column. Choose a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        return COLUMN_LABELS.index(ch)


def main() -> None:
    random.seed()
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    clear_screen()
    print_board(board)

    # Game loop
    last_move: Optional[Tuple[int, int]] = None

    while True:
        current_checker = PLAYERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        col = get_column_input()

        placed = drop_checker(board, col, current_checker)
        if placed is None:
            # Column full: turn is invalid and player loses the turn
            col_label = COLUMN_LABELS[col]
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # No move placed; last_move remains the same
        else:
            last_move = placed

        # Print updated board
        clear_screen()
        print_board(board)

        # Check for win
        winner = check_win(board, last_move if placed is not None else None)
        if winner is not None:
            print(f"Player {winner} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
