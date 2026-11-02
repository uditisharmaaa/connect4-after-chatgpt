# Connect 4 game for Intro CS
# - 6 rows x 7 columns
# - Columns labeled A-G
# - 2 to 5 players (symbols: X, O, V, H, M) selectable via constants
# - Random first player
# - Robust input validation
# - Win and draw detection
# - Uses os.system('clear') to refresh the screen

import os
import random
import sys
from typing import List, Optional, Tuple

# -----------------------------
# Configuration Constants
# -----------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A', 'B', ..., 'G']

# Define up to 5 player symbols here (order matters).
ALL_PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Set how many players will play (between 2 and 5).
PLAYER_COUNT = 2  # change to 3, 4, or 5 as desired

# -----------------------------
# Utility Functions
# -----------------------------
def clear_screen():
    """Clear the console screen using 'clear' as requested."""
    # Use 'clear' primarily (as requested). Fallback to 'cls' on Windows if desired.
    # If your environment doesn't support clearing, you can comment this out.
    if os.name == 'nt':
        # Most Windows terminals use 'cls'; but request emphasized 'clear'.
        # We'll still prefer 'clear', and if it fails, try 'cls'.
        exit_code = os.system('clear')
        if exit_code != 0:
            os.system('cls')
    else:
        os.system('clear')

def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create an empty board as a 2D list filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]):
    """Print the board with column labels and grid lines."""
    # Column labels
    print('   ' + '   '.join(COLUMN_LABELS))
    print(' +' + '---+' * COLS)
    for r in range(ROWS):
        row_str = '|'.join(f' {board[r][c]} ' for c in range(COLS))
        print(f' |{row_str}|')
        print(' +' + '---+' * COLS)

def col_label_to_index(label: str) -> Optional[int]:
    """Convert a column label (A-G) to index, return None if invalid."""
    label = label.strip().upper()
    if label in COLUMN_LABELS:
        return ord(label) - ord('A')
    return None

def is_valid_location(board: List[List[str]], col: int) -> bool:
    """Check if there is at least one empty spot in the given column."""
    return board[0][col] == ' '

def get_next_open_row(board: List[List[str]], col: int) -> Optional[int]:
    """Return the lowest open row index in the column, or None if full."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board: List[List[str]], row: int, col: int, piece: str):
    """Place the player's piece at the specified (row, col)."""
    board[row][col] = piece

def winning_move(board: List[List[str]], piece: str) -> bool:
    """Check if the player with 'piece' has a connect-4."""
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r][c + 1] == piece and
                board[r][c + 2] == piece and
                board[r][c + 3] == piece):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r + 1][c] == piece and
                board[r + 2][c] == piece and
                board[r + 3][c] == piece):
                return True

    # Positive diagonal (down-right) check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and
                board[r + 3][c + 3] == piece):
                return True

    # Negative diagonal (up-right) check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and
                board[r - 3][c + 3] == piece):
                return True

    return False

def is_draw(board: List[List[str]]) -> bool:
    """Return True if the board is full (no more moves)."""
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_player_input(current_player: str) -> str:
    """Prompt the current player for a column letter and validate."""
    while True:
        move = input(f"Player {current_player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").strip()
        # Basic input validation
        if not move:
            print("Input cannot be empty. Try again.")
            continue

        idx = col_label_to_index(move)
        if idx is None:
            print(f"Invalid column. Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue

        return COLUMN_LABELS[idx]  # Return normalized label

def choose_first_player(players: List[str]) -> int:
    """Pick a random starting player index."""
    return random.randrange(len(players))

# -----------------------------
# Main Game Loop
# -----------------------------
def main():
    # Validate player configuration
    if not (2 <= PLAYER_COUNT <= 5):
        print("PLAYER_COUNT must be between 2 and 5.")
        sys.exit(1)
    if len(ALL_PLAYERS) < PLAYER_COUNT:
        print("Not enough player symbols defined in ALL_PLAYERS.")
        sys.exit(1)

    players = ALL_PLAYERS[:PLAYER_COUNT]

    board = create_board(ROWS, COLS)
    current_index = choose_first_player(players)

    # Initial screen
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Players: {' '.join(players)}")
    print(f"Randomly selected first player: {players[current_index]}")
    print_board(board)

    while True:
        current_player = players[current_index]
        # Ask for input until a valid, non-full column is given
        while True:
            col_label = get_player_input(current_player)
            col = col_label_to_index(col_label)
            if col is None:
                # Should not happen due to earlier check, but safe-guard
                print("Invalid input. Try again.")
                continue
            if not is_valid_location(board, col):
                print(f"Column {col_label} is full. Choose a different column.")
                continue
            break

        # Place the piece
        row = get_next_open_row(board, col)
        if row is None:
            # Very unlikely due to prior check
            print(f"Column {col_label} is unexpectedly full. Try again.")
            continue

        drop_piece(board, row, col, current_player)

        # Refresh screen and show updated board
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(players)}")
        print_board(board)

        # Check for win
        if winning_move(board, current_player):
            print(f"Player {current_player} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw! No more valid moves.")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)

if __name__ == "__main__":
    main()
