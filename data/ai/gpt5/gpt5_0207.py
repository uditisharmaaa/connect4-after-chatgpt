import os
import random
import string
from typing import List, Tuple, Optional

# =========================
# Configuration constants
# =========================
ROWS = 6             # number of rows (default 6)
COLS = 7             # number of columns (default 7, max 26)
NUM_PLAYERS = 2      # number of players (2 to 5)

# Player checkers in order. Will slice to NUM_PLAYERS.
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Sanity checks for constraints
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert 1 <= ROWS and 1 <= COLS <= 26, "Board must have at least 1 row, and 1-26 columns."
assert len(CHECKERS) == NUM_PLAYERS, "Number of checkers must equal number of players."


Board = List[List[str]]  # alias for readability


def clear_screen() -> None:
    # Per assignment spec: clear screen using Unix 'clear'
    os.system('clear')


def create_board(rows: int, cols: int) -> Board:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: Board) -> None:
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters (A..)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def column_from_input(inp: str, cols: int) -> Optional[int]:
    """
    Convert a user input (single letter) to a column index, if valid.
    Returns None if invalid.
    """
    if not inp or len(inp.strip()) != 1:
        return None
    ch = inp.strip().upper()
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return None
    return ord(ch) - ord('A')


def lowest_empty_row(board: Board, col: int) -> Optional[int]:
    """
    Return the lowest empty row index for the given column,
    or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board: Board, col: int, checker: str) -> Optional[Tuple[int, int]]:
    """
    Place the checker in the given column at the lowest empty row.
    Returns (row, col) if placed, or None if the column is full.
    """
    r = lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return (r, col)


def in_bounds(rows: int, cols: int, r: int, c: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board: Board, start_r: int, start_c: int, dr: int, dc: int, checker: str) -> int:
    """
    Count consecutive checkers starting from (start_r, start_c) moving in (dr, dc).
    Includes the starting cell if it matches.
    """
    rows, cols = len(board), len(board[0])
    r, c = start_r, start_c
    count = 0
    while in_bounds(rows, cols, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def is_win(board: Board, last_move: Tuple[int, int], checker: str) -> bool:
    """
    Check if placing 'checker' at last_move (row, col) caused a win.
    """
    r, c = last_move

    # Directions: horizontal (0,1), vertical (1,0), diag down-right (1,1), diag up-right (-1,1)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for dr, dc in directions:
        # Count both directions, subtract 1 to avoid double-counting starting cell
        total = (
            count_in_direction(board, r, c, dr, dc, checker) +
            count_in_direction(board, r, c, -dr, -dc, checker) - 1
        )
        if total >= 4:
            return True
    return False


def is_draw(board: Board) -> bool:
    """
    A draw occurs when there are no empty spaces left.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def next_player_index(current: int, total_players: int) -> int:
    return (current + 1) % total_players


def prompt_for_column(current_checker: str, cols: int) -> int:
    """
    Prompt until a valid column letter is entered.
    Returns the valid column index (0-based).
    """
    while True:
        user_inp = input(f"Player {current_checker}, please enter a column: ").strip()
        col = column_from_input(user_inp, cols)
        if col is not None:
            return col
        print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + cols - 1)}.")


def game_loop() -> None:
    board = create_board(ROWS, COLS)
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display before the game starts
    print_board(board)

    winner: Optional[str] = None

    while True:
        current_checker = CHECKERS[current_player]

        # Show current board before the move and prompt
        # (print_board was already called at the end of last turn or at start)
        col = prompt_for_column(current_checker, COLS)

        # Attempt to place the checker
        placement = place_checker(board, col, current_checker)
        if placement is None:
            # Column full: player loses the turn
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses this turn.")
            # Move to next player
            current_player = next_player_index(current_player, NUM_PLAYERS)
            # Show board again for next player
            continue

        # After placing, print updated board
        print_board(board)

        # Check for win
        if is_win(board, placement, current_checker):
            winner = current_checker
            break

        # Check for draw
        if is_draw(board):
            break

        # Next player's turn
        current_player = next_player_index(current_player, NUM_PLAYERS)

    # Final state already printed; announce result
    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw.")


if __name__ == "__main__":
    try:
        game_loop()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        clear_screen()
        print("Game interrupted. Goodbye!")
