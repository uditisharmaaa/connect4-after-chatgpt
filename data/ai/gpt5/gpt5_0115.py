import os
import random
import string
from typing import List, Optional, Tuple

# -----------------------------
# Configuration (constants)
# -----------------------------
ROWS = 6                 # Number of rows (default 6)
COLS = 7                 # Number of columns (default 7, max 26)
NUM_PLAYERS = 2          # Number of players (2-5)
WIN_LEN = 4              # Number of checkers in a row needed to win (always 4)

PLAYER_TOKENS = ["X", "O", "V", "H", "M"]  # Up to 5 players in order

# Basic validations for configuration
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > 26:
    raise ValueError("COLS must be at most 26 to allow column labeling by letters.")
if NUM_PLAYERS > len(PLAYER_TOKENS):
    raise ValueError("Not enough player tokens defined for the number of players.")

ACTIVE_TOKENS = PLAYER_TOKENS[:NUM_PLAYERS]


# -----------------------------
# Utility and game functions
# -----------------------------

def clear_screen() -> None:
    """
    Clear the terminal screen. The assignment specifies using 'clear'.
    """
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """
    Create a board with the given dimensions filled with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """
    Print the board to the terminal in the required format.
    Columns are labeled A, B, C, ...
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)

    # Horizontal separator template
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        # Row content
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)


def get_valid_column_input(cols: int, current_token: str) -> int:
    """
    Prompt the user for a valid column letter and return the corresponding column index.
    Keeps asking until a valid letter (within board range) is entered.
    Does not check if the column is full (that's handled separately to possibly lose the turn).
    """
    valid_letters = string.ascii_uppercase[:cols]
    prompt = f"Player {current_token}, please enter a column: "

    while True:
        user_input = input(prompt)
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue

        entry = user_input.strip().upper()
        if len(entry) != 1 or entry not in valid_letters:
            print(f"Invalid input. Enter a letter between A and {valid_letters[-1]}.")
            continue

        col_index = ord(entry) - ord('A')
        return col_index


def find_row_for_column(board: List[List[str]], col: int) -> Optional[int]:
    """
    Given a column index, find the lowest available row index where a checker can be placed.
    Returns None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    """
    Check if (r, c) is within the bounds of the board.
    """
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board: List[List[str]], start: Tuple[int, int], delta: Tuple[int, int], token: str) -> int:
    """
    Count how many consecutive 'token' cells starting from 'start' (exclusive) in the 'delta' direction.
    """
    r, c = start
    dr, dc = delta
    rows = len(board)
    cols = len(board[0])
    count = 0

    nr, nc = r + dr, c + dc
    while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
        count += 1
        nr += dr
        nc += dc
    return count


def check_win_from(board: List[List[str]], r: int, c: int, token: str, win_len: int = WIN_LEN) -> bool:
    """
    Check if placing 'token' at (r, c) results in a win in any direction.
    We check four directions: horizontal, vertical, diagonal down-right, diagonal up-right.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (-1, 1),  # Diagonal up-right
    ]

    for dr, dc in directions:
        total = 1  # include the placed token
        total += count_in_direction(board, (r, c), (dr, dc), token)
        total += count_in_direction(board, (r, c), (-dr, -dc), token)
        if total >= win_len:
            return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    """
    The game is a draw if the board has no empty spaces.
    A faster check is to see if the top row has any empties; but for clarity, we check all cells.
    """
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current_index: int, total_players: int) -> int:
    """
    Compute the next player's index in a circular manner.
    """
    return (current_index + 1) % total_players


# -----------------------------
# Main game loop
# -----------------------------

def main() -> None:
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)
    current_token = ACTIVE_TOKENS[current_player_idx]

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        # Prompt current player for input (validated column letter)
        col = get_valid_column_input(COLS, current_token)

        # Determine placement row (if any)
        row = find_row_for_column(board, col)

        if row is None:
            # Column is full: turn is invalid and the player loses the turn
            clear_screen()
            print_board(board)
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_token} loses this turn.")
            # Next player's turn
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            current_token = ACTIVE_TOKENS[current_player_idx]
            continue

        # Place the checker
        board[row][col] = current_token

        # Clear and show updated board
        clear_screen()
        print_board(board)

        # Check for a win
        if check_win_from(board, row, col, current_token, WIN_LEN):
            print(f"Player {current_token} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
        current_token = ACTIVE_TOKENS[current_player_idx]

    # Game over


if __name__ == "__main__":
    main()
