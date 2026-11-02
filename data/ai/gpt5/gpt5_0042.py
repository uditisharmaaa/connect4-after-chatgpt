import os
import random
import string
import sys

# ------------------------- Configuration Constants -------------------------
# Board dimensions (submission requires 6 rows x 7 columns)
ROWS = 6
COLS = 7  # Must be <= 26 (one letter per column)
# Number of players (submission requires 2 players)
NUM_PLAYERS = 2  # Can be from 2 to 5

# The order of player checkers; players are assigned in order from this list
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row required to win
CONNECT_N = 4

# ------------------------- Validation of Configuration -------------------------
if COLS > 26 or COLS < 1:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

# Use the first NUM_PLAYERS checkers
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]

# ------------------------- Board Utilities -------------------------
def create_board(rows, cols):
    """
    Create a board with given dimensions, filled with spaces.
    Board is a list of rows; board[r][c] is the cell at row r and column c.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """
    Clear the terminal screen. Linux/Unix uses 'clear'.
    """
    os.system('clear')

def print_board(board):
    """
    Print the board in the specified ASCII format with column headers A..,
    rows with grid lines, and cells containing player tokens or spaces.
    """
    clear_screen()
    cols = len(board[0])
    rows = len(board)

    # Header with column letters
    letters = list(string.ascii_uppercase[:cols])
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal line for top of the grid
    horiz = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(horiz)
        # Row cells
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c] if board[r][c] != "" else " ")
        print("| " + " | ".join(row_cells) + " |")
    # Bottom line
    print(horiz)

def is_full(board):
    """
    Return True if the board is full (no spaces left), else False.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def drop_checker(board, col_idx, token):
    """
    Attempt to drop a token into column 'col_idx'.
    Returns:
      - placed_row_index if the token was placed
      - None if the column is full (no placement)
    """
    rows = len(board)
    # Start from the bottom row and find the first empty space
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return r
    return None  # Column full

# ------------------------- Win Checking -------------------------
def check_win_from_cell(board, start_r, start_c, dr, dc, token):
    """
    Check CONNECT_N in a row from (start_r, start_c) in direction (dr, dc) for token.
    """
    rows = len(board)
    cols = len(board[0])

    for k in range(CONNECT_N):
        r = start_r + dr * k
        c = start_c + dc * k
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != token:
            return False
    return True

def check_win(board, token):
    """
    Check if the given token has a winning CONNECT_N sequence anywhere on the board.
    Directions: horizontal (0,1), vertical (1,0), diag down-right (1,1), diag down-left (1,-1)
    """
    rows = len(board)
    cols = len(board[0])
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if check_win_from_cell(board, r, c, dr, dc, token):
                    return True
    return False

# ------------------------- Input Handling -------------------------
def get_column_input(valid_cols):
    """
    Prompt the user to enter a column letter. Validate input:
    - Single alphabetic character
    - Within the range of available columns
    Keeps prompting until a valid input is received.
    Returns the uppercase letter and its index.
    """
    while True:
        try:
            inp = input().strip()
        except EOFError:
            # Gracefully exit on EOF
            print("\nInput closed. Exiting game.")
            sys.exit(0)

        if len(inp) != 1 or not inp.isalpha():
            print("Invalid input. Please enter a single letter for the column:")
            continue

        letter = inp.upper()
        if letter not in valid_cols:
            print("Invalid column. Please enter a valid column letter:")
            continue

        return letter, valid_cols.index(letter)

# ------------------------- Game Loop -------------------------
def main():
    # Initialize board
    board = create_board(ROWS, COLS)
    col_letters = list(string.ascii_uppercase[:COLS])

    # Randomly choose starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)

    # Game loop
    while True:
        current_token = PLAYER_TOKENS[current_player_idx]
        # Prompt
        print(f"Player {current_token}, please enter a column:")

        # Get a valid column letter input (does not lose turn on invalid input)
        letter, col_idx = get_column_input(col_letters)

        # Attempt to place the checker
        placed_row = drop_checker(board, col_idx, current_token)

        if placed_row is None:
            # Column full: turn is invalid and the player loses the turn
            print_board(board)
            print(f"Column {letter} is full. Player {current_token} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Continue to next iteration
            continue

        # Successful placement: show updated board
        print_board(board)

        # Check for a win for the current player
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for a draw
        if is_full(board):
            print("The game is a draw!")
            break

        # Advance to next player after a successful turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
