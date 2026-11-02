import os
import random
import string
import sys

# ========= Configuration (can be changed for testing; submission requires these values) =========
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
WIN_LENGTH = 4  # Always 4 per assignment

# Checker order for up to 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
# ===============================================================================================


def clear_screen():
    # Clear the terminal screen (Linux/Unix, macOS); on Windows 'clear' usually isn't available.
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers A.. up to columns
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(headers)
    print(sep)
    for r in range(rows):
        row_cells = "|".join(f" {board[r][c]} " for c in range(cols))
        print(f"|{row_cells}|")
        print(sep)


def get_column_index_from_input(user_input, cols):
    """
    Validate and convert the user input to a column index.
    Returns an integer index if valid, otherwise returns None.
    """
    if not user_input:
        return None
    s = user_input.strip()
    if len(s) != 1:
        return None
    ch = s.upper()
    if ch < 'A' or ch > 'Z':
        return None
    idx = ord(ch) - ord('A')
    if idx < 0 or idx >= cols:
        return None
    return idx


def drop_checker(board, col_idx, checker):
    """
    Attempt to drop `checker` into column col_idx.
    Returns:
      (row_idx, col_idx) if placement succeeded
      None if the column is full
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return (r, col_idx)
    return None


def check_winner(board, last_row, last_col, win_len=WIN_LENGTH):
    """
    Check if placing at (last_row, last_col) created a winning line of length win_len.
    Only needs to check lines through the last move.
    """
    target = board[last_row][last_col]
    if target == " ":
        return False

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include the last placed checker

        # check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == target:
            count += 1
            r += dr
            c += dc

        # check the opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == target:
            count += 1
            r -= dr
            c -= dc

        if count >= win_len:
            return True

    return False


def is_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def select_starting_player(num_players):
    return random.randrange(num_players)


def main():
    # Validations for configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
        sys.exit(1)
    if COLUMNS < 1 or COLUMNS > 26:
        print("COLUMNS must be between 1 and 26.", file=sys.stderr)
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.", file=sys.stderr)
        sys.exit(1)

    # Prepare players and board
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)

    current_player_idx = select_starting_player(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Read and validate user input (reprompt until valid letter within board)
        col_idx = None
        while col_idx is None:
            try:
                user_input = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted.")
                return
            col_idx = get_column_index_from_input(user_input, COLUMNS)
            if col_idx is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
                print(f"Player {current_checker}, please enter a column:")

        # Try to place checker; if column full, player loses turn
        placement = drop_checker(board, col_idx, current_checker)
        if placement is None:
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col_idx]} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successful placement
        last_row, last_col = placement

        # Update screen
        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, last_row, last_col, WIN_LENGTH):
            print(f"Player {current_checker} won!")
            return

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
