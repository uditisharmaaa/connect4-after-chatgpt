#!/usr/bin/env python3
import os
import random
from typing import List, Optional, Tuple

# ====== Configuration Constants ======
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must match COLS length
PLAYER_TOKENS = ("X", "O", "V", "H", "M")  # Up to 5 players
NUM_PLAYERS = 2  # Set to 2..5 for the number of players in this game
# ====================================


def clear_screen() -> None:
    os.system("clear")


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    # Column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Rows from top to bottom
    for r in range(len(board)):
        print("| " + " ".join(board[r]) + " ")
    print("-" * (2 + 2 * len(board[0]) - 1))


def find_drop_row(board: List[List[str]], col: int) -> Optional[int]:
    # Return the row index where the token will land in this column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_token(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, token: str) -> int:
    rows, cols = len(board), len(board[0])
    r, c = start_r, start_c
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board: List[List[str]], last_r: int, last_c: int, token: str) -> bool:
    # Check 4-in-a-row in all directions from the last placed token
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        # Count both directions from the last move, subtract 1 to avoid double-counting the center
        total = (
            count_in_direction(board, last_r, last_c, dr, dc, token)
            + count_in_direction(board, last_r, last_c, -dr, -dc, token)
            - 1
        )
        if total >= 4:
            return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    # Draw if top row has no spaces
    return all(cell != " " for cell in board[0])


def parse_column_input(s: str) -> Optional[int]:
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(s)


def get_player_move(board: List[List[str]], token: str) -> int:
    cols = len(board[0])
    while True:
        raw = input(f"Player {token}, choose a column ({COLUMN_LABELS}): ")
        col = parse_column_input(raw)
        if col is None:
            print(f"Invalid input. Enter one letter from {COLUMN_LABELS}.")
            continue
        if find_drop_row(board, col) is None:
            print("That column is full. Choose another.")
            continue
        return col


def validate_config() -> Tuple[int, Tuple[str, ...]]:
    if COLS != len(COLUMN_LABELS):
        raise ValueError("COLS must match length of COLUMN_LABELS.")
    if not (2 <= NUM_PLAYERS <= len(PLAYER_TOKENS)):
        raise ValueError(f"NUM_PLAYERS must be between 2 and {len(PLAYER_TOKENS)}.")
    active_tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    return NUM_PLAYERS, active_tokens


def main() -> None:
    num_players, active_tokens = validate_config()
    board = create_board(ROWS, COLS)

    current_idx = random.randrange(num_players)
    clear_screen()
    print("Welcome to Connect Four!")
    print(f"Players: {' '.join(active_tokens)}")
    print(f"Randomly selected first player: {active_tokens[current_idx]}")
    print_board(board)

    while True:
        token = active_tokens[current_idx]
        col = get_player_move(board, token)
        move = drop_token(board, col, token)
        # move cannot be None because we validated, but be safe:
        if move is None:
            print("Unexpected error: column is full after validation.")
            continue

        last_r, last_c = move

        clear_screen()
        print_board(board)

        if check_win(board, last_r, last_c, token):
            print(f"Player {token} wins!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % num_players


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("Game interrupted.")
