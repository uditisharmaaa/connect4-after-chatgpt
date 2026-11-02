import os
import random
import string
from typing import List, Optional, Tuple

# ----------------------- Configuration -----------------------
ROWS = 6            # Number of rows (default submission requirement: 6)
COLS = 7            # Number of columns (default submission requirement: 7, max 26)
WIN_LENGTH = 4      # Connect 4 condition
MAX_COLS = 26       # Limit due to alphabet labeling

# Player configuration (default submission requirement: 2 players)
CHECKERS = ["X", "O", "V", "H", "M"]  # Order must be X, O, V, H, M
NUM_PLAYERS = 2                        # Allowed range: 2..5

# ----------------------- Validation --------------------------
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > MAX_COLS:
    raise ValueError(f"COLS must be <= {MAX_COLS}.")
if NUM_PLAYERS > len(CHECKERS):
    raise ValueError("Not enough checker symbols for the number of players.")

ACTIVE_CHECKERS = CHECKERS[:NUM_PLAYERS]

# ----------------------- Board Logic -------------------------
def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_and_print_board(board: List[List[str]]) -> None:
    """Clear the screen and render the board with column headers A.."""
    os.system('clear')
    cols = len(board[0])
    # Header
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    # Rows (top to bottom)
    for r in range(len(board)):
        print(sep)
        row_cells = "|" + "|".join(f" {cell} " for cell in board[r]) + "|"
        print(row_cells)
    print(sep)

def is_valid_column_input(user_input: str, cols: int) -> bool:
    """Check if input is a single letter within the board columns."""
    if not user_input or len(user_input) != 1:
        return False
    ch = user_input.upper()
    if not ("A" <= ch <= "Z"):
        return False
    idx = ord(ch) - ord('A')
    return 0 <= idx < cols

def column_index_from_input(user_input: str) -> int:
    """Convert column letter to 0-based index."""
    return ord(user_input.upper()) - ord('A')

def lowest_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    """Return the lowest empty row index for a given column, or None if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    """Place checker in the specified column if possible; return (row, col) or None if column full."""
    r = lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return (r, col)

def in_bounds(board: List[List[str]], r: int, c: int) -> bool:
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def check_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, checker: str) -> int:
    """Count consecutive checkers including the starting cell in a direction and its opposite."""
    count = 1
    # Forward
    r, c = start_r + dr, start_c + dc
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    # Backward
    r, c = start_r - dr, start_c - dc
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r -= dr
        c -= dc
    return count

def check_win(board: List[List[str]], last_r: int, last_c: int, checker: str) -> bool:
    """Check whether placing checker at (last_r, last_c) creates a winning line."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        if check_direction(board, last_r, last_c, dr, dc, checker) >= WIN_LENGTH:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    """Return True if board is completely filled."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# ----------------------- Input Handling ----------------------
def prompt_for_column(current_checker: str, cols: int) -> int:
    """Prompt the current player until a valid column letter is provided."""
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        if is_valid_column_input(user_input, cols):
            return column_index_from_input(user_input)
        else:
            print("Invalid input. Please enter a valid column letter.")

# ----------------------- Game Loop ---------------------------
def main() -> None:
    random.seed()  # Initialize RNG
    board = create_board(ROWS, COLS)

    # Random starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial render before the game starts
    clear_and_print_board(board)

    # Main game loop
    while True:
        checker = ACTIVE_CHECKERS[current_player_idx]
        # Prompt for a valid column letter (input validation does not lose turn)
        col = prompt_for_column(checker, COLS)

        # Try to place the checker (if column full, player loses the turn)
        placed_pos = place_checker(board, col, checker)
        if placed_pos is None:
            # Column is full; turn is lost
            clear_and_print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {checker} loses this turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successful placement
        last_r, last_c = placed_pos

        # Render updated board
        clear_and_print_board(board)

        # Check for win
        if check_win(board, last_r, last_c, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
