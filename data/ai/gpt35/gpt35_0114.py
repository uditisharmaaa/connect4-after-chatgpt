import os
import random

# Constants for the game configuration
ROWS = 6           # Number of rows on the board
COLUMNS = 7        # Number of columns on the board (max 26)
NUM_PLAYERS = 2    # Number of players (between 2 and 5)
WIN_STREAK = 4     # Number of checkers in a row required to win

# Players' checkers symbols in order
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates and returns an empty board (2D list) filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal with column labels and borders."""
    columns = len(board[0])
    rows = len(board)
    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    print(headers)
    # Print the top border line
    border_line = "+" + "---+" * columns
    for r in range(rows):
        print(border_line)
        row_str = "|"
        for c in range(columns):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(border_line)  # bottom border after the last row

def get_valid_column(player):
    """
    Prompts the current player to enter a valid column letter.
    Validates input: must be uppercase letter within columns range.
    Returns the zero-based index of the column.
    """
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip()
        if len(col_input) != 1:
            print("Invalid input! Please enter a single uppercase letter.")
            continue
        col_char = col_input.upper()
        if not ('A' <= col_char <= chr(ord('A') + COLUMNS - 1)):
            print(f"Invalid input! Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        col_idx = ord(col_char) - ord('A')
        return col_idx

def place_checker(board, col, checker):
    """
    Attempts to place the checker's piece in the given column.
    The checker falls to the lowest empty position in the column.
    Returns True if placement successful, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def is_winner(board, checker):
    """
    Checks if the given checker has 4 in a row horizontally,
    vertically, or diagonally anywhere on the board.
    Returns True if checker wins, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal streaks
    for r in range(rows):
        for c in range(cols - WIN_STREAK + 1):
            if all(board[r][c+i] == checker for i in range(WIN_STREAK)):
                return True

    # Check vertical streaks
    for c in range(cols):
        for r in range(rows - WIN_STREAK + 1):
            if all(board[r+i][c] == checker for i in range(WIN_STREAK)):
                return True

    # Check diagonal (down-right) streaks
    for r in range(rows - WIN_STREAK + 1):
        for c in range(cols - WIN_STREAK + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_STREAK)):
                return True

    # Check diagonal (up-right) streaks
    for r in range(WIN_STREAK - 1, rows):
        for c in range(cols - WIN_STREAK + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_STREAK)):
                return True

    return False

def is_draw(board):
    """
    Returns True if the board is completely full (no empty spaces),
    meaning game is a draw. False otherwise.
    """
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    # Select the players' checkers symbols for the configured number of players
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly choose starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        current_checker = players[current_player_idx]

        # Get valid column choice from player
        col = get_valid_column(current_checker)

        # Attempt to place checker; if column full, player loses turn
        if not place_checker(board, col, current_checker):
            print(f"Column {chr(ord('A') + col)} is full! Player {current_checker} loses the turn.")
            input("Press Enter to continue...")
        else:
            # After successful placement, check for win
            if is_winner(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if is_draw(board):
                clear_screen()
                print_board(board)
                print("Game is a draw!")
                break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
