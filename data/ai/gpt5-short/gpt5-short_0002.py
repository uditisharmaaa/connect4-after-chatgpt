import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must match COLS
EMPTY = " "

# Tokens used by players in order. Only the first NUM_PLAYERS will be used.
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

# Set how many players will play: 2 to 5
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5


# =========================
# Board utilities
# =========================
def create_board(rows=ROWS, cols=COLS):
    """Create an empty board (list of lists) filled with EMPTY."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """Clear the terminal screen. Uses 'clear' as requested."""
    os.system("clear")


def print_board(board, players):
    """Pretty-print the current board state with column labels and player legend."""
    # Column header
    print("  " + " ".join(COLUMN_LABELS[:len(board[0])]))
    # Board rows (top row first)
    for r in range(len(board)):
        print("| " + " ".join(board[r]) + " |")
    # Footer line
    print("  " + "-".join("-" for _ in range(len(board[0]))))
    # Legend for active players
    legend = "  Players: " + " ".join(players)
    print(legend)


def is_valid_column_input(s):
    """Return True if input s is a single letter that maps to a column label."""
    if not s or len(s) != 1:
        return False
    s = s.upper()
    return s in COLUMN_LABELS[:COLS]


def col_from_input(s):
    """Convert a column letter (A-G) to zero-based column index."""
    return COLUMN_LABELS.index(s.upper())


def get_next_open_row(board, col):
    """
    Return the row index where the token would land in the given column,
    or None if the column is full.
    """
    # Start from bottom row to top; find the first EMPTY slot
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def drop_token(board, row, col, token):
    """Place the token at (row, col) on the board."""
    board[row][col] = token


# =========================
# Win/Draw detection
# =========================
def check_win(board, row, col, token):
    """
    Check whether placing 'token' at (row, col) results in a connect-4.
    We check 4 directions:
      - Horizontal (0, ±1)
      - Vertical (±1, 0)
      - Diagonal down-right / up-left (±1, ±1)
      - Diagonal up-right / down-left (±1, ∓1)
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the newly placed token

        # Check in the positive direction (dr, dc)
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction (-dr, -dc)
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def check_draw(board):
    """Return True if the board is full (no EMPTY cells in top row)."""
    # If any cell in the top row is EMPTY, the board is not full
    return all(cell != EMPTY for cell in board[0])


# =========================
# Input handling
# =========================
def prompt_for_move(current_token):
    """
    Prompt the current player for a column letter and validate it.
    Continues prompting until a valid, non-full column is chosen.
    """
    while True:
        user_input = input(f"Player {current_token}, choose a column ({COLUMN_LABELS[:COLS]}): ").strip()

        # Validate basic format
        if not is_valid_column_input(user_input):
            print(f"Invalid input. Please enter a single letter from {COLUMN_LABELS[:COLS]}.")
            continue

        col = col_from_input(user_input)
        row = get_next_open_row(board, col)
        if row is None:
            print("That column is full. Please choose a different column.")
            continue

        return row, col


# =========================
# Game loop
# =========================
if __name__ == "__main__":
    # Validate the number of players
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    # Active player tokens (slice of PLAYER_TOKENS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]

    # Initialize game state
    board = create_board()
    current_index = random.randrange(NUM_PLAYERS)  # Random first player

    # Main game loop
    while True:
        clear_screen()
        print_board(board, players)

        current_token = players[current_index]
        row, col = prompt_for_move(current_token)

        # Place the token
        drop_token(board, row, col, current_token)

        # Check for a win
        if check_win(board, row, col, current_token):
            clear_screen()
            print_board(board, players)
            print(f"Player {current_token} wins! Congratulations!")
            break

        # Check for a draw
        if check_draw(board):
            clear_screen()
            print_board(board, players)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

    print("Game over.")
