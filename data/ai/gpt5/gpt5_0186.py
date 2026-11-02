import os
import random
import sys

# ===========================
# Configuration (changeable)
# ===========================
ROWS = 6
COLUMNS = 7        # Max 26 columns (A..Z)
NUM_PLAYERS = 2    # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # In order

# ===========================
# Validation of configuration
# ===========================
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLUMNS > 26 or COLUMNS < 1:
    raise ValueError("COLUMNS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]

# ===========================
# Utility functions
# ===========================
def clear_screen():
    # Per assignment: use 'clear' (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    # Initialize board with spaces " "
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(n):
    # Returns list of column labels: ["A", "B", ...]
    return [chr(ord('A') + i) for i in range(n)]

def print_board(board):
    # Prints the board in the required ASCII format
    labels = column_labels(len(board[0]))
    # Header labels
    print("  " + "   ".join(labels))
    # Horizontal separator
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(sep)
        # Each row
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def is_board_full(board):
    # Draw if no spaces left anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def drop_checker(board, col_index, checker):
    """
    Attempts to drop a checker into column col_index.
    Returns the (row_index, col_index) where it lands, or None if column is full.
    """
    rows = len(board)
    # Start from bottom (last row), go up to find first empty " "
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return (r, col_index)
    return None  # Column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    """
    Counts consecutive checkers equal to 'checker' starting from (start_r, start_c)
    moving by delta (dr, dc), excluding the starting cell.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, r, c, checker):
    """
    Checks if placing 'checker' at (r, c) results in a win (4 in a row).
    We count in both directions for each of the 4 lines: horizontal, vertical, 2 diagonals.
    """
    # Directions: (dr, dc) pairs where we will count both ways
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # include the placed checker itself
        total += count_in_direction(board, r, c, dr, dc, checker)
        total += count_in_direction(board, r, c, -dr, -dc, checker)
        if total >= 4:
            return True
    return False

def get_valid_column_input(valid_labels):
    """
    Prompt user until they enter a valid column label (single letter within valid_labels).
    Returns the uppercase label.
    """
    while True:
        try:
            user_input = input().strip()
        except EOFError:
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter:")
            continue
        ch = user_input.upper()
        if ch not in valid_labels:
            print("Invalid column. Please enter a valid column letter:")
            continue
        return ch

def game_loop():
    rows, cols = ROWS, COLUMNS
    board = create_board(rows, cols)
    labels = column_labels(cols)

    # Randomly select first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)
    # Game loop
    while True:
        current_checker = PLAYER_TOKENS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        col_label = get_valid_column_input(labels)
        col_index = ord(col_label) - ord('A')

        # Attempt to drop checker
        pos = drop_checker(board, col_index, current_checker)
        if pos is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
        else:
            # Check for win/draw after successful move
            r, c = pos
            clear_screen()
            print_board(board)
            # Check win
            if is_winning_move(board, r, c, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check draw
            if is_board_full(board):
                print("The game is a draw.")
                break

        # Advance to next player regardless (even if column was full)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

def main():
    game_loop()

if __name__ == "__main__":
    main()
