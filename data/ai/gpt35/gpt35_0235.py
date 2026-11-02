import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WINNING_COUNT = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Set game configuration here
NUM_PLAYERS = 2        # Between MIN_PLAYERS and MAX_PLAYERS
NUM_ROWS = ROWS        # Number of rows (6 for assignment)
NUM_COLUMNS = COLUMNS  # Number of columns (7 for assignment)


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    """Create a board initialized with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Print the board with column headers as letters starting from A."""
    clear_screen()
    columns = len(board[0])
    rows = len(board)

    # Print column headers A, B, C...
    header_letters = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(header_letters))

    # Print the board
    line_sep = '+' + '---+' * columns
    for r in range(rows):
        print(line_sep)
        row_str = '|'
        for c in range(columns):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(line_sep)


def is_valid_column(input_str, columns):
    """Check if the input_str is a valid column letter within the board."""
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    return 'A' <= c < chr(ord('A') + columns)


def get_column_index(column_letter):
    """Convert column letter to 0-based index."""
    return ord(column_letter.upper()) - ord('A')


def place_checker(board, col, checker):
    """
    Place checker in the lowest available row in column col.
    Return True if placed successfully, False if column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_winner(board, checker):
    """Check if given checker has four in a row horizontally, vertically, or diagonally."""

    rows = len(board)
    cols = len(board[0])

    # Horizontal Check
    for r in range(rows):
        count = 0
        for c in range(cols):
            count = count + 1 if board[r][c] == checker else 0
            if count >= WINNING_COUNT:
                return True

    # Vertical Check
    for c in range(cols):
        count = 0
        for r in range(rows):
            count = count + 1 if board[r][c] == checker else 0
            if count >= WINNING_COUNT:
                return True

    # Diagonal Checks (left-top to right-bottom)
    for r in range(rows - WINNING_COUNT + 1):
        for c in range(cols - WINNING_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WINNING_COUNT)):
                return True

    # Diagonal Checks (left-bottom to right-top)
    for r in range(WINNING_COUNT - 1, rows):
        for c in range(cols - WINNING_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WINNING_COUNT)):
                return True

    return False


def board_full(board):
    """Return True if the board is full (no spaces left)."""
    return all(cell != " " for row in board for cell in row)


def main():
    # Validate configuration constants
    if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return

    if not (1 <= NUM_COLUMNS <= MAX_COLUMNS):
        print(f"Number of columns must be between 1 and {MAX_COLUMNS}.")
        return

    # Initialize board
    board = create_board(NUM_ROWS, NUM_COLUMNS)

    # Determine players and their checkers
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        input_prompt = f"Player {current_checker}, please enter a column: "

        while True:
            user_input = input(input_prompt).strip().upper()
            if not is_valid_column(user_input, NUM_COLUMNS):
                print(f"Invalid input! Please enter a letter between A and {chr(ord('A') + NUM_COLUMNS - 1)}.")
                continue

            col_idx = get_column_index(user_input)
            if place_checker(board, col_idx, current_checker):
                # Checker placed successfully
                break
            else:
                # Column full, player loses turn
                print(f"Column {user_input} is full. You lose your turn.")
                break

        # Check for win
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
