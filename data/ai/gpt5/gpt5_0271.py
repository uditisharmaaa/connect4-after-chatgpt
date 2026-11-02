import os
import random
import string
from typing import List, Optional, Tuple

# ----------------------------
# Configuration (constants)
# ----------------------------

# Board dimensions (rows x cols). Assignment requires submission with 6x7.
ROWS = 6
COLS = 7  # Max 26 columns (A-Z)
WIN_LENGTH = 4  # Number of connected checkers needed to win (fixed at 4)

# Number of players (between 2 and 5). Assignment requires 2 for submission.
NUM_PLAYERS = 2

# Player tokens in order. Will use the first NUM_PLAYERS from this list.
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]


# ----------------------------
# Utility / Validation
# ----------------------------

def validate_configuration(rows: int, cols: int, num_players: int) -> None:
    """Validate global configuration constants."""
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if cols < 1 or cols > 26:
        raise ValueError("COLS must be between 1 and 26 (inclusive).")
    if rows < 1:
        raise ValueError("ROWS must be at least 1.")
    if num_players > len(PLAYER_TOKENS):
        raise ValueError("Not enough PLAYER_TOKENS defined for NUM_PLAYERS.")


# ----------------------------
# Board Representation
# ----------------------------

Board = List[List[str]]  # board[row][col]

def create_board(rows: int, cols: int) -> Board:
    """Create an empty board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen() -> None:
    """Clear the terminal screen (Unix/Linux)."""
    os.system('clear')


def print_board(board: Board) -> None:
    """Clear screen and print the current board with column headers."""
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (letters A..)
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)

    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c] if board[r][c] != " " else " ")
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


# ----------------------------
# Game Mechanics
# ----------------------------

def column_from_input(user_input: str, cols: int) -> Optional[int]:
    """Convert user input to a column index if valid, else return None."""
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return None
    return ord(ch) - ord('A')


def find_available_row(board: Board, col: int) -> Optional[int]:
    """Find the lowest available row index in the given column (or None if full)."""
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_token(board: Board, col: int, token: str) -> Optional[Tuple[int, int]]:
    """Place a token in the given column. Return (row, col) or None if column is full."""
    r = find_available_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return (r, col)


def board_full(board: Board) -> bool:
    """Return True if there are no empty spaces on the board."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def check_win(board: Board, token: str) -> bool:
    """Check if the given token has a winning sequence of WIN_LENGTH."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                # Forward direction
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc

                # Backward direction
                rr, cc = r - dr, c - dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token:
                    count += 1
                    rr -= dr
                    cc -= dc

                if count >= WIN_LENGTH:
                    return True
    return False


# ----------------------------
# Game Loop
# ----------------------------

def game_loop(rows: int, cols: int, num_players: int) -> None:
    """Run the Connect 4 game loop."""
    validate_configuration(rows, cols, num_players)
    tokens = PLAYER_TOKENS[:num_players]
    board = create_board(rows, cols)

    # Randomly choose starting player
    current_player_idx = random.randint(0, num_players - 1)

    # Show initial empty board and announce first player
    print_board(board)
    print(f"Player {tokens[current_player_idx]} starts!")

    while True:
        # Display current board before asking for input
        print_board(board)
        print(f"Player {tokens[current_player_idx]}, please enter a column:")

        # Get valid input (letter within range)
        col_idx: Optional[int] = None
        last_col_letter = chr(ord('A') + cols - 1)
        while True:
            user_in = input().strip()
            col_idx = column_from_input(user_in, cols)
            if col_idx is not None:
                break
            print(f"Invalid input. Please enter a column letter between A and {last_col_letter}:")

        # Attempt to place token
        token = tokens[current_player_idx]
        placed = place_token(board, col_idx, token)

        if placed is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            col_letter = chr(ord('A') + col_idx)
            print(f"Column {col_letter} is full. Turn lost.")
            # Check draw even though board unchanged (in case the board is fully filled)
            if board_full(board):
                print("It's a draw!")
                return
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        # After a successful move, check for win
        if check_win(board, token):
            print_board(board)
            print(f"Player {token} won!")
            return

        # Check for draw
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players


# ----------------------------
# Entry Point
# ----------------------------

def main() -> None:
    random.seed()  # Initialize RNG
    game_loop(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
