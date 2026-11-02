# Connect 4 (6x7) for 2–5 players
# - Columns labeled A-G
# - Players use tokens from PLAYER_TOKENS (first NUM_PLAYERS used)
# - Random first player
# - Validates input and detects wins/draws
# - Clears screen with os.system('clear')

import os
import random
import sys
from typing import List, Tuple, Optional

# -------------------------
# Configuration constants
# -------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Change to 2..5

# -------------------------
# Utility functions
# -------------------------
def clear_screen():
    os.system('clear')  # As requested; on Windows use 'cls'

def create_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]):
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLS)
    # Print rows from top to bottom
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {ch} ' for ch in row_cells) + '|')
        print('+' + '---+' * COLS)

def col_is_full(board: List[List[str]], col: int) -> bool:
    return board[0][col] != ' '

def drop_token(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    # Place token in lowest empty slot in the column.
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return (r, col)
    return None  # Column full

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, token) -> int:
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board: List[List[str]], last_r: int, last_c: int, token: str) -> bool:
    # Check 4 directions: horizontal, vertical, two diagonals
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        total = 1
        total += count_in_direction(board, last_r, last_c, dr, dc, token)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    return all(board[0][c] != ' ' for c in range(COLS))

def parse_move(inp: str) -> Optional[int]:
    if not inp or len(inp.strip()) == 0:
        return None
    s = inp.strip().upper()
    if len(s) != 1:
        return None
    if s < 'A' or s > chr(ord('A') + COLS - 1):
        return None
    return ord(s) - ord('A')

def prompt_move(player_token: str, board: List[List[str]]) -> int:
    while True:
        raw = input(f"Player {player_token}, choose a column (A-{COLUMN_LABELS[-1]}): ")
        col = parse_move(raw)
        if col is None:
            print(f"Invalid input. Enter a single letter A-{COLUMN_LABELS[-1]}.")
            continue
        if col_is_full(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another.")
            continue
        return col

def validate_config():
    if not (2 <= NUM_PLAYERS <= len(PLAYER_TOKENS) and NUM_PLAYERS <= 5):
        print(f"NUM_PLAYERS must be between 2 and 5 and <= len(PLAYER_TOKENS). Got {NUM_PLAYERS}.")
        sys.exit(1)

# -------------------------
# Game loop
# -------------------------
def main():
    validate_config()
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    board = create_board()

    current_idx = random.randrange(NUM_PLAYERS)  # Random first player

    try:
        while True:
            clear_screen()
            print(f"Connect 4 - {ROWS}x{COLS}")
            print(f"Players: {' '.join(tokens)}  |  Current: {tokens[current_idx]}")
            print_board(board)

            col = prompt_move(tokens[current_idx], board)
            placed = drop_token(board, col, tokens[current_idx])
            if placed is None:
                # Shouldn't happen due to validation, but be safe.
                print("Unexpected error: column full after validation. Try again.")
                input("Press Enter...")
                continue

            r, c = placed
            if is_winning_move(board, r, c, tokens[current_idx]):
                clear_screen()
                print_board(board)
                print(f"Player {tokens[current_idx]} wins! Congratulations!")
                break

            if is_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break

            current_idx = (current_idx + 1) % NUM_PLAYERS

    except (EOFError, KeyboardInterrupt):
        print("\nGame exited.")

if __name__ == "__main__":
    main()
