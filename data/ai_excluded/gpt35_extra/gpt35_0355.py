import os
import random
import sys

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Using 2 players and 6x7 board as required for submission
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    """Create and return an empty board with given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board with column headers as letters."""
    columns = len(board[0])
    rows = len(board)
    # Print column labels
    header = "  "
    for c in range(columns):
        header += f"  {chr(ord('A') + c)} "
    print(header)
    # Print horizontal separator and rows
    sep = "+" + "---+" * columns
    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(columns):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)

def is_valid_column(col_char, columns):
    """Check if the column letter is valid (A to corresponding max)."""
    if len(col_char) != 1:
        return False
    ord_col = ord(col_char)
    return ord('A') <= ord_col < ord('A') + columns

def column_index(col_char):
    """Convert column letter to zero-based index."""
    return ord(col_char) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place the checker in the given column if possible.
    Return True if placement was successful, False if column full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(columns):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(columns):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal checks (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(columns - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal checks (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(columns - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    """Return True if board is full, otherwise False."""
    for row in board:
        if " " in row:
            return False
    return True

def input_column(current_player, player_checker, columns):
    """Prompt the current player for a column until valid input is received."""
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(col, columns):
            # Invalid column letter
            continue
        col_idx = column_index(col)
        return col_idx

def main():
    if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        sys.exit(1)

    # Initialize board and player checkers
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        current_checker = player_checkers[current_player_idx]

        # Input & validation loop
        col_idx = input_column(current_player_idx, current_checker, COLUMNS)

        # Try to place checker, if column full player loses turn
        placed = place_checker(board, col_idx, current_checker)

        clear_screen()
        print_board(board)

        if not placed:
            # Column full - player loses turn
            pass
        else:
            # Check if current player wins
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check draw
            if board_full(board):
                print("The game is a draw!")
                break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
