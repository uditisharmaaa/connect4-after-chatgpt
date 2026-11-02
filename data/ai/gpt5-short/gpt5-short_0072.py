#!/usr/bin/env python3
import os
import random
import string
from typing import List, Optional, Tuple

# Configuration constants
ROWS = 6
COLS = 7
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A', 'B', ..., 'G']

# Define up to 5 player symbols. Use the first N_PLAYERS of these.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Set number of players here (2 to 5)
N_PLAYERS = 2  # Change to 3, 4, or 5 if desired.

# Clear command (Linux/macOS per requirement)
def clear_screen():
    os.system('clear')

def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]) -> None:
    # Header with column labels
    print('  ' + '   '.join(COL_LABELS))
    print('+' + '---+' * COLS)
    # Board rows
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {ch}' for ch in row_cells) + '|')
        print('+' + '---+' * COLS)

def column_index_from_input(s: str) -> Optional[int]:
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COL_LABELS:
        return COL_LABELS.index(s)
    return None

def is_column_full(board: List[List[str]], col: int) -> bool:
    return board[0][col] != ' '

def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    # Drop into the lowest available slot in the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board: List[List[str]], r: int, c: int, symbol: str) -> bool:
    # Check 4 in a row including position (r, c)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        count = 1
        # Extend in positive direction
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        # Extend in negative direction
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def board_full(board: List[List[str]]) -> bool:
    return all(board[0][c] != ' ' for c in range(COLS))

def prompt_for_move(player_symbol: str, board: List[List[str]]) -> int:
    while True:
        entry = input(f"Player {player_symbol}, choose a column ({'/'.join(COL_LABELS)}): ")
        col = column_index_from_input(entry)
        if col is None:
            print("Invalid input. Please enter a single letter between A and G.")
            continue
        if is_column_full(board, col):
            print(f"Column {COL_LABELS[col]} is full. Choose another column.")
            continue
        return col

def main():
    # Validate number of players
    if not (2 <= N_PLAYERS <= 5):
        print("Error: N_PLAYERS must be between 2 and 5.")
        return
    symbols = PLAYER_SYMBOLS[:N_PLAYERS]
    board = create_board(ROWS, COLS)

    # Choose random first player
    current_idx = random.randrange(N_PLAYERS)

    # Game loop
    while True:
        clear_screen()
        print_board(board)
        current_symbol = symbols[current_idx]
        col = prompt_for_move(current_symbol, board)
        pos = drop_piece(board, col, current_symbol)
        # pos should not be None since we validated, but guard anyway
        if pos is None:
            print("Unexpected error: could not drop piece. Try again.")
            input("Press Enter to continue...")
            continue
        r, c = pos

        # Check for win
        if check_win(board, r, c, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % N_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
