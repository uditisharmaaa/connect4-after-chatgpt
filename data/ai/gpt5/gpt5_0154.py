import os
import random
import sys

# Constants (you can change these for different dimensions/players)
ROWS = 6
COLS = 7  # Max 26 (A-Z)
PLAYER_COUNT = 2  # Between 2 and 5 players

# Checkers assigned in order
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:PLAYER_COUNT]

# Ensure constraints are met
if PLAYER_COUNT < 2 or PLAYER_COUNT > 5:
    print("PLAYER_COUNT must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)


def clear_screen():
    """
    Clears the terminal screen. The assignment requests using 'clear'.
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Creates a 2D board initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_letters(cols):
    """
    Returns a list of column labels from 'A' to the appropriate letter.
    """
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    """
    Prints the Connect 4 board with column labels and grid lines.
    """
    rows = len(board)
    cols = len(board[0])

    letters = column_letters(cols)
    # Header with column letters
    print("  " + "   ".join(letters))
    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    # Bottom border
    print(border)


def lowest_empty_row(board, col):
    """
    Returns the lowest available row index in the specified column.
    If the column is full, returns None.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def is_draw(board):
    """
    Checks if the board is full (no spaces left).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def check_win(board, symbol):
    """
    Checks whether the given symbol has 4 in a row horizontally,
    vertically, or diagonally on the board.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r][c + 1] == symbol and
                board[r][c + 2] == symbol and
                board[r][c + 3] == symbol):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == symbol and
                board[r + 1][c] == symbol and
                board[r + 2][c] == symbol and
                board[r + 3][c] == symbol):
                return True

    # Diagonal down-right check
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r + 1][c + 1] == symbol and
                board[r + 2][c + 2] == symbol and
                board[r + 3][c + 3] == symbol):
                return True

    # Diagonal up-right check
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r - 1][c + 1] == symbol and
                board[r - 2][c + 2] == symbol and
                board[r - 3][c + 3] == symbol):
                return True

    return False


def get_valid_column_input(cols):
    """
    Prompts the user for a valid column input (single uppercase letter within range).
    Re-prompts until a valid input is provided.
    Returns the zero-based column index.
    """
    letters = column_letters(cols)
    min_letter = letters[0]
    max_letter = letters[-1]
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter between {min_letter} and {max_letter}:")
            continue
        ch = user_input[0]
        if ch < min_letter or ch > max_letter:
            print(f"Invalid input. Please enter a letter between {min_letter} and {max_letter}:")
            continue
        return ord(ch) - ord('A')


def main():
    # Initialize game
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_player_idx = random.randrange(len(PLAYERS))

    # Initial screen
    clear_screen()
    print_board(board)
    # Main game loop
    while True:
        player_symbol = PLAYERS[current_player_idx]
        print(f"Player {player_symbol}, please enter a column:")

        # Get a valid column letter input
        col = get_valid_column_input(COLS)

        # Try to place the checker in the chosen column
        row = lowest_empty_row(board, col)
        if row is None:
            # Column full: turn is invalid and the player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % len(PLAYERS)
            # Check draw even though no move was made (unlikely to change)
            if is_draw(board):
                print("It's a draw!")
                break
            continue

        # Place the checker
        board[row][col] = player_symbol

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(PLAYERS)


if __name__ == "__main__":
    main()
