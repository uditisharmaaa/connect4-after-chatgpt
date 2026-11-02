#!/usr/bin/env python3
"""
Connect 4 (Console Version)

- Board: 6 rows x 7 columns
- Columns labeled A-G
- 2 to 5 players (symbols: X, O, V, H, M) configured via constants
- Random first player
- Robust input validation
- Win and draw detection
- Clears the screen using os.system('clear')

Author: Your Name
"""

import os
import random
from typing import List, Optional, Tuple

# ======= Configuration Constants =======
ROWS: int = 6
COLS: int = 7
COL_LABELS: List[str] = [chr(ord('A') + i) for i in range(COLS)]

# Up to 5 player symbols in fixed order (do not change order, just choose how many via NUM_PLAYERS)
PLAYER_SYMBOLS: List[str] = ['X', 'O', 'V', 'H', 'M']

# Number of players for the game (integer 2..5). The game uses the first NUM_PLAYERS from PLAYER_SYMBOLS.
NUM_PLAYERS: int = 2

# How many in a row to win
CONNECT_N: int = 4

# Allow 'Q' to quit mid-game (recommended for usability)
ALLOW_QUIT: bool = True


# ======= Utility Functions =======

def clear_screen() -> None:
    """
    Clear the console screen.
    Requirement specifies using os.system('clear').
    Also try 'cls' as a fallback for Windows, but always attempt 'clear' first.
    """
    # Primary requirement:
    ret = os.system('clear')
    if ret != 0:
        # Fallback for Windows if 'clear' is not available
        os.system('cls')


def create_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    """Create an empty board filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """Print the current board with column labels."""
    clear_screen()
    print("Connect 4")
    print("Players:", ' '.join(PLAYER_SYMBOLS[:NUM_PLAYERS]))
    print()
    # Column labels
    print('  ' + '   '.join(COL_LABELS))
    print(' +' + '---+' * COLS)
    # Rows
    for r in range(ROWS):
        row_cells = [board[r][c] for c in range(COLS)]
        print(' | ' + ' | '.join(row_cells) + ' |')
        print(' +' + '---+' * COLS)


def get_valid_columns(board: List[List[str]]) -> List[int]:
    """
    Return a list of column indices that are not full.
    A column is valid if the top cell is empty.
    """
    return [c for c in range(COLS) if board[0][c] == '']


def is_column_full(board: List[List[str]], col: int) -> bool:
    """Check if a column is full (no spaces)."""
    return board[0][col] != ' '


def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Drop a piece into the given column for the player symbol.
    Returns the (row, col) position where the piece lands, or None if the column is full.
    """
    if is_column_full(board, col):
        return None
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None


def in_bounds(r: int, c: int) -> bool:
    """Check if a position is within the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def check_winner(board: List[List[str]], symbol: str, last_pos: Tuple[int, int]) -> bool:
    """
    Check if placing 'symbol' at last_pos created a CONNECT_N in a row in any direction.
    Optimized to start from the last placed piece.
    """
    if last_pos is None:
        return False
    r0, c0 = last_pos

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the last placed piece

        # Extend in positive direction
        r, c = r0 + dr, c0 + dc
        while in_bounds(r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Extend in negative direction
        r, c = r0 - dr, c0 - dc
        while in_bounds(r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= CONNECT_N:
            return True

    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if the board is full (draw)."""
    return all(board[0][c] != ' ' for c in range(COLS))


def label_to_col(label: str) -> Optional[int]:
    """
    Convert a single-letter column label (A-G) to a column index.
    Returns None if invalid.
    """
    label = label.strip().upper()
    if len(label) != 1:
        return None
    if label in COL_LABELS:
        return COL_LABELS.index(label)
    return None


def prompt_move(current_symbol: str, board: List[List[str]]) -> Optional[int]:
    """
    Prompt the current player for a move and validate it.
    Returns a valid column index or None if the user chose to quit.
    """
    while True:
        choice = input(f"Player {current_symbol}, choose a column (A-G){' or Q to quit' if ALLOW_QUIT else ''}: ").strip().upper()
        if ALLOW_QUIT and choice == 'Q':
            return None

        col = label_to_col(choice)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            continue

        if is_column_full(board, col):
            print(f"Column {COL_LABELS[col]} is full. Choose another column.")
            continue

        return col


def validate_configuration() -> None:
    """Validate configuration constants and provide safe defaults with messages if needed."""
    global NUM_PLAYERS
    if not isinstance(NUM_PLAYERS, int) or NUM_PLAYERS < 2 or NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print(f"NUM_PLAYERS must be an integer between 2 and {len(PLAYER_SYMBOLS)}. Defaulting to 2.")
        NUM_PLAYERS = 2


def next_player_index(current: int, total: int) -> int:
    """Return the next player's index in cyclic order."""
    return (current + 1) % total


# ======= Main Game Loop =======

def play_game() -> None:
    """Run a single game of Connect 4."""
    validate_configuration()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()

    # Random starting player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    winner: Optional[str] = None

    while True:
        print_board(board)
        print(f"Turn: Player {players[current_idx]}")

        col = prompt_move(players[current_idx], board)
        if col is None:
            print("Game aborted by user. Goodbye!")
            return

        pos = drop_piece(board, col, players[current_idx])
        if pos is None:
            # Shouldn't happen due to validation, but safe-guard
            print("Unexpected error: Could not place piece. Try again.")
            continue

        # Check for winner
        if check_winner(board, players[current_idx], pos):
            winner = players[current_idx]
            print_board(board)
            print(f"Player {winner} wins! Congratulations!")
            break

        # Check for draw
        if board_full(board):
            print_board(board)
            print("It's a draw! Board is full.")
            break

        # Next player's turn
        current_idx = next_player_index(current_idx, NUM_PLAYERS)

    # Post-game: prompt to play again
    while True:
        again = input("Play again? (Y/N): ").strip().upper()
        if again == 'Y':
            play_game()
            return
        elif again == 'N':
            print("Thanks for playing!")
            return
        else:
            print("Please enter Y or N.")


if __name__ == "__main__":
    # Ensure board uses consistent internal representation (spaces for empty)
    # Normalize any accidental creation differences (already handled in create_board).
    random.seed()  # Use system time or OS entropy
    play_game()
