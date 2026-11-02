import os
import random
import string
import sys

# ----------------------------
# Configuration (you can change these constants for testing)
# ----------------------------
NUM_ROWS = 6
NUM_COLS = 7    # max 26
NUM_PLAYERS = 2  # between 2 and 5

# Player checker symbols in order (first NUM_PLAYERS are used)
CHECKERS = ["X", "O", "V", "H", "M"]

# ----------------------------
# Validations for configuration
# ----------------------------
if NUM_COLS < 1 or NUM_COLS > 26:
    print("Error: NUM_COLS must be between 1 and 26.")
    sys.exit(1)

if NUM_ROWS < 1:
    print("Error: NUM_ROWS must be at least 1.")
    sys.exit(1)

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if NUM_PLAYERS > len(CHECKERS):
    print("Error: Not enough checker symbols for the configured number of players.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:NUM_COLS])

# ----------------------------
# Board utilities
# ----------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Use 'clear' for Unix/Linux as required
    os.system('clear')

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column labels
    header = "  " + "   ".join(COL_LABELS[:cols])
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))

def is_valid_column_label(s):
    return len(s) == 1 and s in COL_LABELS

def column_index_from_label(label):
    return COL_LABELS.index(label)

def get_player_input(player_symbol):
    # Loop until we get a syntactically valid column label within the board
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        if not is_valid_column_label(user_input):
            print(f"Invalid column. Please enter a letter between A and {COL_LABELS[NUM_COLS - 1]}.")
            continue
        return column_index_from_label(user_input)

def drop_checker(board, col, checker):
    # Attempt to drop 'checker' into column 'col'.
    # Returns the row index where it landed, or None if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # column full

def check_winner(board, needed=4):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Directions to check: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            start = board[r][c]
            if start == " ":
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == start:
                    count += 1
                    if count == needed:
                        return start
                    rr += dr
                    cc += dc
    return None

def is_draw(board):
    # Draw if no spaces remain
    for row in board:
        if " " in row:
            return False
    return True

# ----------------------------
# Game loop
# ----------------------------
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    # Choose a random starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)

    while True:
        current_symbol = PLAYERS[current_player_idx]

        # Get a syntactically valid column (letter within bounds)
        col = get_player_input(current_symbol)

        # Try to drop the checker
        row_placed = drop_checker(board, col, current_symbol)

        # If column is full, the player loses the turn
        if row_placed is None:
            print_board(board)
            print(f"Column {COL_LABELS[col]} is full. Player {current_symbol} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, print the board
        print_board(board)

        # Check for winner
        winner = check_winner(board, needed=4)
        if winner is not None:
            print(f"Player {winner} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
