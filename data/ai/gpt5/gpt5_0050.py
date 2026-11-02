import os
import random
import sys

# Constants (as required by the assignment)
ROWS = 6                 # Number of rows in the board (height)
COLS = 7                 # Number of columns in the board (width), max 26
NUM_PLAYERS = 2          # Number of players: between 2 and 5 inclusive

# Allowed checkers for up to 5 players, in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Safety checks for constants
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")


def clear_screen():
    """
    Clear the terminal screen. Required to use 'clear' for Unix/Linux as per assignment.
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Create a game board with given dimensions, initialized with single-space strings.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(n):
    """
    Return list of column labels 'A', 'B', ..., up to n columns (max 26).
    """
    return [chr(ord('A') + i) for i in range(n)]


def print_board(board):
    """
    Print the game board in the specified format with column labels at the top.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column labels
    print("  " + "   ".join(labels))

    # Separator line
    sep = "+" + ("---+" * cols)

    # Each row of the board
    for r in range(rows):
        print(sep)
        row_str = ""
        for c in range(cols):
            cell = board[r][c]
            row_str += "|" + cell.center(3)
        row_str += "|"
        print(row_str)
    print(sep)


def is_valid_column_input(user_input, valid_labels):
    """
    Validate that the input is a single letter corresponding to an available column label.
    """
    if not user_input or len(user_input) != 1:
        return False
    return user_input in valid_labels


def get_player_input(current_checker, valid_labels):
    """
    Prompt the current player for a column label. Keep asking until a valid label is entered.
    Invalid inputs (non-letters, out-of-range) do not cost a turn.
    """
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting game.")
            sys.exit(0)

        if is_valid_column_input(user_input, valid_labels):
            return user_input
        else:
            print("Invalid input. Please enter a valid column letter.")


def col_index_from_label(label):
    """
    Convert a column label (e.g., 'A') to a zero-based column index.
    """
    return ord(label) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Place the checker in the specified column at the lowest available row.
    Returns the (row, col) position if placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row and move upwards to find the first empty slot
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return (r, col_idx)
    return None  # Column is full


def check_win(board, checker):
    """
    Check if the given checker has 4 in a row horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Horizontal to the right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (-1, 1),  # Diagonal up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    """
    Check if the board is full (draw).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    labels = column_labels(COLS)

    # Choose a random starting player
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_idx]
        # Ask for valid column letter input
        col_label = get_player_input(current_checker, labels)
        col_idx = col_index_from_label(col_label)

        # Attempt to place; if column full, player loses the turn
        pos = place_checker(board, col_idx, current_checker)

        # Clear and print board after the action/attempt as per requirement
        clear_screen()
        print_board(board)

        if pos is None:
            # Column was full; turn is invalid and player loses the turn
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) over % NUM_PLAYERS
            continue

        # Successful placement; check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
