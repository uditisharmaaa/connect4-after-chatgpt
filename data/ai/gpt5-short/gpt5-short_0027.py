#!/usr/bin/env python3
import os
import random
from typing import List, Optional

# ====== Configuration ======
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Player symbols in turn order. The game will use the first NUM_PLAYERS of these.
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Set how many players are playing (must be between 2 and 5).
NUM_PLAYERS = 2
# ===========================


Board = List[List[str]]


def clear_screen() -> None:
    # Requirement specifies using 'clear'
    os.system("clear")


def create_board(rows: int, cols: int) -> Board:
    return [["." for _ in range(cols)] for _ in range(rows)]


def print_board(board: Board) -> None:
    # Column headers
    print("  " + " ".join(COLUMN_LABELS[:NUM_COLS]))
    # Rows top to bottom
    for r in range(NUM_ROWS):
        print("| " + " ".join(board[r]) + " |")
    print("-" * (NUM_COLS * 2 + 3))


def parse_move(user_input: str) -> Optional[int]:
    s = user_input.strip().upper()
    if len(s) != 1:
        return None
    if s not in COLUMN_LABELS[:NUM_COLS]:
        return None
    return COLUMN_LABELS.index(s)


def column_is_full(board: Board, col: int) -> bool:
    # If top cell is not empty, the column is full
    return board[0][col] != "."


def drop_piece(board: Board, col: int, symbol: str) -> bool:
    if column_is_full(board, col):
        return False
    # Place from bottom up
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == ".":
            board[r][col] = symbol
            return True
    return False  # Should not happen due to earlier check


def check_win(board: Board, symbol: str) -> bool:
    # Horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if (
                board[r][c] == symbol
                and board[r][c + 1] == symbol
                and board[r][c + 2] == symbol
                and board[r][c + 3] == symbol
            ):
                return True

    # Vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if (
                board[r][c] == symbol
                and board[r + 1][c] == symbol
                and board[r + 2][c] == symbol
                and board[r + 3][c] == symbol
            ):
                return True

    # Diagonal down-right
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if (
                board[r][c] == symbol
                and board[r + 1][c + 1] == symbol
                and board[r + 2][c + 2] == symbol
                and board[r + 3][c + 3] == symbol
            ):
                return True

    # Diagonal up-right
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if (
                board[r][c] == symbol
                and board[r - 1][c + 1] == symbol
                and board[r - 2][c + 2] == symbol
                and board[r - 3][c + 3] == symbol
            ):
                return True

    return False


def check_draw(board: Board) -> bool:
    # Draw if no empty cells remain in top row (means all columns are full)
    return all(cell != "." for cell in board[0])


def get_active_players() -> List[str]:
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough PLAYER_SYMBOLS for NUM_PLAYERS.")
    return PLAYER_SYMBOLS[:NUM_PLAYERS]


def prompt_for_move(current_symbol: str, board: Board) -> int:
    while True:
        move = input(f"Player {current_symbol}, choose a column ({COLUMN_LABELS[:NUM_COLS]}): ")
        col = parse_move(move)
        if col is None:
            print(f"Invalid input. Enter a single letter from {COLUMN_LABELS[:NUM_COLS]}.")
            continue
        if column_is_full(board, col):
            print("That column is full. Choose a different one.")
            continue
        return col


def main() -> None:
    active_players = get_active_players()
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly pick the index of the first player
    current_index = random.randint(0, len(active_players) - 1)

    while True:
        clear_screen()
        print_board(board)

        current_symbol = active_players[current_index]
        col = prompt_for_move(current_symbol, board)
        drop_piece(board, col, current_symbol)

        # Check for win/draw
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(active_players)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
