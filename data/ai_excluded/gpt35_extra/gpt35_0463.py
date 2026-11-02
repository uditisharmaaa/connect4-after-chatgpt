import os
import random
import string

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Selected settings for submission
NUM_PLAYERS = 2  # must be between MIN_PLAYERS and MAX_PLAYERS


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    """Create the game board as a list of rows with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board, players, current_player_index):
    """Print the board with column labels and the current player's turn info."""
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    col_labels = list(string.ascii_uppercase)[:columns]

    # Column labels
    print("  " + "   ".join(col_labels))
    # Print each row with separators
    for r in range(rows):
        print("+" + "---+" * columns)
        row_line = []
        for c in range(columns):
            row_line.append(f" {board[r][c]} ")
        print("|" + "|".join(row_line) + "|")
    print("+" + "---+" * columns)
    player_checker = players[current_player_index]
    print(f"Player {player_checker}, please enter a column:")


def input_valid_column(input_str, columns):
    """Check if the input is a single uppercase letter in the valid range."""
    if len(input_str) != 1:
        return False
    if input_str not in string.ascii_uppercase[:columns]:
        return False
    return True


def place_checker(board, col_index, checker):
    """Place the checker in the given column if possible.
    Returns True if placed, False if column full."""
    rows = len(board)
    # Place checker from bottom up (rows-1 to 0)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # column full


def check_win(board, checker):
    """Check all directions for a win of four consecutive checkers."""
    rows = len(board)
    cols = len(board[0])

    def four_in_a_row(lst):
        count = 0
        for val in lst:
            if val == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
        return False

    # Check horizontal
    for r in range(rows):
        if four_in_a_row(board[r]):
            return True

    # Check vertical
    for c in range(cols):
        col_vals = [board[r][c] for r in range(rows)]
        if four_in_a_row(col_vals):
            return True

    # Check diagonals (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r + i][c + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    # Check diagonals (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r - i][c + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    return False


def board_full(board):
    """Return True if no empty spaces, else False."""
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Validate settings
    if COLUMNS > MAX_COLUMNS or COLUMNS < 1:
        print(f"Error: Columns must be between 1 and {MAX_COLUMNS}")
        return
    if ROWS < 1:
        print("Error: Rows must be positive")
        return
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Error: Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
        return

    players = PLAYERS[:NUM_PLAYERS]

    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board, players, current_player_index)

    while True:
        player_checker = players[current_player_index]

        col_input = input().strip().upper()

        # Validate input
        while not input_valid_column(col_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter:")
            col_input = input().strip().upper()

        col_index = string.ascii_uppercase.index(col_input)

        placed = place_checker(board, col_index, player_checker)
        if not placed:
            # Turn lost if column is full
            print(f"Column {col_input} is full. Player {player_checker} loses the turn.")
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board, players, current_player_index)
            continue

        print_board(board, players, current_player_index)

        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
