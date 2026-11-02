import os
import random
import string
import sys

# Constants (Submission requires 6x7 board and 2 players)
ROWS = 6
COLS = 7  # Max 26 columns supported
NUM_PLAYERS = 2  # Supported: 2 to 5 players

# Player symbols in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYERS = CHECKERS[:NUM_PLAYERS]

# Game constants
WIN_LENGTH = 4
EMPTY_CELL = " "


def clear_screen():
    # Per assignment: use 'clear' (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels are A, B, C, ... up to 26 columns
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with labels (two leading spaces, three spaces between labels)
    header = "  " + "   ".join(labels)
    print(header)

    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(border)
        # Row cells
        row_parts = []
        for c in range(cols):
            row_parts.append(f" {board[r][c]} ")
        print("|" + "|".join(row_parts) + "|")
    # Bottom border
    print(border)


def get_valid_column_input(cols, current_player_symbol, board, error_message=None):
    """
    Repeatedly prompt the user for a valid column letter within range.
    Does not allow losing the turn for invalid inputs (keeps asking).
    Returns the valid column index (0-based).
    """
    labels = column_labels(cols)
    label_set = set(labels)

    while True:
        clear_screen()
        print_board(board)
        if error_message:
            print(error_message)
        print(f"Player {current_player_symbol}, please enter a column:", end=" ")
        user_input = input().strip().upper()

        # Validate: must be a single letter within the labels
        if len(user_input) != 1 or user_input not in label_set:
            error_message = "Invalid input. Please enter a valid column letter."
            continue

        # Valid letter; return index
        return labels.index(user_input)


def place_checker(board, col, symbol):
    """
    Place the symbol in the lowest available row in the given column.
    Returns True if placed, False if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            board[r][col] = symbol
            return True
    return False


def check_direction(board, start_row, start_col, delta_row, delta_col, symbol):
    """
    Count consecutive symbols in a given direction starting from (start_row, start_col).
    Returns the count of consecutive symbols including the starting cell.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_row, start_col
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += delta_row
        c += delta_col
    return count


def check_win(board, symbol):
    """
    Check if the given symbol has a winning sequence of WIN_LENGTH
    horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue

            # Check in four primary directions: right, down, down-right, down-left
            # To optimize, only start checks where enough space remains.

            # Horizontal (right)
            if c + WIN_LENGTH - 1 < cols:
                if all(board[r][c + k] == symbol for k in range(WIN_LENGTH)):
                    return True

            # Vertical (down)
            if r + WIN_LENGTH - 1 < rows:
                if all(board[r + k][c] == symbol for k in range(WIN_LENGTH)):
                    return True

            # Diagonal (down-right)
            if r + WIN_LENGTH - 1 < rows and c + WIN_LENGTH - 1 < cols:
                if all(board[r + k][c + k] == symbol for k in range(WIN_LENGTH)):
                    return True

            # Diagonal (down-left)
            if r + WIN_LENGTH - 1 < rows and c - WIN_LENGTH + 1 >= 0:
                if all(board[r + k][c - k] == symbol for k in range(WIN_LENGTH)):
                    return True

    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY_CELL:
                return False
    return True


def prompt_continue(message, board):
    clear_screen()
    print_board(board)
    print(message)
    print("Press Enter to continue...", end="")
    try:
        input()
    except EOFError:
        # Non-interactive environment safety
        pass


def main():
    # Validate constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLS <= 26):
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)

    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Show initial board before game starts
    clear_screen()
    print_board(board)
    print(f"Player {PLAYERS[current_player_index]} starts. Press Enter to begin...", end="")
    try:
        input()
    except EOFError:
        pass

    # Game loop
    while True:
        current_symbol = PLAYERS[current_player_index]

        # Ask for input until a valid column letter is given
        col = get_valid_column_input(COLS, current_symbol, board)

        # Attempt to place the checker
        if not place_checker(board, col, current_symbol):
            # Column full: turn is invalid and the player loses the turn
            message = f"Column {column_labels(COLS)[col]} is full. Player {current_symbol} loses the turn."
            prompt_continue(message, board)
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Continue game
            # Check for draw even if no placement? Typically not needed, but do a safe check:
            if board_full(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break
            continue

        # After successful placement, show updated board
        clear_screen()
        print_board(board)

        # Check for a win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for a draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

        # Prompt next player line as in example
        print(f"Player {PLAYERS[current_player_index]}, please enter a column:", end=" ")
        # We don't actually take input here; the next loop iteration will reprompt with a fresh screen.
        try:
            # Read and discard to allow a smoother flow when run interactively
            # Comment out the next line if undesired; keeping it improves alignment with example flow.
            pass
        except EOFError:
            pass


if __name__ == "__main__":
    main()
