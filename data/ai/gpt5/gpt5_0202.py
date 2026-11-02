import os
import random
import string
import sys

# Constants (submission requirement: 6 rows x 7 columns, 2 players)
ROWS = 6            # Number of rows (height)
COLS = 7            # Number of columns (width) - must be <= 26
NUM_PLAYERS = 2     # Supported range: 2..5

# Available checker symbols in order. Players use the first NUM_PLAYERS of these.
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

# Precompute column labels (A..Z)
COL_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    """
    Clear the terminal screen (Linux/Unix).
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Create an empty board initialized with spaces.
    Board is a list of lists, indexed by [row][col].
    Top row is index 0; bottom row is index rows - 1.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column labels and grid lines.
    Matches the style shown in the assignment description.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column labels
    header = "  " + "   ".join(COL_LABELS[:cols])
    print(header)

    # Build horizontal divider line like +---+---+...+
    divider = "+" + "+".join(["---"] * cols) + "+"

    # For each row, print divider, then the row content
    for r in range(rows):
        print(divider)
        # Each cell is centered within 3 spaces
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    # Bottom divider
    print(divider)


def find_lowest_empty_row(board, col):
    """
    Return the index of the lowest empty row in the given column.
    If the column is full, return None.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(rows, cols, r, c):
    """
    Check if (r, c) is within the bounds of the board.
    """
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers starting from (start_r, start_c) moving
    in direction (dr, dc), for the given checker symbol.
    Does not include the starting cell itself.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(rows, cols, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, checker):
    """
    Check whether placing 'checker' at (last_r, last_c) causes a win.
    A win is 4 in a row horizontally, vertically, or diagonally.
    """
    # Directions to check: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count both directions from the last placed checker
        total = 1  # include the placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, checker)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= 4:
            return True
    return False


def board_full(board):
    """
    Return True if the board has no empty spaces, else False.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_valid_column_input():
    """
    Prompt the user for a column letter, validate it, and return a column index.
    Keeps prompting until a valid input is provided.
    Valid input is a single letter corresponding to a column label (A..).
    """
    valid_labels = COL_LABELS
    while True:
        user_input = input().strip()
        if len(user_input) == 0:
            print("Invalid input. Please enter a column letter (e.g., A).")
            print("Player, please enter a column:")
            continue
        letter = user_input.upper()
        if len(letter) != 1 or letter not in valid_labels:
            print("Invalid input. Please enter a valid column letter on the board.")
            print("Player, please enter a column:")
            continue
        col_index = valid_labels.index(letter)
        return col_index


def main():
    # Initialize game state
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select the starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show the empty board before starting, as per instructions
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]} will start.")
    input("Press Enter to begin...")

    # Main game loop
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_idx]}, please enter a column:")

        # Get a valid column index
        col = get_valid_column_input()

        # Find the lowest empty row in the selected column
        row = find_lowest_empty_row(board, col)

        if row is None:
            # Column is full -> invalid turn and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {COL_LABELS[col]} is full. Player {players[current_player_idx]} loses the turn.")
            input("Press Enter to continue...")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        checker = players[current_player_idx]
        board[row][col] = checker

        # Check for a win
        if check_win(board, row, col, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check for a draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
