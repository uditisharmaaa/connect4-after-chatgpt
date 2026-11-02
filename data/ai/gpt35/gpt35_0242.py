import os
import random

# Constants for the game
ROWS = 6          # Number of rows on the board
COLUMNS = 7       # Number of columns on the board (max 26)
NUM_PLAYERS = 2   # Number of players (between 2 and 5)
WIN_LENGTH = 4    # Number of checkers in a row needed to win

# Player checkers symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """Create and return an empty board initialized with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and grid lines."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    # Print the board rows with +---+ separator
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))


def get_column_index(input_str, max_columns):
    """
    Convert user input letter to column index.
    Return -1 if invalid.
    """
    if len(input_str) != 1:
        return -1
    col = input_str.upper()
    if 'A' <= col <= chr(ord('A') + max_columns - 1):
        return ord(col) - ord('A')
    return -1


def is_column_full(board, col):
    """Return True if the given column is full, False otherwise."""
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place the checker in the given column at the lowest available row.
    Returns True if placed successfully, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_winner(board, checker):
    """
    Check the entire board if the given checker has 4 in a row:
    horizontally, vertically or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-right
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-left
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def board_full(board):
    """Return True if the board is completely filled, False otherwise."""
    return all(cell != " " for row in board for cell in row)


def get_valid_input(player, board):
    """
    Prompt the player to enter a column letter for their move.
    Validate input until a valid and playable column is chosen.
    Returns the 0-based column index.
    """
    max_columns = len(board[0])
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip()
        col = get_column_index(user_input, max_columns)
        if col == -1:
            # Invalid input
            continue
        if not is_column_full(board, col):
            return col
        else:
            # Column full, turn is lost as per assignment instructions
            print(f"Column {user_input.upper()} is full. You lose your turn.")
            return None


def main():
    # Initialize game state
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_index]
        col = get_valid_input(current_checker, board)

        # If player lost the turn because column is full
        if col is None:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place the checker in the chosen column
        placed = place_checker(board, col, current_checker)
        # This should always be True here due to validation,
        # but we keep check for safety.
        if not placed:
            # Column full (should not happen due to validation)
            print(f"Column {chr(ord('A') + col)} is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
