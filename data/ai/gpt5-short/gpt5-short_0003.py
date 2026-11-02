import os
import random
from typing import List, Optional, Tuple

# =========================
# Configurable constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must have length == COLS
TOKENS = ["X", "O", "V", "H", "M"]  # Up to 5 players
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# =========================
# Utility functions
# =========================
def clear_screen() -> None:
    os.system('clear')

def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]) -> None:
    # Header with column labels
    print("   " + " ".join(COLUMN_LABELS))
    # Board rows
    for r in range(ROWS):
        row_cells = [board[r][c] for c in range(COLS)]
        print(f"{ROWS - r:2d} " + " ".join(row_cells))
    # Footer line
    print("   " + " ".join("-" for _ in range(COLS)))

def col_from_label(label: str) -> Optional[int]:
    if len(label) != 1:
        return None
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def find_open_row(board: List[List[str]], col: int) -> Optional[int]:
    # Return the lowest available row index in the column (bottom-most empty)
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_disc(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    row = find_open_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, token: str) -> int:
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board: List[List[str]], r: int, c: int, token: str) -> bool:
    # Check four directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # include the placed disc
        total += count_in_direction(board, r, c, dr, dc, token)
        total += count_in_direction(board, r, c, -dr, -dc, token)
        if total >= 4:
            return True
    return False

def board_full(board: List[List[str]]) -> bool:
    return all(board[0][c] != " " for c in range(COLS))

def validate_constants() -> None:
    if COLS != len(COLUMN_LABELS):
        raise ValueError("COLS must match length of COLUMN_LABELS.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(TOKENS):
        raise ValueError("Not enough TOKENS provided for NUM_PLAYERS.")

# =========================
# Game loop
# =========================
def main() -> None:
    validate_constants()
    players = TOKENS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    current_player_index = random.randrange(NUM_PLAYERS)
    move_count = 0
    winner: Optional[str] = None

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {' '.join(players)}")
        print(f"Current player: {players[current_player_index]}")

        # Input loop
        while True:
            choice = input(f"Choose a column (A-{COLUMN_LABELS[-1]}), or Q to quit: ").strip().upper()
            if choice == "Q":
                clear_screen()
                print("Game exited by user.")
                return

            col = col_from_label(choice)
            if col is None:
                print(f"Invalid input. Enter a single letter A-{COLUMN_LABELS[-1]}.")
                continue

            row = find_open_row(board, col)
            if row is None:
                print("That column is full. Choose another one.")
                continue
            break

        # Place disc
        token = players[current_player_index]
        placed = drop_disc(board, col, token)
        if placed is None:
            # Should not happen due to validation, but safeguard anyway
            print("Unexpected error: could not place disc. Try again.")
            continue

        r, c = placed
        move_count += 1

        # Check for win
        if is_winning_move(board, r, c, token):
            winner = token
            clear_screen()
            print_board(board)
            print(f"Player {token} wins! Congratulations!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves available.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
