import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                 # Number of rows (default for Connect 4 is 6)
COLS = 7                 # Number of columns (default for Connect 4 is 7). Max is 26 (A-Z)
NUM_PLAYERS = 2          # Number of players supported: 2 to 5
WIN_LENGTH = 4           # Number of connected checkers needed to win (always 4)

# Player checker symbols, in order. For N players, first N are used.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']


# =========================
# Utility and game helpers
# =========================

def create_board(rows, cols):
    """
    Create a board (list of lists) filled with spaces.
    board[r][c] where r in [0..rows-1], c in [0..cols-1]
    Top row is index 0, bottom row is index rows - 1.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """
    Clear the terminal screen (Linux/Unix: clear).
    """
    os.system('clear')


def print_board(board):
    """
    Clear the screen and print the board with column labels and borders.
    Matches the example formatting in the assignment.
    """
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal border for each row
    h_border = "+" + "+".join(["---"] * cols) + "+"

    # Print each row with separators
    for r in range(rows):
        print(h_border)
        row_cells = "|".join([f" {board[r][c]} " for c in range(cols)])
        print(f"|{row_cells}|")
    print(h_border)


def choose_start_player(num_players):
    """
    Randomly choose the index of the starting player [0..num_players-1].
    """
    return random.randint(0, num_players - 1)


def get_valid_column_input(cols):
    """
    Prompt the user until they provide a valid column letter (A..).
    Returns the 0-based column index for a valid input.
    This function only validates input format and range, not whether the column is full.
    """
    while True:
        user_input = input("Please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue

        # Accept both uppercase and lowercase, consider only the first character
        ch = user_input[0].upper()

        if ch < 'A' or ch > chr(ord('A') + cols - 1):
            print("Invalid column. Please enter a letter within the board range.")
            continue

        return ord(ch) - ord('A')


def place_checker(board, col, symbol):
    """
    Place the checker symbol in the lowest available row within the given column.
    Returns (row_index, col_index) if placed successfully.
    Returns None if the column is full (no placement).
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count the number of consecutive 'symbol' cells starting from (start_r, start_c),
    stepping by (dr, dc), including the starting cell if it matches.
    Stops on first mismatch or out-of-bounds.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, symbol):
    """
    Check if placing 'symbol' at (last_r, last_c) produced a win.
    We check in four direction pairs: horizontal, vertical, diag1, diag2.
    For each pair we count both ways and subtract 1 to avoid double-counting the starting cell.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right / up-left
        (1, -1),  # diagonal down-left / up-right
    ]
    for dr, dc in directions:
        total = (
            count_in_direction(board, last_r, last_c, dr, dc, symbol) +
            count_in_direction(board, last_r, last_c, -dr, -dc, symbol) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    """
    Check if the board is full (no spaces left).
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def validate_configuration(rows, cols, num_players):
    """
    Validate global configuration:
    - rows >= 1, cols between 1 and 26
    - num_players between 2 and 5
    - WIN_LENGTH remains 4 as per assignment
    """
    if rows < 1 or cols < 1:
        print("Error: Board dimensions must be positive.")
        return False
    if cols > 26:
        print("Error: Maximum supported columns is 26 (A-Z).")
        return False
    if num_players < 2 or num_players > 5:
        print("Error: Number of players must be between 2 and 5.")
        return False
    if WIN_LENGTH != 4:
        print("Error: WIN_LENGTH must be 4 per assignment.")
        return False
    return True


def main():
    # Validate configuration
    if not validate_configuration(ROWS, COLS, NUM_PLAYERS):
        sys.exit(1)

    # Select symbols for the number of players
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Initialize board
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = choose_start_player(NUM_PLAYERS)

    # Show initial board
    print_board(board)
    print(f"Player {symbols[current_player_idx]}, please enter a column:")

    # Game loop
    while True:
        # Prompt input for the current player
        col = get_valid_column_input(COLS)

        # Attempt to place the checker
        result = place_checker(board, col, symbols[current_player_idx])

        if result is None:
            # Column full: player loses their turn
            print_board(board)
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {symbols[current_player_idx]} loses the turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print(f"Player {symbols[current_player_idx]}, please enter a column:")
            continue

        last_r, last_c = result

        # After a successful placement, print updated board
        print_board(board)

        # Check for a win
        if check_win(board, last_r, last_c, symbols[current_player_idx]):
            print(f"Player {symbols[current_player_idx]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print(f"Player {symbols[current_player_idx]}, please enter a column:")


if __name__ == "__main__":
    main()
