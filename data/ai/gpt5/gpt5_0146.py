import random
import os
import string
import sys

# -------------------------------
# Configuration constants
# -------------------------------
ROWS = 6                 # number of rows (default for submission: 6)
COLUMNS = 7              # number of columns (default for submission: 7) - max 26
NUM_PLAYERS = 2          # players: 2 to 5 (default for submission: 2)
TOKENS = ["X", "O", "V", "H", "M"]  # tokens for players in order

# -------------------------------
# Validation of configuration
# -------------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLUMNS > 26:
    print("COLUMNS must be at most 26.")
    sys.exit(1)

# Slice tokens to number of players
PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]

# -------------------------------
# Board utility functions
# -------------------------------
def create_board(rows, cols):
    """
    Create a board with given dimensions initialized with spaces.
    Board is a list of lists: board[row][col].
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """
    Clear the terminal screen (Linux/Unix).
    """
    os.system('clear')

def print_board(board):
    """
    Print the board with column headers (A..), grid lines, and cells.
    """
    rows = len(board)
    cols = len(board[0])

    clear_screen()

    # Header with letters
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    header_line = "  " + "   ".join(headers)
    print(header_line)

    # Top border
    print("+---" * cols + "+")

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+---" * cols + "+")

def column_from_input(inp, cols):
    """
    Convert a single uppercase letter input to a column index.
    Returns column index or None if invalid.
    """
    if len(inp) != 1:
        return None
    if inp < 'A' or inp > 'Z':
        return None
    col = ord(inp) - ord('A')
    if 0 <= col < cols:
        return col
    return None

def find_drop_row(board, col):
    """
    Given a column index, return the row index where the checker will land,
    or None if the column is full.
    The checker drops to the lowest available (from bottom up).
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def board_full(board):
    """
    Return True if the board is full (no spaces), else False.
    """
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, start_r, start_c, dr, dc, token):
    """
    Count consecutive tokens from a starting cell moving in direction (dr, dc).
    Returns the count.
    """
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def has_winner(board, last_row, last_col, token):
    """
    Check if placing 'token' at (last_row, last_col) created a connect-4.
    We count in both directions for each axis and diagonal.
    Directions checked:
      - Horizontal (0,1)
      - Vertical (1,0)
      - Diagonal down-right (1,1)
      - Diagonal up-right (-1,1)
    """
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        # count in positive direction
        pos = check_win_from(board, last_row, last_col, dr, dc, token)
        # count in negative direction, excluding the starting cell to avoid double counting
        neg = check_win_from(board, last_row - dr, last_col - dc, -dr, -dc, token)
        if pos + neg >= 4:
            return True
    return False

# -------------------------------
# Game loop
# -------------------------------
def main():
    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Randomly choose starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Print initial board before game starts
    print_board(board)

    # Main game loop
    winner = None
    while True:
        token = PLAYER_TOKENS[current_player_idx]

        # Prompt until valid input letter is provided (column full is a different case)
        while True:
            user_input = input(f"Player {token}, please enter a column: ").strip().upper()

            col = column_from_input(user_input, COLUMNS)
            if col is None:
                # Invalid input (e.g., number, out of range, multi-char)
                print("Invalid input. Please enter a valid column letter within range.")
                continue

            # Valid column letter; attempt to place checker
            drop_row = find_drop_row(board, col)
            if drop_row is None:
                # Column is full: turn is lost as per spec
                print(f"Column {string.ascii_uppercase[col]} is full. You lose your turn.")
                # No placement; move to next player
                # Before switching, check for draw (board might be full)
                if board_full(board):
                    print_board(board)
                    print("It's a draw!")
                    return
                # Print the board to show no change, then break out to switch player
                print_board(board)
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break
            else:
                # Place the checker
                board[drop_row][col] = token
                # After each action, print the board
                print_board(board)

                # Check for win
                if has_winner(board, drop_row, col, token):
                    print(f"Player {token} won!")
                    return

                # Check for draw
                if board_full(board):
                    print("It's a draw!")
                    return

                # Switch to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break

if __name__ == "__main__":
    main()
