import os
import random
import string

# Constants
ROWS = 6               # Number of rows
COLS = 7               # Number of columns
MIN_PLAYERS = 2        # Minimum number of players
MAX_PLAYERS = 5        # Maximum number of players
NUM_PLAYERS = 2        # Number of players for this assignment submission
WIN_LENGTH = 4         # Number of checkers in a row needed to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Player checkers in order

# Validate NUM_PLAYERS within allowed range
if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
    raise ValueError(f"NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")

# Selected checkers for the current game
PLAYERS = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create and return an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board to the terminal as per assignment formatting."""
    clear_screen()
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))
    horizontal_line = "+" + "---+" * cols
    for row in board:
        print(horizontal_line)
        print("| " + " | ".join(row) + " |")
    print(horizontal_line)

def is_valid_column(column_letter, cols):
    """Check if the column letter is valid on the board."""
    if len(column_letter) != 1:
        return False
    column_letter = column_letter.upper()
    if column_letter < 'A' or column_letter >= chr(ord('A') + cols):
        return False
    return True

def column_to_index(column_letter):
    """Convert column letter to zero-based index."""
    return ord(column_letter.upper()) - ord('A')

def is_column_full(board, col_idx):
    """Return True if the given column is full (no spaces)."""
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest empty row of the given column.
    Return True if successful, False if column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False  # Column full

def check_line(line, checker):
    """Check a list of cells (line) for WIN_LENGTH consecutive checkers."""
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal lines
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical lines
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-right (\)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal up-right (/)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """Return True if board is full and no winner."""
    return all(cell != " " for cell in board[0])

def get_player_input(player):
    """Prompt player for a valid column letter input."""
    cols = len(board[0])
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if not is_valid_column(col, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = column_to_index(col)
        if is_column_full(board, col_idx):
            print("Column is full. Turn lost.")
            return None
        return col_idx

# Initialize the board
board = create_board(ROWS, COLS)

# Randomly select starting player index
current_player_idx = random.randint(0, NUM_PLAYERS - 1)
current_checker = PLAYERS[current_player_idx]

print_board(board)
print(f"Player {current_checker} starts the game.")

while True:
    col_idx = get_player_input(current_checker)
    if col_idx is not None:
        placed = place_checker(board, col_idx, current_checker)
        # As per assignment, if column was full, turn lost and should not ask again,
        # but we already handled that in get_player_input by returning None.
        # So if col_idx is None, it means turn lost and we skip placing.
        if placed:
            print_board(board)
            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check for draw
            if check_draw(board):
                print("The game is a draw.")
                break
        else:
            # Should not happen since checked for full in get_player_input
            print("Unexpected error: could not place checker.")
    else:
        # Turn lost due to full column, skip placing
        print_board(board)

    # Move to next player
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
    current_checker = PLAYERS[current_player_idx]
