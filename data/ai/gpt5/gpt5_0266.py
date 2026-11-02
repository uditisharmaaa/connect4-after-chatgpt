import os
import random
import string
import sys

# ==========================
# Configuration (constants)
# ==========================
# Submission requires: 6 rows x 7 columns and 2 players enabled
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Supported range: 2..5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # In order for up to 5 players

# ==========================
# Utility and game functions
# ==========================

def clear_screen():
    """Clear the game screen in a Unix/Linux terminal."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board with given rows and columns initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column headers labeled A.. and grid separators."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers
    header_letters = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(header_letters))

    # Top border
    print('+' + '---+' * cols)

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {cell} ' for cell in row_cells) + '|')
        print('+' + '---+' * cols)


def is_valid_column_input(s, cols):
    """Validate if input s is a single uppercase letter within board columns."""
    if len(s) != 1:
        return False
    if s not in string.ascii_uppercase:
        return False
    index = ord(s) - ord('A')
    return 0 <= index < cols


def get_lowest_empty_row(board, col):
    """Return the lowest empty row index in given column, or None if column is full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def place_checker(board, col, token):
    """
    Place token in the lowest empty row of col.
    Return (row_index, col_index) if placed, else None if column is full.
    """
    r = get_lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return (r, col)


def in_bounds(r, c, rows, cols):
    """Check if row, col are within the bounds of the board."""
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    """
    Check whether the given token has 4 in a row on the board.
    Checks horizontally, vertically, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < 4 and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= 4:
                    return True
    return False


def board_full(board):
    """Return True if the board is completely filled (no spaces)."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def next_player_index(current, total):
    """Advance to next player index cyclically."""
    return (current + 1) % total


def setup_players(num_players):
    """Return list of player tokens for num_players, ensuring constraints."""
    if num_players < 2 or num_players > 5:
        print("NUM_PLAYERS must be between 2 and 5. Exiting.")
        sys.exit(1)
    return PLAYER_TOKENS[:num_players]


def prompt_for_column(current_token, cols):
    """
    Prompt user to enter a column letter.
    Ensures input validation: must be a valid uppercase column letter within range.
    Keeps asking until valid (but does not check for full column here).
    """
    while True:
        user_input = input(f"Player {current_token}, please enter a column: ").strip().upper()
        if is_valid_column_input(user_input, cols):
            return ord(user_input) - ord('A')
        # Invalid input; ask again without losing turn
        print("Invalid input. Please enter a valid column letter.")


def main():
    # Validate column constraint (A-Z)
    if COLS < 1 or COLS > 26:
        print("Number of columns must be between 1 and 26. Exiting.")
        sys.exit(1)

    # Initialize game state
    board = create_board(ROWS, COLS)
    players = setup_players(NUM_PLAYERS)
    current_player_idx = random.randrange(len(players))

    # Initial screen and board
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_token = players[current_player_idx]

        # Ask for column input (validated format/range)
        col = prompt_for_column(current_token, COLS)

        # Attempt to place checker
        placement = place_checker(board, col, current_token)

        # Clear and print board after the attempt (as per requirement)
        clear_screen()

        if placement is None:
            # Column full: invalid turn; player loses the turn
            print_board(board)
            print("Column is full. Turn lost.")
            # Advance to next player
            current_player_idx = next_player_index(current_player_idx, len(players))
            # Before continuing, check draw (board may already be full)
            if board_full(board):
                print("It's a draw!")
                break
            continue

        # Successful placement, print updated board
        print_board(board)

        # Check win condition for current player
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(players))


if __name__ == "__main__":
    main()
