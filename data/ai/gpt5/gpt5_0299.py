import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7            # Max 26
NUM_PLAYERS = 2     # Between 2 and 5 inclusive

CHECKERS = ["X", "O", "V", "H", "M"]  # Player markers in order

# =========================
# Validation of constants
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

PLAYER_MARKERS = CHECKERS[:NUM_PLAYERS]

# =========================
# Utility functions
# =========================

def clear_screen():
    # For Unix/Linux as required by the assignment
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    header_letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(header_letters))
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * cols))

def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    ch = s.upper()
    if ch < 'A' or ch > chr(ord('A') + cols - 1):
        return False
    return True

def first_empty_row_in_column(board, col):
    # Return the bottom-most empty row index for given column, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def check_winner(board, last_row, last_col, marker):
    # Check 4 directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include last placed checker
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == marker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == marker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def is_draw(board):
    # Draw if no spaces left in the top row (or entire board)
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

# =========================
# Main game loop
# =========================

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)
    status_message = ""

    # Initial display before the game starts (as required)
    while True:
        clear_screen()
        print_board(board)
        if status_message:
            print(status_message)
            status_message = ""
        print(f"Player {PLAYER_MARKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        # Validate input: only reprompt on invalid input (bad chars or out of range)
        if not is_valid_column_input(user_input, COLS):
            status_message = "Invalid input. Please enter a valid column letter."
            continue

        col = ord(user_input) - ord('A')

        # Attempt to place checker; if column is full, player loses the turn
        target_row = first_empty_row_in_column(board, col)
        if target_row is None:
            # Turn is invalid and player loses the turn (do not re-prompt)
            status_message = f"Column {user_input} is full. Turn lost."
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place the checker
        marker = PLAYER_MARKERS[current_player]
        board[target_row][col] = marker

        # Check for win
        if check_winner(board, target_row, col, marker):
            clear_screen()
            print_board(board)
            print(f"Player {marker} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
