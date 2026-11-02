import os
import random
import string
import sys

# ----------------------------
# Configuration (change if you like, but submission must use given values)
# ----------------------------
ROWS = 6
COLS = 7      # up to 26
NUM_PLAYERS = 2  # between 2 and 5

# Player checker symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]

# ----------------------------
# Validation of configuration
# ----------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]
LETTERS = list(string.ascii_uppercase[:COLS])

# ----------------------------
# Utility functions
# ----------------------------
def clear_screen():
    # Per assignment requirement:
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column labels
    header = "  " + "   ".join(LETTERS[:cols])
    sep = "+---" * cols + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def get_column_input(valid_letters, current_player_checker):
    while True:
        user_in = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        # Validate: must be a single valid letter within the board
        if len(user_in) != 1 or user_in not in valid_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        return valid_letters.index(user_in)

def place_checker(board, col, checker):
    """
    Attempts to place checker in the given column. Returns the (row, col) if placed,
    or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row and go upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return (r, col)
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_pos, checker):
    """
    Check for 4 in a row including last_pos in any direction.
    """
    if last_pos is None:
        return False
    rows = len(board)
    cols = len(board[0])
    r0, c0 = last_pos

    # Directions: horizontal, vertical, diag-down-right, diag-up-right
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]

    for dr, dc in directions:
        count = 1

        # Forward direction
        r, c = r0 + dr, c0 + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Backward direction
        r, c = r0 - dr, c0 - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

# ----------------------------
# Game loop
# ----------------------------
def main():
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_index = random.randrange(len(PLAYERS))

    # Initial screen
    clear_screen()
    print_board(board)

    # Game state
    last_move = None

    while True:
        current_checker = PLAYERS[current_player_index]

        # Prompt for input
        col = get_column_input(LETTERS, current_checker)

        # Attempt to place checker
        placed = place_checker(board, col, current_checker)

        # Clear screen and reprint board after attempted move
        clear_screen()

        if placed is None:
            # Column full: player loses the turn (no reprompt)
            print_board(board)
            print(f"Column {LETTERS[col]} is full. Player {current_checker} loses the turn.")
            # Next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
            continue

        last_move = placed

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, last_move, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
