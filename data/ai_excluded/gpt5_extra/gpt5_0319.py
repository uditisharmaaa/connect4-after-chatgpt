import os
import random
import string
from typing import List, Optional, Tuple

# ========================
# Configuration constants
# ========================
ROWS = 6
COLUMNS = 7          # Max 26 columns supported (A-Z)
NUM_PLAYERS = 2      # Supported: 2..5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Validate configuration
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert 1 <= COLUMNS <= 26, "COLUMNS must be between 1 and 26 (A-Z)"
assert ROWS >= 4 and COLUMNS >= 4, "Board must be at least 4x4 for Connect 4"
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]


def clear_screen() -> None:
    """Clear the terminal screen (Unix/Linux)."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a rows x cols board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """Render the board to the terminal."""
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def is_valid_column_letter(ch: str, cols: int) -> bool:
    """Check if the given character corresponds to a valid column letter A.."""
    if len(ch) != 1 or not ch.isalpha():
        return False
    ch = ch.upper()
    letters = string.ascii_uppercase[:cols]
    return ch in letters


def col_letter_to_index(ch: str) -> int:
    """Convert column letter A.. to 0-based index."""
    return ord(ch.upper()) - ord('A')


def get_lowest_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    """Return the lowest empty row index for the given column, or None if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    """Place the token in the given column if possible. Return (row, col) or None if column is full."""
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], token: str) -> bool:
    """Check whether the given token has a win of length WIN_LENGTH on the board."""
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    nr += dr
                    nc += dc
                if count == WIN_LENGTH:
                    return True
    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if the board has no empty spaces."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def prompt_for_column(current_token: str, cols: int) -> int:
    """Prompt the user until a valid column letter is entered. Returns zero-based index."""
    while True:
        user_input = input(f"Player {current_token}, please enter a column: ").strip()
        if len(user_input) == 0:
            print("Invalid input. Please enter a column letter.")
            continue
        ch = user_input[0].upper()
        if not is_valid_column_letter(ch, cols):
            print("Invalid column. Please enter a valid column letter within the board.")
            continue
        return col_letter_to_index(ch)


def main() -> None:
    random.seed()
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)

        current_token = PLAYER_TOKENS[current_player_index]

        # Before turn, check for draw (in case the board is full with no winner)
        if board_full(board):
            print("It's a draw!")
            break

        # Get a valid column input (letter within range)
        col_index = prompt_for_column(current_token, COLUMNS)

        # Attempt to drop the checker
        result = drop_checker(board, col_index, current_token)
        if result is None:
            # Column full: invalid turn, player loses turn
            col_letter = string.ascii_uppercase[col_index]
            print(f"Column {col_letter} is full. You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Wait for user to acknowledge so message isn't immediately cleared
            input("Press Enter to continue...")
            continue

        # Successful placement: check for win
        if check_win(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} won!")
            break

        # Check for draw after a successful move
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
