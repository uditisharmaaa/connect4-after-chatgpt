import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7           # Max 26 (A-Z)
PLAYER_COUNT = 2   # Supported: 2..5

# Tokens in order for up to 5 players
TOKENS = ["X", "O", "V", "H", "M"]


# =========================
# Validation of configuration
# =========================
def validate_config():
    if not (2 <= PLAYER_COUNT <= 5):
        raise ValueError("PLAYER_COUNT must be between 2 and 5.")
    if not (1 <= ROWS):
        raise ValueError("ROWS must be positive.")
    if not (1 <= COLS <= 26):
        raise ValueError("COLS must be between 1 and 26 (A-Z).")


# =========================
# Board creation and printing
# =========================
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # Requirement specifies using 'clear'
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
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


# =========================
# Input handling
# =========================
def get_valid_column_input(cols, current_token):
    # Keep asking until valid letter within board range
    while True:
        try:
            user_input = input(f"Player {current_token}, please enter a column: ")
        except EOFError:
            # Graceful exit on EOF
            print("\nInput ended. Exiting game.")
            sys.exit(0)

        if not user_input:
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue

        user_input = user_input.strip()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter (A-Z).")
            continue

        letter = user_input.upper()
        idx = ord(letter) - ord('A')
        if 0 <= idx < cols:
            return idx
        else:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")


# =========================
# Game mechanics
# =========================
def drop_checker(board, col, token):
    """
    Drops the token into the specified column.
    Returns the (row, col) where the token was placed.
    If the column is full, returns None.
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None


def check_win(board, last_row, last_col, token):
    """
    Check 4 in a row in all directions from the last placed token.
    Directions: horizontal, vertical, diag-down-right, diag-up-right
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include last placed
        # forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False


def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# =========================
# Main game loop
# =========================
def play_game(rows, cols, player_count):
    validate_config()
    board = create_board(rows, cols)
    players = TOKENS[:player_count]

    # Randomly select first player
    current_player_idx = random.randrange(player_count)

    # Show initial board
    print_board(board)

    while True:
        current_token = players[current_player_idx]

        # Prompt for input (validated)
        col = get_valid_column_input(cols, current_token)

        # Attempt to drop checker
        placement = drop_checker(board, col, current_token)

        if placement is None:
            # Column is full, player loses turn
            print_board(board)
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_token} loses the turn.")
            # Next player
            current_player_idx = (current_player_idx + 1) % player_count
            continue

        # Successful placement: check for win/draw
        last_row, last_col = placement
        print_board(board)

        if check_win(board, last_row, last_col, current_token):
            print(f"Player {current_token} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % player_count


if __name__ == "__main__":
    play_game(ROWS, COLS, PLAYER_COUNT)
