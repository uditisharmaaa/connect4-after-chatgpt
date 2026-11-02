import os
import random
import string

# =======================
# Configuration constants
# =======================

# Board dimensions (ROWS x COLS). Submission requires 6x7.
ROWS = 6
COLS = 7  # Max 26
# Number of players (between 2 and 5). Submission requires 2.
NUM_PLAYERS = 2

# Checker symbols used in order for players 1..N
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of connected checkers needed to win (always 4)
CONNECT_N = 4

# =======================
# Utility and core logic
# =======================

def clear_console():
    # Clear console on Unix-like systems
    os.system('clear')


def create_board(rows, cols):
    # Create a 2D board (list of lists) initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Clear before printing the updated board
    clear_console()

    rows = len(board)
    cols = len(board[0]) if rows else 0

    # Header: column labels A..Z
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Top border
    print("+" + "---+" * cols)

    # Rows from top to bottom
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * cols)


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def drop_checker(board, col_index, checker):
    """
    Attempt to drop a checker into column col_index.
    Returns:
      - (True, row_index) on success
      - (False, None) if the column is full
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r
    return False, None


def check_direction(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers from start position in both directions of (dr, dc).
    Returns True if total in a line >= CONNECT_N.
    """
    rows = len(board)
    cols = len(board[0])

    count = 1  # include the starting piece

    # forward direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc

    # backward direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r -= dr
        c -= dc

    return count >= CONNECT_N


def check_win(board, last_r, last_c, checker):
    """
    Check for a win condition based on the last move.
    """
    # Directions: horizontal, vertical, diagonal down-right, diagonal up-right
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]
    for dr, dc in directions:
        if check_direction(board, last_r, last_c, dr, dc, checker):
            return True
    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_validated_input(cols):
    """
    Prompt the user until a valid column letter is provided.
    Returns uppercase letter A.. corresponding to a column index in range.
    """
    valid_letters = set(string.ascii_uppercase[:cols])
    while True:
        user_input = input().strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            print("Please enter a column:")
            continue
        letter = user_input.upper()
        if letter not in valid_letters:
            print("Invalid input. Please enter a valid column letter within the board.")
            print("Please enter a column:")
            continue
        return letter


def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5 inclusive.")
    if COLS < 1 or ROWS < 1:
        raise ValueError("Board dimensions must be positive.")
    if COLS > 26:
        raise ValueError("Maximum supported columns is 26 due to letter labeling.")
    if NUM_PLAYERS > len(CHECKERS):
        raise ValueError("Not enough checker symbols defined for the number of players.")

    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Show initial board before the game starts
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_index]

        # If board is already full (draw), stop
        if board_full(board):
            print("It's a draw!")
            break

        # Prompt current player
        print(f"Player {current_checker}, please enter a column:")

        # Validate input letter
        letter = get_validated_input(COLS)
        col_index = ord(letter) - ord('A')

        # Attempt to place the checker
        success, row_index = drop_checker(board, col_index, current_checker)

        # Print updated board after the turn attempt
        print_board(board)

        if success:
            # Check for win
            if check_win(board, row_index, col_index, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check for draw after a successful move
            if board_full(board):
                print("It's a draw!")
                break
        else:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {letter} is full. Player {current_checker} loses the turn.")

        # Alternate to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
