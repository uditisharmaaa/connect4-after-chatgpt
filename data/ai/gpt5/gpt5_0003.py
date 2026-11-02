import os
import random
import string
from typing import List, Optional, Tuple

# --------- Configuration (submission should use 6 rows x 7 cols and 2 players) ---------
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
CONNECT_N = 4

# Player checkers in order of assignment
CHECKER_SET = ["X", "O", "V", "H", "M"]
CHECKERS = CHECKER_SET[:NUM_PLAYERS]

# --------- Helpers ---------
def clear_screen() -> None:
    # Per assignment requirement (Linux/Unix terminal)
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(labels))

    # Grid
    horizontal = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(horizontal)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(horizontal)


def column_from_input(inp: str, max_cols: int) -> Optional[int]:
    if len(inp) != 1:
        return None
    ch = inp.upper()
    if ch < 'A' or ch > 'Z':
        return None
    idx = ord(ch) - ord('A')
    if 0 <= idx < max_cols:
        return idx
    return None


def get_valid_input(current_checker: str, num_cols: int) -> int:
    # Keep prompting until user enters a valid column letter
    while True:
        user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        col = column_from_input(user_in, num_cols)
        if col is not None:
            return col
        print("Invalid input. Please enter a valid column letter.")


def place_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    # Place checker in the lowest available row in the given column.
    # Returns (row, col) if placed, otherwise None if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return (r, col)
    return None


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, checker: str) -> int:
    # Count consecutive checkers in one direction starting from (start_r, start_c) inclusive
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board: List[List[str]], last_r: int, last_c: int, checker: str) -> bool:
    # Check 4-in-a-row including the last placed checker, for all 4 principal directions.
    # Directions: horizontal (0,1), vertical (1,0), diag1 (1,1), diag2 (1,-1)
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        # Count both directions, subtract 1 to not double-count the last checker
        forward = check_direction(board, last_r, last_c, dr, dc, checker)
        backward = check_direction(board, last_r, last_c, -dr, -dc, checker)
        if forward + backward - 1 >= CONNECT_N:
            return True
    return False


def board_full(board: List[List[str]]) -> bool:
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def next_player_index(curr: int, total: int) -> int:
    return (curr + 1) % total


def validate_configuration() -> None:
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
    assert 1 <= COLS <= 26, "COLS must be between 1 and 26."
    assert ROWS >= 1, "ROWS must be at least 1."
    assert CONNECT_N >= 2, "CONNECT_N must be at least 2."
    # Having fewer cells than needed to possibly win is allowed but will always draw.


# --------- Game Loop ---------
def main() -> None:
    validate_configuration()
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board before the game starts
    clear_screen()
    print_board(board)

    while True:
        checker = CHECKERS[current_player_idx]

        # Prompt for input on the current board state
        col = get_valid_input(checker, COLS)

        # Try placing the checker
        placed = place_checker(board, col, checker)

        if placed is None:
            # Column full: player loses the turn (no retry)
            col_label = string.ascii_uppercase[col]
            print(f"Column {col_label} is full. Player {checker} loses the turn.")
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            # Proceed to next turn; display board for next player
            clear_screen()
            print_board(board)
            continue

        last_r, last_c = placed

        # After a valid move, check for win/draw and show the updated board
        clear_screen()
        print_board(board)

        if check_win(board, last_r, last_c, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)


if __name__ == "__main__":
    main()
