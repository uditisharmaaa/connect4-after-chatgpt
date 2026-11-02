#!/usr/bin/env python3
"""
Connect 4 (6 rows x 7 columns) for 2–5 players.

Features:
- Columns labeled A-G (case-insensitive input).
- Players represented by tokens: X, O, V, H, M (in that order).
- Number of players is chosen via NUM_PLAYERS constant (2–5).
- Randomly selects the first player.
- Input validation (valid column, not full, allows 'Q' to quit).
- Win detection (horizontal, vertical, both diagonals).
- Draw detection when the board is full.
- Uses os.system('clear') to refresh the screen each turn.

Adjust the NUM_PLAYERS constant below (2–5) before running if desired.
"""

import os
import random
from typing import List, Optional, Tuple

# ----- Configuration constants -----
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must match COLS
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players in this order
NUM_PLAYERS = 2  # Change to any integer 2–5


def clear_screen() -> None:
    # Per assignment requirement
    os.system('clear')


def create_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    # Header with labels
    print("   " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)

    # Rows from top (row 0) to bottom (row ROWS-1)
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            cells.append(board[r][c])
        print(" | " + " | ".join(cells) + " |")
        print(" +" + "---+" * COLS)


def validate_num_players(n: int) -> int:
    if n < 2 or n > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5 inclusive.")
    if n > len(PLAYER_TOKENS):
        raise ValueError("Not enough PLAYER_TOKENS for NUM_PLAYERS.")
    return n


def get_column_index(choice: str) -> Optional[int]:
    if not choice:
        return None
    ch = choice.strip().upper()
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return None


def find_drop_row(board: List[List[str]], col: int) -> Optional[int]:
    # Start from bottom row up to top, find first empty space
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None  # column full


def place_token(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS


def count_in_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, token: str) -> int:
    # Count consecutive tokens starting just beyond the starting cell
    count = 0
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board: List[List[str]], last_move: Tuple[int, int], token: str) -> bool:
    r0, c0 = last_move

    # Directions: horizontal (0,1), vertical (1,0), diag down-right (1,1), diag up-right (-1,1)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # include the last placed token
        total += count_in_direction(board, r0, c0, dr, dc, token)
        total += count_in_direction(board, r0, c0, -dr, -dc, token)
        if total >= 4:
            return True
    return False


def is_board_full(board: List[List[str]]) -> bool:
    # Top row has any space? If none, it's full
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True


def prompt_for_move(player_idx: int, token: str) -> Optional[int]:
    while True:
        choice = input(f"Player {player_idx + 1} ({token}) - Choose column A-G (or Q to quit): ").strip()
        if not choice:
            print("Invalid input. Please enter a column letter A-G.")
            continue
        if choice.lower() == 'q':
            return None
        col = get_column_index(choice)
        if col is None:
            print("Invalid column. Please choose a letter A-G.")
            continue
        return col


def announce_winner(token: str) -> None:
    print(f"\nPlayer with token '{token}' wins! Congratulations!")


def announce_draw() -> None:
    print("\nIt's a draw! The board is full and no more moves can be made.")


def main() -> None:
    try:
        n_players = validate_num_players(NUM_PLAYERS)
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    tokens = PLAYER_TOKENS[:n_players]
    board = create_board()

    current_player_index = random.randrange(n_players)

    while True:
        clear_screen()
        print("CONNECT 4")
        print(f"Players: {', '.join(tokens)}  |  First to connect 4 wins")
        print_board(board)
        print(f"\nCurrent turn: Player {current_player_index + 1} ({tokens[current_player_index]})")

        col_choice = prompt_for_move(current_player_index, tokens[current_player_index])
        if col_choice is None:
            print("\nGame ended by user. Goodbye!")
            break

        drop_pos = place_token(board, col_choice, tokens[current_player_index])
        if drop_pos is None:
            print("That column is full. Press Enter to choose another column.")
            input()
            continue

        # Check for win
        if is_winning_move(board, drop_pos, tokens[current_player_index]):
            clear_screen()
            print("CONNECT 4")
            print_board(board)
            announce_winner(tokens[current_player_index])
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print("CONNECT 4")
            print_board(board)
            announce_draw()
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % n_players


if __name__ == "__main__":
    main()
