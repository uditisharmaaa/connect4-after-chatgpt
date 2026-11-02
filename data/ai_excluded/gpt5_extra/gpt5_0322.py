import os
import random
import string

# -------------------------------
# Constants (adjustable)
# -------------------------------
ROWS = 6                     # Number of rows (default submission requires 6)
COLS = 7                     # Number of columns (default submission requires 7, max 26)
NUM_PLAYERS = 2              # Number of players (2 to 5; default submission requires 2)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for up to 5 players, in order

# -------------------------------
# Utility and Validation
# -------------------------------

def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')

def clamp_game_settings():
    """Ensure game settings are valid; adjust if necessary."""
    global COLS, ROWS, NUM_PLAYERS
    # Enforce maximum columns due to labeling with letters
    COLS = max(1, min(COLS, 26))
    ROWS = max(1, ROWS)
    NUM_PLAYERS = max(2, min(NUM_PLAYERS, 5))

def column_labels():
    """Return a list of column labels 'A', 'B', ..., according to COLS."""
    return list(string.ascii_uppercase[:COLS])

def is_valid_column_label(label):
    """Check if a given label is a single uppercase column letter within board."""
    return len(label) == 1 and label in column_labels()

def column_to_index(label):
    """Convert a column label (e.g., 'A') to the corresponding column index (0-based)."""
    return ord(label) - ord('A')

# -------------------------------
# Board Creation and Printing
# -------------------------------

def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in the required format."""
    cols = len(board[0])
    labels = column_labels()

    # Header with column labels
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + "---+" * cols)
    # Rows from top to bottom
    for r in range(len(board)):
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
        print("+" + "---+" * cols)

# -------------------------------
# Game Mechanics
# -------------------------------

def get_lowest_empty_row(board, col):
    """Return the lowest available row index in a column, or None if the column is full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, symbol):
    """Place a checker in the specified column if possible. Return True if placed, else False."""
    row = get_lowest_empty_row(board, col)
    if row is None:
        return False
    board[row][col] = symbol
    return True

def check_win(board, symbol):
    """Check if the given symbol has a 4-in-a-row anywhere on the board."""
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # Directions: right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                # Check next 3 cells in the direction
                for k in range(1, 4):
                    nr, nc = r + dr * k, c + dc * k
                    if in_bounds(nr, nc) and board[nr][nc] == symbol:
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
    return False

def check_draw(board):
    """Return True if the board is full and no more moves can be made."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# -------------------------------
# Input Handling
# -------------------------------

def prompt_for_column(current_symbol):
    """
    Prompt the current player for a column letter.
    Validate input as an uppercase column label (A..).
    If invalid, keep prompting until valid.
    """
    labels = set(column_labels())
    while True:
        user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in labels:
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue
        return user_input

# -------------------------------
# Main Game Loop
# -------------------------------

def main():
    clamp_game_settings()

    # Prepare players' symbols according to NUM_PLAYERS
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Create the game board
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = players[current_player_index]

        # Ask the current player for a move (validated column label)
        col_label = prompt_for_column(current_symbol)
        col_index = column_to_index(col_label)

        # Attempt to place the checker
        placed = place_checker(board, col_index, current_symbol)

        # Clear and reprint board after the move attempt (as per requirement)
        clear_screen()
        print_board(board)

        if not placed:
            # Column was full; player loses the turn
            print(f"Column {col_label} is full. Player {current_symbol} loses the turn.")
            # No win possible without placing; proceed to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Check for a win after a successful placement
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
