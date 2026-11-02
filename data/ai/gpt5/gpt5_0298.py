import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6          # Number of rows on the board
COLS = 7          # Number of columns on the board (max 26)
NUM_PLAYERS = 2   # Number of players (between 2 and 5)

# Player checkers in play order. Use the first NUM_PLAYERS of these.
TOKENS = ["X", "O", "V", "H", "M"]

# =========================
# Validation of configuration
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS > 26 or COLS < 1:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = TOKENS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])  # Column labels 'A'.. up to COLS


# =========================
# Board creation and printing
# =========================
def create_board(rows, cols):
    """
    Create a board initialized with spaces.
    The board is a list of lists, indexed as board[row][col],
    with row 0 at the top and row rows-1 at the bottom.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """
    Clear the terminal screen. Works on Linux/Unix as required by the assignment.
    """
    os.system('clear')


def print_board(board):
    """
    Print the board with column labels and grid lines, matching the example format.
    """
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column labels
    header = "  " + "   ".join(COL_LABELS[:cols])
    print(header)

    # For each row, print separator and content
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


# =========================
# Game mechanics
# =========================
def is_valid_column_input(user_input):
    """
    Validate that user_input is exactly one uppercase letter within the board bounds.
    Returns the column index if valid, otherwise returns None.
    """
    if len(user_input) != 1:
        return None
    if user_input not in COL_LABELS:
        return None
    return COL_LABELS.index(user_input)


def get_column_choice(current_token):
    """
    Prompt the current player until a syntactically valid column letter is entered.
    Note:
      - Invalid inputs (non-letters, out-of-range letters) must be re-entered (turn not lost).
      - A valid but full column will be handled by the caller (turn lost).
    Returns the chosen column index.
    """
    while True:
        choice = input(f"Player {current_token}, please enter a column: ").strip().upper()
        col_idx = is_valid_column_input(choice)
        if col_idx is not None:
            return col_idx
        else:
            print("Invalid input. Please enter a valid column letter shown at the top of the board.")


def place_checker(board, col, token):
    """
    Attempt to place the checker 'token' into column 'col'.
    The checker should occupy the lowest available space in the column.
    Returns (row_index, col) if successfully placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row upwards to find first empty cell
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None  # Column is full


def count_in_direction(board, start_r, start_c, dr, dc, token):
    """
    Count consecutive tokens starting just beyond the start cell in the direction (dr, dc),
    stopping when out of bounds or a different token is encountered.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_winner(board, last_move, token):
    """
    Check whether placing 'token' at 'last_move' created a winning line of 4.
    last_move is a tuple (row, col).
    Checks horizontal, vertical, and both diagonals.
    """
    if last_move is None:
        return False
    r, c = last_move

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        # Count contiguous tokens in both directions from the last move
        total = 1  # include last placed token
        total += count_in_direction(board, r, c, dr, dc, token)
        total += count_in_direction(board, r, c, -dr, -dc, token)
        if total >= 4:
            return True
    return False


def is_draw(board):
    """
    The game is a draw if there are no empty spaces in the top row (i.e., no more moves).
    """
    return all(cell != " " for cell in board[0])


# =========================
# Main game loop
# =========================
def main():
    board = create_board(ROWS, COLS)
    # Randomly select which player starts
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display before any moves
    print_board(board)

    while True:
        current_token = PLAYERS[current_player_idx]
        # Prompt for a valid column letter
        col_idx = get_column_choice(current_token)

        # Attempt to place the checker
        placed = place_checker(board, col_idx, current_token)

        if placed is None:
            # Valid input but column is full: turn is invalid and the player loses the turn.
            print(f"Column {COL_LABELS[col_idx]} is full. Player {current_token} loses the turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Print updated (unchanged) board for next player's turn
            print_board(board)
            continue

        # After a valid move, print the updated board
        print_board(board)

        # Check for a win
        if check_winner(board, placed, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game over


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        print("\nGame interrupted.")
