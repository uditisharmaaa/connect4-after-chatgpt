import os
import random
import string
import sys

# ------------------------------
# Configuration (changeable)
# ------------------------------
ROWS = 6                 # Number of rows (default: 6)
COLS = 7                 # Number of columns (default: 7, max 26)
NUM_PLAYERS = 2          # Number of players (2 to 5)

# ------------------------------
# Constants and Validation
# ------------------------------
MAX_COLS = 26
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= MAX_COLS):
    print(f"Error: COLS must be between 1 and {MAX_COLS}.")
    sys.exit(1)

# ------------------------------
# Board Utilities
# ------------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Linux/Unix per assignment
    os.system('clear')

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)
    # Top border
    print("+" + ("---+" * cols))

    # Rows (from top to bottom)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))

def column_index_from_input(inp, cols):
    inp = inp.strip().upper()
    if len(inp) != 1:
        return None
    if inp < "A" or inp >= chr(ord("A") + cols):
        return None
    return ord(inp) - ord("A")

def get_valid_column_input(current_player_symbol, cols):
    while True:
        try:
            user_inp = input(f"Player {current_player_symbol}, please enter a column: ").strip()
        except EOFError:
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        idx = column_index_from_input(user_inp, cols)
        if idx is not None:
            return idx
        # Invalid inputs do not lose turn; reprompt
        print("Invalid input. Please enter an uppercase letter within the board range.")

def drop_checker(board, col, symbol):
    """
    Attempts to drop 'symbol' into column 'col'.
    Returns:
      (True, (row, col)) if placed,
      (False, None) if column is full.
    """
    rows = len(board)
    # From bottom up, find first empty
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True, (r, col)
    return False, None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_winner(board, last_pos, symbol):
    """
    Check if placing at last_pos (row, col) for 'symbol' created a win.
    If last_pos is None (e.g., lost turn due to full column), return False.
    """
    if last_pos is None:
        return False

    rows, cols = len(board), len(board[0])
    r0, c0 = last_pos

    # Directions: (dr, dc). We will count both ways and subtract 1 to avoid double-counting the origin.
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # include the last placed checker
        # Forward
        r, c = r0 + dr, c0 + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Backward
        r, c = r0 - dr, c0 - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no spaces left in top row (or anywhere)
    for row in board:
        if " " in row:
            return False
    return True

# ------------------------------
# Game Flow
# ------------------------------
def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial board
    print_board(board)

    # Main game loop
    while True:
        current_symbol = players[current_player_idx]

        # Prompt for input (re-prompt until valid letter within range)
        col = get_valid_column_input(current_symbol, COLS)

        # Try to drop checker
        placed, last_pos = drop_checker(board, col, current_symbol)
        # Always print updated board (clear + print) after an attempt
        print_board(board)

        if not placed:
            # Column full: turn is invalid and player loses the turn
            # No placement -> no win check. Move to next player.
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_symbol} loses the turn.")
            # Proceed to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Before next prompt, check draw (board might be full)
            if is_draw(board):
                print("The game is a draw.")
                break
            continue

        # After a successful placement, check for win
        if check_winner(board, last_pos, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
