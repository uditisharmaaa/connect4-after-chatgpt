# Connect 4 (6x7) for Intro CS
# - Columns labeled A-G
# - Supports 2 to 5 players with symbols: X, O, V, H, M
# - Random first player
# - Validates input
# - Checks wins and draws
# - Clears screen with os.system('clear')

import os
import random
from typing import List, Optional, Tuple

# ---------- Configuration ----------
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Choose how many players (2 to 5)
NUM_PLAYERS = 2

# Symbols will be taken in order from this list (first NUM_PLAYERS are used)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

EMPTY = "."

# ---------- Helpers ----------

def clear_screen() -> None:
    # As requested, use 'clear'
    os.system('clear')

def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]) -> None:
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS[:len(board[0])]))
    # Print rows (top row first)
    for r in range(len(board)):
        print(f"{len(board)-r} " + " ".join(board[r]))
    print()

def col_from_label(label: str) -> Optional[int]:
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def is_valid_column(board: List[List[str]], col: int) -> bool:
    return 0 <= col < len(board[0]) and board[0][col] == EMPTY

def get_next_open_row(board: List[List[str]], col: int) -> Optional[int]:
    # Find the lowest empty row in this column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def drop_piece(board: List[List[str]], row: int, col: int, symbol: str) -> None:
    board[row][col] = symbol

def board_full(board: List[List[str]]) -> bool:
    return all(cell != EMPTY for cell in board[0])

def winning_move(board: List[List[str]], symbol: str) -> bool:
    rows, cols = len(board), len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r][c+1] == symbol and
                board[r][c+2] == symbol and board[r][c+3] == symbol):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == symbol and board[r+1][c] == symbol and
                board[r+2][c] == symbol and board[r+3][c] == symbol):
                return True

    # Diagonal down-right (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r+1][c+1] == symbol and
                board[r+2][c+2] == symbol and board[r+3][c+3] == symbol):
                return True

    # Diagonal up-right (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and board[r-1][c+1] == symbol and
                board[r-2][c+2] == symbol and board[r-3][c+3] == symbol):
                return True

    return False

def prompt_move(current_symbol: str) -> str:
    return input(f"Player {current_symbol}, choose a column (A-{COLUMN_LABELS[COLS-1]}): ").strip()

# ---------- Game Loop ----------

def main() -> None:
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough PLAYER_SYMBOLS for NUM_PLAYERS.")
    if COLS != 7 or ROWS != 6 or COLUMN_LABELS[:COLS] != "ABCDEFG":
        raise ValueError("This game is fixed to 6 rows and 7 columns labeled A-G as requested.")

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomize starting player
    current_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print("Connect 4 — 6x7")
        print(f"Players: {' '.join(players)}  |  Current: {players[current_idx]}")
        print_board(board)

        move = prompt_move(players[current_idx])
        col = col_from_label(move) if len(move) == 1 else None

        if col is None:
            print(f"Invalid input. Please enter a single letter A-{COLUMN_LABELS[COLS-1]}.")
            input("Press Enter to continue...")
            continue

        if not is_valid_column(board, col):
            print("That column is full or invalid. Try another.")
            input("Press Enter to continue...")
            continue

        row = get_next_open_row(board, col)
        if row is None:
            print("That column is full. Try another.")
            input("Press Enter to continue...")
            continue

        drop_piece(board, row, col, players[current_idx])

        # Check win
        if winning_move(board, players[current_idx]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_idx]} wins! Congratulations!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! Board is full.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

    print("Game over.")

if __name__ == "__main__":
    main()
