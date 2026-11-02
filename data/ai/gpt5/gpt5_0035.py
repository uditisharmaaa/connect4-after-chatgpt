import os
import random
import string
import sys
from typing import List, Optional, Tuple

# ----------------------------
# Configuration (adjustable)
# ----------------------------
ROWS = 6                 # default submission setting
COLS = 7                 # default submission setting (max 26)
NUM_PLAYERS = 2          # default submission setting (between 2 and 5)
WIN_LENGTH = 4           # number in a row needed to win (fixed at 4)
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]  # up to 5 players

# Safety checks for configuration
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > 26:
    raise ValueError("COLS must be <= 26 (for column labels A-Z).")
if NUM_PLAYERS > len(PLAYER_TOKENS):
    raise ValueError("Not enough tokens defined for the number of players.")


# ----------------------------
# Utility functions
# ----------------------------
def clear_screen() -> None:
    # For Unix/Linux terminals
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    # Board indexed as board[row][col], row 0 is top, row rows-1 is bottom
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    # Labels A, B, C, ...
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    labels = column_labels(len(board[0]))
    # Header
    header = "  " + "   ".join(labels)
    print(header)
    # Separator
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    # Rows
    for r in range(len(board)):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(len(labels))) + "|"
        print(row_cells)
    print(sep)


def is_valid_column_label(label: str, cols: int) -> bool:
    return len(label) == 1 and label in string.ascii_uppercase[:cols]


def col_index_from_label(label: str) -> int:
    return ord(label) - ord('A')


def find_row_for_col(board: List[List[str]], col: int) -> Optional[int]:
    # Return the lowest available row index in the given column; None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    row = find_row_for_col(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)


def in_bounds(rows: int, cols: int, r: int, c: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board: List[List[str]], start: Tuple[int, int], dr: int, dc: int, token: str) -> int:
    rows, cols = len(board), len(board[0])
    r, c = start
    count = 0
    while in_bounds(rows, cols, r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win_from(board: List[List[str]], pos: Tuple[int, int]) -> bool:
    r, c = pos
    token = board[r][c]
    if token == " ":
        return False
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horiz, vert, diag down-right, diag down-left
    for dr, dc in directions:
        # Count both directions from the last placed position, subtract 1 to avoid double-counting the origin
        total = (
            count_in_direction(board, (r, c), dr, dc, token) +
            count_in_direction(board, (r, c), -dr, -dc, token) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def board_full(board: List[List[str]]) -> bool:
    return all(cell != " " for row in board for cell in row)


def prompt_column(current_token: str, cols: int) -> str:
    labels = column_labels(cols)
    prompt = f"Player {current_token}, please enter a column ({labels[0]}-{labels[-1]}): "
    while True:
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        # Accept case-insensitive, but require it to be a single letter within range
        if len(raw) == 1 and raw.isalpha():
            ch = raw.upper()
            if is_valid_column_label(ch, cols):
                return ch
        print("Invalid input. Please enter a single letter within the valid column range.")


# ----------------------------
# Game loop
# ----------------------------
def main() -> None:
    board = create_board(ROWS, COLS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    winner: Optional[str] = None

    while True:
        current_token = players[current_player_idx]

        # Prompt for a column letter (validated for range/character)
        col_label = prompt_column(current_token, COLS)
        col = col_index_from_label(col_label)

        # Attempt to place checker
        placed_pos = drop_checker(board, col, current_token)
        if placed_pos is None:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {col_label} is full. Turn lost.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Show board again after turn (even if no move)
            input("Press Enter to continue...")
            clear_screen()
            print_board(board)
            continue

        # Clear and print updated board after a successful move
        clear_screen()
        print_board(board)

        # Check win condition only if a piece was placed
        if check_win_from(board, placed_pos):
            winner = current_token
            break

        # Check draw
        if board_full(board):
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game over message
    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw.")


if __name__ == "__main__":
    main()
