#!/usr/bin/env python3
import os
import random
from typing import List, Tuple, Optional

# -------------------- Configuration --------------------
ROWS = 6
COLS = 7
COL_LABELS = tuple("ABCDEFG")

# Choose 2–5 players. Only the first NUM_PLAYERS tokens are used.
PLAYER_TOKENS = ("X", "O", "V", "H", "M")
NUM_PLAYERS = 2  # change to 3, 4, or 5 for more players

# -------------------- Board Utilities --------------------
def make_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen() -> None:
    # Per requirement: use 'clear'
    try:
        os.system("clear")
    except Exception:
        pass  # Best effort; ignore if not available

def print_board(board: List[List[str]]) -> None:
    # Header
    print("  " + " ".join(COL_LABELS))
    # Rows
    for r in range(ROWS):
        row_cells = [board[r][c] for c in range(COLS)]
        print("| " + " ".join(row_cells))
    print()  # trailing newline

def col_from_label(label: str) -> Optional[int]:
    label = label.strip().upper()
    if len(label) != 1 or label not in COL_LABELS:
        return None
    return ord(label) - ord('A')

def next_open_row(board: List[List[str]], col: int) -> Optional[int]:
    # Return the lowest (largest r) open row index in a column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_token(board: List[List[str]], col: int, token: str) -> Tuple[int, int]:
    r = next_open_row(board, col)
    if r is None:
        raise ValueError("Column is full")
    board[r][col] = token
    return r, col

# -------------------- Win / Draw Checking --------------------
def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_direction(board: List[List[str]], r: int, c: int, dr: int, dc: int, token: str) -> int:
    # Count consecutive tokens starting just beyond (r, c) in direction (dr, dc)
    count = 0
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr += dr
        cc += dc
    return count

def is_winning_move(board: List[List[str]], r: int, c: int) -> bool:
    token = board[r][c]
    if token == " ":
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        # Count both directions from the last placed token
        total = 1
        total += count_direction(board, r, c, dr, dc, token)
        total += count_direction(board, r, c, -dr, -dc, token)
        if total >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    # Draw if top row has no spaces (board full)
    return all(cell != " " for cell in board[0])

# -------------------- Input Handling --------------------
def get_player_move(board: List[List[str]], token: str) -> int:
    while True:
        choice = input(f"Player {token}, choose a column ({COL_LABELS[0]}-{COL_LABELS[-1]}): ").strip().upper()
        col = col_from_label(choice)
        if col is None:
            print(f"Invalid input. Enter a single letter from {COL_LABELS[0]} to {COL_LABELS[-1]}.")
            continue
        if next_open_row(board, col) is None:
            print("That column is full. Try another.")
            continue
        return col

# -------------------- Game Loop --------------------
def main() -> None:
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
    active_tokens = PLAYER_TOKENS[:NUM_PLAYERS]

    board = make_board()
    current_index = random.randrange(NUM_PLAYERS)  # random first player

    while True:
        clear_screen()
        print_board(board)

        token = active_tokens[current_index]
        col = get_player_move(board, token)
        r, c = drop_token(board, col, token)

        if is_winning_move(board, r, c):
            clear_screen()
            print_board(board)
            print(f"Player {token} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
