import os
import random
import string
import sys

# ----- CONSTANTS -----
ROWS = 6
COLS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players supported
NUM_PLAYERS = 2  # Adjust between 2 and 5
WIN_LENGTH = 4
MAX_COLS = 26  # Limit from assignment text

assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
assert COLS <= MAX_COLS, "Max columns exceeded"

# ----- HELPER FUNCTIONS -----
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Print separator
    print("+" + "---+" * cols)
    # Print each row from top to bottom
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Return a set of column indices (0-indexed) which are not full."""
    return {c for c in range(len(board[0])) if board[0][c] == " "}

def input_column(valid_columns, cols):
    valid_letters = [string.ascii_uppercase[c] for c in valid_columns]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:cols]:
            print("Invalid input! Please enter a valid column letter (e.g., A-G).")
            continue
        col_idx = ord(col_input) - ord('A')
        if col_idx not in valid_columns:
            print(f"Column {col_input} is full or unavailable. Please choose another column.")
            continue
        return col_idx

def drop_checker(board, col_idx, token):
    """Drops the checker into the specified column. Returns row index or None if column full."""
    for row_idx in reversed(range(len(board))):  # Start from bottom row
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = token
            return row_idx
    return None  # This should never happen if input is validated

def check_winner(board, row_idx, col_idx, token):
    """Check all directions for WIN_LENGTH in a row."""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1  # Count the checker just placed
        # Check in the positive direction
        r, c = row_idx + dr, col_idx + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row_idx - dr, col_idx - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    return all(cell != " " for cell in board[0])

# ----- MAIN GAME LOOP -----
def main():
    board = create_board(ROWS, COLS)
    player_tokens = PLAYER_TOKENS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        token = player_tokens[current_player]
        valid_columns = get_valid_columns(board)

        if not valid_columns:
            print("The game is a draw! No player has won.")
            break

        print(f"Player {token},", end=" ")
        col_idx = input_column(valid_columns, COLS)
        row_idx = drop_checker(board, col_idx, token)
        clear_screen()
        print_board(board)

        if check_winner(board, row_idx, col_idx, token):
            print(f"Player {token} won!")
            break

        if is_draw(board):
            print("The game is a draw! No player has won.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
