import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # Maximum allowed columns (based on letters A-Z)
PLAYERS = 2        # Number of players (between 2 and 5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure constants are within allowed values
assert 2 <= PLAYERS <= 5, "Number of players must be between 2 and 5"
assert COLUMNS <= MAX_COLUMNS, f"Number of columns cannot exceed {MAX_COLUMNS}"


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """Create and return the game board initialized with whitespace."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Print the Connect 4 board with column labels."""
    clear_screen()
    columns = len(board[0])
    # Print the column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    print(header)
    # Print the top border
    print("+" + "---+" * columns)
    # Print each row with vertical separators
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * columns)


def col_letter_to_index(letter):
    """Convert uppercase column letter to board index."""
    return ord(letter) - ord('A')


def is_valid_column_input(user_input, columns):
    """Check if the user's input is a valid column letter."""
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col = user_input.upper()
    if ord(col) < ord('A') or ord(col) >= ord('A') + columns:
        return False
    return True


def place_checker(board, col_idx, checker):
    """
    Place a checker in the chosen column, falling to the lowest available space.
    Return True if placed successfully, False if the column is full.
    """
    # Start checking from bottom row up
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False  # Column full


def check_four_in_a_row(checkers_line, checker):
    """
    Helper function to check if there are four consecutive same checkers.
    Returns True if found, else False.
    """
    count = 0
    for c in checkers_line:
        if c == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
    return False


def check_win(board, checker):
    """Check the entire board for a win condition for the given checker."""

    rows = len(board)
    columns = len(board[0])

    # Check horizontal wins
    for row in range(rows):
        row_line = board[row]
        if check_four_in_a_row(row_line, checker):
            return True

    # Check vertical wins
    for col in range(columns):
        col_line = [board[row][col] for row in range(rows)]
        if check_four_in_a_row(col_line, checker):
            return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(rows - WIN_CONDITION + 1):
        for col in range(columns - WIN_CONDITION + 1):
            diagonal = [board[row + i][col + i] for i in range(WIN_CONDITION)]
            if all(c == checker for c in diagonal):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(WIN_CONDITION - 1, rows):
        for col in range(columns - WIN_CONDITION + 1):
            diagonal = [board[row - i][col + i] for i in range(WIN_CONDITION)]
            if all(c == checker for c in diagonal):
                return True

    return False


def check_draw(board):
    """Return True if board is full (draw), else False."""
    # If any space is empty, not draw yet
    for row in board:
        if " " in row:
            return False
    return True


def get_player_input(player_checker, columns):
    """Prompt the current player for input and validate."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_input(user_input, columns):
            # Invalid format or out of range
            continue
        col_idx = col_letter_to_index(user_input)
        return col_idx


def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)

    # Select a random starting player index
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    # Game loop
    while True:
        checker = CHECKERS[current_player]

        # Get user input and validate
        col_idx = get_player_input(checker, COLUMNS)

        # Attempt to place the checker; if column full, player loses turn
        placed = place_checker(board, col_idx, checker)
        if not placed:
            # Inform that column is full and player loses turn
            # But per assignment: "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn."
            # So continue to next player without retrying.
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS


if __name__ == "__main__":
    main()
