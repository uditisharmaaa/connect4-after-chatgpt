import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5  # max players supported
MIN_PLAYERS = 2  # min players supported
NUM_PLAYERS = 2  # set number of players for submission (2 players)
CONNECT_N = 4    # number of checkers in a row to win

# Players' checker symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Map column letters to indices (A->0, B->1, ..., Z->25)
COL_LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create an empty board with given dimensions."""
    # Board is a list of rows, each row is a list of cells
    # empty cells represented by ' '
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column headers and borders."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COL_LETTERS))

    # Print top border and rows with cell content
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def get_column_index(input_str):
    """Convert a column letter to index if valid, otherwise return None."""
    if len(input_str) != 1:
        return None
    letter = input_str.upper()
    if letter in COL_LETTERS:
        return COL_LETTERS.index(letter)
    return None

def is_column_full(board, col):
    """Check if a given column is full (no empty spaces)."""
    # Since new checkers drop to lowest empty row, if top row (row 0) is occupied, column is full
    return board[0][col] != " "

def place_checker(board, col, checker):
    """
    Place the player's checker in the lowest available position in the chosen column.
    Return True if placed, False if column full.
    """
    # Start checking from bottom row upwards
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column full
    return False

def check_winner(board, checker):
    """Check if the given checker has 4 in a row horizontally, vertically or diagonally."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - CONNECT_N + 1):
            if all(board[r][c+i] == checker for i in range(CONNECT_N)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - CONNECT_N + 1):
            if all(board[r+i][c] == checker for i in range(CONNECT_N)):
                return True

    # Diagonal down-right check
    for r in range(rows - CONNECT_N + 1):
        for c in range(cols - CONNECT_N + 1):
            if all(board[r+i][c+i] == checker for i in range(CONNECT_N)):
                return True

    # Diagonal down-left check
    for r in range(rows - CONNECT_N + 1):
        for c in range(CONNECT_N - 1, cols):
            if all(board[r+i][c-i] == checker for i in range(CONNECT_N)):
                return True

    return False

def is_board_full(board):
    """Return True if the board is completely filled with no empty spaces."""
    for row in board:
        if " " in row:
            return False
    return True

def input_column(player):
    """
    Prompt player for a column input, and validate input until correct.
    Return column index integer.
    """
    while True:
        input_col = input(f"Player {player}, please enter a column: ").strip()
        col_idx = get_column_index(input_col)
        if col_idx is None:
            print("Invalid input! Please enter a valid column letter.")
            continue
        if is_column_full(board, col_idx):
            # According to spec, turn is lost if column full
            print(f"Column {input_col.upper()} is full! You lose your turn.")
            return None
        return col_idx

# --- Main game logic ---

# Create the board
board = create_board(ROWS, COLS)

# Select the players' symbols based on number of players
players = PLAYER_SYMBOLS[:NUM_PLAYERS]

# Randomly select starting player index
current_player_idx = random.randint(0, NUM_PLAYERS - 1)

# Print initial board
print_board(board)

# Main game loop
while True:
    current_player = players[current_player_idx]

    col = input_column(current_player)
    if col is None:
        # Player loses turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print_board(board)
        continue

    placed = place_checker(board, col, current_player)
    print_board(board)

    # After placing checker, check if current player won
    if check_winner(board, current_player):
        print(f"Player {current_player} won!")
        break

    # Check for draw
    if is_board_full(board):
        print("The game is a draw!")
        break

    # Move to next player
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
