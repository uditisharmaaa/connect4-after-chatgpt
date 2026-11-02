import os
import random
import string
from typing import List, Optional, Tuple

# ==========================
# Configuration (constants)
# ==========================
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]

# Sanity checks for configuration
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert 1 <= ROWS, "ROWS must be at least 1."
assert 1 <= COLS <= 26, "COLS must be between 1 and 26."
assert NUM_PLAYERS <= len(PLAYER_MARKERS), "Not enough markers for players."


def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels
    labels = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(labels))
    print("+" + ("---+" * cols))

    # Rows (top to bottom)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))


def column_from_input(inp: str, max_cols: int) -> Optional[int]:
    if not inp or len(inp) != 1:
        return None
    ch = inp.upper()
    labels = string.ascii_uppercase[:max_cols]
    if ch in labels:
        return labels.index(ch)
    return None


def get_valid_input(cols: int, current_player_marker: str) -> int:
    # Keep asking until a valid column letter is provided
    while True:
        user_inp = input(f"Player {current_player_marker}, please enter a column: ").strip()
        col = column_from_input(user_inp, cols)
        if col is not None:
            return col
        print("Invalid input. Please enter a valid column letter.")


def place_checker(board: List[List[str]], col: int, marker: str) -> Optional[Tuple[int, int]]:
    """
    Attempt to place a marker in the given column.
    Returns (row, col) if placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = marker
            return (r, col)
    return None


def in_bounds(board: List[List[str]], r: int, c: int) -> bool:
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def check_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, marker: str) -> int:
    """
    Count continuous markers including start cell (assumed to match marker)
    in both positive and negative directions defined by (dr, dc).
    """
    count = 1  # start cell
    # positive direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(board, r, c) and board[r][c] == marker:
        count += 1
        r += dr
        c += dc
    # negative direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(board, r, c) and board[r][c] == marker:
        count += 1
        r -= dr
        c -= dc
    return count


def check_win(board: List[List[str]], r: int, c: int, marker: str) -> bool:
    """
    Check whether placing 'marker' at (r, c) resulted in 4 in a row.
    """
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        if check_direction(board, r, c, dr, dc, marker) >= 4:
            return True
    return False


def check_draw(board: List[List[str]]) -> bool:
    # Draw if no spaces left in top row (or anywhere)
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Initialize game
    board = create_board(ROWS, COLS)
    players = PLAYER_MARKERS[:NUM_PLAYERS]

    # Randomly choose starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_marker = players[current_player_idx]
        # Ask for input until valid letter; if column full, player loses the turn.
        col = get_valid_input(COLS, current_marker)

        # Attempt to place
        placed_pos = place_checker(board, col, current_marker)

        if placed_pos is None:
            # Column full: player loses this turn
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_marker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        r, c = placed_pos

        # After a valid move, clear and show updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, r, c, current_marker):
            print(f"Player {current_marker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
