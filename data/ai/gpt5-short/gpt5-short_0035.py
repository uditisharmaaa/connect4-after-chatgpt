#!/usr/bin/env python3

import os
import random
from typing import List, Optional, Tuple

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = tuple("ABCDEFG")

# Set the number of active players (2 to 5). Players use these symbols in order.
N_PLAYERS = 2
ALL_PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# =========================
# Validation of config
# =========================
def get_active_players(n: int) -> List[str]:
    if not (2 <= n <= 5):
        print(f"Invalid N_PLAYERS={n}. Defaulting to 2.")
        n = 2
    return ALL_PLAYER_SYMBOLS[:n]

ACTIVE_PLAYERS = get_active_players(N_PLAYERS)

# =========================
# Board utilities
# =========================
def make_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen() -> None:
    # Use 'clear' as requested
    os.system("clear")

def print_board(board: List[List[str]]) -> None:
    # Top labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        row_cells = [board[r][c] for c in range(COLS)]
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * COLS)

def col_from_label(label: str) -> Optional[int]:
    label = label.strip().upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def is_column_full(board: List[List[str]], col: int) -> bool:
    return board[0][col] != " "

def get_valid_columns(board: List[List[str]]) -> List[int]:
    return [c for c in range(COLS) if not is_column_full(board, c)]

def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    # Drop from bottom-most available row
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    return None  # Column full

# =========================
# Win/draw checking
# =========================
DIRECTIONS = [
    (0, 1),   # horizontal right
    (1, 0),   # vertical down
    (1, 1),   # diagonal down-right
    (1, -1),  # diagonal down-left
]

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board: List[List[str]], r: int, c: int, dr: int, dc: int, symbol: str) -> int:
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def is_winning_move(board: List[List[str]], r: int, c: int, symbol: str) -> bool:
    # Check 4-in-a-row in any direction through (r, c)
    for dr, dc in DIRECTIONS:
        # Count both directions, subtract 1 to avoid double-counting (r,c)
        total = (
            count_in_direction(board, r, c, dr, dc, symbol) +
            count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    return all(board[0][c] != " " for c in range(COLS))

# =========================
# Input handling
# =========================
def prompt_for_move(player_symbol: str, board: List[List[str]]) -> int:
    valid_cols = get_valid_columns(board)
    valid_labels = {COLUMN_LABELS[c] for c in valid_cols}
    while True:
        move = input(f"Player {player_symbol}, choose a column ({'/'.join(COLUMN_LABELS)}): ").strip().upper()
        col = col_from_label(move)
        if col is None:
            print("Invalid input. Please enter a letter A-G.")
            continue
        if col not in valid_cols:
            if move in valid_labels:
                # This case won't happen because valid_labels came from valid_cols,
                # but keep structure clear.
                pass
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another.")
            continue
        return col

# =========================
# Game loop
# =========================
def game() -> None:
    board = make_board()
    # Random first player index
    current_index = random.randrange(len(ACTIVE_PLAYERS))

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(ACTIVE_PLAYERS)}")
        print_board(board)

        current_player = ACTIVE_PLAYERS[current_index]
        if not get_valid_columns(board):
            print("It's a draw! No more moves.")
            break

        col = prompt_for_move(current_player, board)
        drop_pos = drop_piece(board, col, current_player)
        # drop_pos should never be None because we validate columns, but be safe
        if drop_pos is None:
            print("Unexpected error: column full after validation. Try again.")
            continue
        r, c = drop_pos

        if is_winning_move(board, r, c, current_player):
            clear_screen()
            print("Connect 4")
            print(f"Players: {' '.join(ACTIVE_PLAYERS)}")
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print("Connect 4")
            print(f"Players: {' '.join(ACTIVE_PLAYERS)}")
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(ACTIVE_PLAYERS)

def main() -> None:
    random.seed()  # Initialize PRNG
    game()

if __name__ == "__main__":
    main()
