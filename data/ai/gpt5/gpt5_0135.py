import os
import random
import sys
from typing import List, Tuple

# ===========================
# Configuration (constants)
# ===========================
# Board dimensions (ROWS x COLS). Submission requires 6 x 7.
ROWS = 6
COLS = 7  # Must be <= 26 due to column labels A-Z
# Number of players (between 2 and 5). Submission requires 2.
NUM_PLAYERS = 2

# Checker symbols in order for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# Win condition (number in a row to win)
WIN_LENGTH = 4

# ===========================
# Validation of configuration
# ===========================
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS > 26 or COLS < 1 or ROWS < 1:
    print("Invalid board dimensions. COLS must be between 1 and 26, ROWS must be >= 1.")
    sys.exit(1)

# Slice the checkers to the chosen number of players
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]


# ===========================
# Board utilities
# ===========================
def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen() -> None:
    # Linux/Unix terminals
    os.system('clear')


def column_label(col_idx: int) -> str:
    # 0 -> 'A', 1 -> 'B', ...
    return chr(ord('A') + col_idx)


def print_board(board: List[List[str]]) -> None:
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header = "  " + "   ".join(column_label(c) for c in range(cols))
    print(header)
    print("+" + "---+" * cols)
    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)


# ===========================
# Game mechanics
# ===========================
def get_valid_column_input(cols: int, current_player_token: str) -> int:
    """
    Continues to prompt the user until a valid column letter (A..A+cols-1) is entered.
    Returns the column index (0-based).
    """
    max_col_label = column_label(cols - 1)
    while True:
        user_input = input(f"Player {current_player_token}, please enter a column: ").strip().upper()
        # Validate single letter within range A..max_col_label
        if len(user_input) == 1 and 'A' <= user_input <= max_col_label:
            return ord(user_input) - ord('A')
        # Invalid input, re-prompt
        print(f"Invalid input. Enter a single letter between A and {max_col_label}.")


def place_checker(board: List[List[str]], col: int, token: str) -> bool:
    """
    Attempt to place the token in the given column.
    The token falls to the lowest available cell.
    Returns True if placed, False if the column is full.
    """
    rows = len(board)
    # Start from the bottom row
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True
    return False  # Column full


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], last_token: str) -> bool:
    """
    Check if any player (or specifically last_token) has a winning line.
    For efficiency, we can check all tokens on the board generically.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    directions: List[Tuple[int, int]] = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            token = board[r][c]
            if token == " ":
                continue
            # Optional micro-optimization: only check for the last_token
            if last_token is not None and token != last_token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= WIN_LENGTH:
                    return True
    return False


def check_draw(board: List[List[str]]) -> bool:
    """
    Return True if the board is full (no spaces), otherwise False.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# ===========================
# Main game loop
# ===========================
def main() -> None:
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial print before the game starts
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_token = PLAYER_TOKENS[current_player_idx]

        # Prompt input for a valid column letter
        col_idx = get_valid_column_input(COLS, current_token)

        # Try to place the checker
        placed = place_checker(board, col_idx, current_token)

        # Clear and print updated board after the attempt
        clear_screen()
        print_board(board)

        if placed:
            # Check for win
            if check_win(board, current_token):
                print(f"Player {current_token} won!")
                break

            # Check for draw
            if check_draw(board):
                print("The game is a draw.")
                break

            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {column_label(col_idx)} is full. Player {current_token} loses the turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        # Loop continues; the board is printed at the start of each iteration

    # Game over


if __name__ == "__main__":
    main()
