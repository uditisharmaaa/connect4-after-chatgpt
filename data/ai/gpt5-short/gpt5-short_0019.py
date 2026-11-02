import os
import random
from typing import List, Optional, Tuple

# ---------------------------
# Configuration constants
# ---------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = tuple("ABCDEFG")

# Allowed player symbols in fixed order. Use the first NUM_PLAYERS of these.
PLAYER_SYMBOLS = ("X", "O", "V", "H", "M")

# Set the number of players here (between 2 and 5 inclusive).
NUM_PLAYERS = 2  # change to 3, 4, or 5 if desired


# ---------------------------
# Utility functions
# ---------------------------
def clear_screen() -> None:
    # As requested, use this specific clear command.
    os.system("clear")


def make_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    # Header with column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    # Rows from top (row 0) to bottom (row ROWS-1)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c] if board[r][c] != " " else ".")
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * COLS)


def column_from_input(user_in: str) -> Optional[int]:
    if not user_in:
        return None
    ch = user_in.strip().upper()
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return None


def first_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    # Drop from bottom up; find the lowest empty row.
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def is_board_full(board: List[List[str]]) -> bool:
    # If top row has no spaces in any column, it's full.
    return all(board[0][c] != " " for c in range(COLS))


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS


def count_direction(
    board: List[List[str]],
    r: int,
    c: int,
    dr: int,
    dc: int,
    symbol: str,
) -> int:
    """
    Count consecutive pieces of 'symbol' starting at (r, c) and stepping by (dr, dc),
    including the starting cell.
    """
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count


def is_winning_move(
    board: List[List[str]],
    last_row: int,
    last_col: int,
    symbol: str,
) -> bool:
    """
    Check all 4 directions passing through the last placed piece:
    - Horizontal (0,1)
    - Vertical (1,0)
    - Diagonal down-right (1,1)
    - Diagonal up-right (-1,1)
    We count both directions and subtract 1 to avoid double-counting the center.
    """
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = (
            count_direction(board, last_row, last_col, dr, dc, symbol)
            + count_direction(board, last_row, last_col, -dr, -dc, symbol)
            - 1
        )
        if total >= 4:
            return True
    return False


def get_active_players() -> Tuple[str, ...]:
    n = NUM_PLAYERS
    if not isinstance(n, int) or n < 2 or n > 5:
        print(f"NUM_PLAYERS={n} is invalid; defaulting to 2 players.")
        n = 2
    return PLAYER_SYMBOLS[:n]


def prompt_for_move(current_symbol: str, board: List[List[str]]) -> int:
    while True:
        user_in = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
        col = column_from_input(user_in)
        if col is None:
            print("Invalid input. Please enter a letter from A to G.")
            continue
        row = first_empty_row(board, col)
        if row is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose a different column.")
            continue
        return col


# ---------------------------
# Main game loop
# ---------------------------
def main() -> None:
    random.seed()
    players = list(get_active_players())
    board = make_board()

    # Randomly choose starting player index
    turn_index = random.randrange(len(players))

    winner: Optional[str] = None

    while True:
        clear_screen()
        print_board(board)
        current = players[turn_index]

        # Get and apply move
        col = prompt_for_move(current, board)
        row = first_empty_row(board, col)
        assert row is not None  # guarded by prompt_for_move

        board[row][col] = current

        # Check win
        if is_winning_move(board, row, col, current):
            winner = current
            clear_screen()
            print_board(board)
            print(f"Player {winner} wins! Connect 4 achieved.")
            break

        # Check draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            break

        # Next player's turn
        turn_index = (turn_index + 1) % len(players)


if __name__ == "__main__":
    main()
