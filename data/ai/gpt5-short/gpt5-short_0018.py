import os
import random
import string
from typing import List, Optional, Tuple

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = list("ABCDEFG")  # Must be length COLS
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5 for intro class assignment

# =========================
# Utility functions
# =========================

def clear_screen() -> None:
    """
    Clear the terminal screen.
    The assignment requires os.system('clear'), which works on Unix-like systems.
    """
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """
    Create an empty Connect 4 board represented as a 2D list of strings.
    Empty cells are represented by a single dot '.'.
    """
    return [["." for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """
    Print the board to the terminal with column labels at the top
    and each row of the board below. The bottom of the board is the last row.
    """
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Print each row
    for row in board:
        print("  " + " ".join(row))


def next_open_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Return the index of the lowest empty row in the given column,
    or None if the column is full.
    The bottom row has index ROWS - 1.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ".":
            return r
    return None


def apply_move(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Place the player's symbol into the given column at the next available row.
    Returns the (row, col) of the placed piece, or None if the column is full.
    """
    r = next_open_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return (r, col)


def in_bounds(r: int, c: int) -> bool:
    """Check if (r, c) is within the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def count_in_direction(board: List[List[str]], r: int, c: int, dr: int, dc: int, symbol: str) -> int:
    """
    Count consecutive symbols starting from (r, c) and moving step (dr, dc).
    Includes the starting cell in the count if it matches the symbol.
    """
    count = 0
    cr, cc = r, c
    while in_bounds(cr, cc) and board[cr][cc] == symbol:
        count += 1
        cr += dr
        cc += dc
    return count


def check_win(board: List[List[str]], r: int, c: int, symbol: str) -> bool:
    """
    Check if placing symbol at (r, c) causes a win (4 in a row).
    We check in four lines: horizontal, vertical, and two diagonals.
    For each line, count in both directions and subtract 1 to avoid double-counting (r, c).
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = (
            count_in_direction(board, r, c, dr, dc, symbol) +
            count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    """
    The game is a draw if the top row of every column is filled (i.e., no '.').
    """
    return all(board[0][c] != "." for c in range(COLS))


def get_column_input(player_symbol: str) -> Optional[int]:
    """
    Prompt the user to pick a column (A-G). Returns the column index (0-based),
    or None if the user enters 'Q' to quit. Validates input.
    """
    prompt = f"Player {player_symbol}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}) or Q to quit: "
    while True:
        choice = input(prompt).strip().upper()
        if choice == "Q":
            return None
        if len(choice) == 1 and choice in COLUMN_LABELS:
            col_idx = COLUMN_LABELS.index(choice)
            return col_idx
        print(f"Invalid input. Please enter a single letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}, or Q to quit.")


def validate_settings() -> List[str]:
    """
    Validate NUM_PLAYERS and COLUMN_LABELS against COLS.
    Returns the list of active player symbols to use in the game.
    """
    if COLS != len(COLUMN_LABELS):
        raise ValueError("COLS must match the length of COLUMN_LABELS.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough PLAYER_SYMBOLS for the number of players.")
    # Use the first NUM_PLAYERS symbols
    return PLAYER_SYMBOLS[:NUM_PLAYERS]


def play_game() -> None:
    """
    Main game loop:
    - Initialize settings and board
    - Pick a random starting player
    - Loop turns until win or draw
    - Clear screen and print the board before each move
    """
    active_players = validate_settings()
    board = create_board(ROWS, COLS)

    # Randomize starting player
    current_index = random.randrange(len(active_players))

    # Game loop
    while True:
        clear_screen()
        print_board(board)
        current_player_symbol = active_players[current_index]
        print(f"\nIt's Player {current_player_symbol}'s turn.")

        # Get a valid column input or quit
        col = get_column_input(current_player_symbol)
        if col is None:
            print("\nGame ended by user. Goodbye!")
            return

        # Attempt to apply the move
        pos = apply_move(board, col, current_player_symbol)
        if pos is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Press Enter to choose again.")
            input()
            continue

        r, c = pos

        # Check for win or draw
        if check_win(board, r, c, current_player_symbol):
            clear_screen()
            print_board(board)
            print(f"\nPlayer {current_player_symbol} wins! Congratulations!")
            return

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("\nIt's a draw! The board is full.")
            return

        # Advance to next player
        current_index = (current_index + 1) % len(active_players)


if __name__ == "__main__":
    # Seed the random number generator (optional: for variety each run)
    random.seed()

    # Start the game
    play_game()
