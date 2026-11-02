import os
import random
import string

# Constants for dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # maximum columns supported
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Global settings for this submission
NUM_PLAYERS = 2  # Must be between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Validate constants for safety
assert 1 <= ROWS
assert 1 <= COLUMNS <= MAX_COLUMNS
assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    """
    Create a board with given rows and columns.
    Each cell initialized as a space.
    Returns a 2D list: board[row][col]
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to the terminal with column letters on top,
    horizontal lines as shown in the assignment example.
    """
    rows = len(board)
    columns = len(board[0]) if rows > 0 else 0

    # Print header: A, B, C, ...
    header = "  "
    for i in range(columns):
        header += "  " + string.ascii_uppercase[i] + " "
    print(header)

    # Print rows from top to bottom with borders
    horizontal_line = "+" + ("---+" * columns)
    for r in range(rows):
        print(horizontal_line)
        row_str = "|"
        for c in range(columns):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(horizontal_line)


def input_valid_column(input_str, columns):
    """
    Check if the input string is a single uppercase letter between A and max column letter
    """
    if len(input_str) != 1:
        return False
    ch = input_str[0]
    if ch not in string.ascii_uppercase[:columns]:
        return False
    return True


def place_checker(board, col_index, checker):
    """
    Place the checker at the lowest available row in the given column.
    If the column is full, return False.
    Otherwise, place the checker and return True.
    The board indexing: board[row][col]
    Row 0 is top, row ROWS-1 is bottom.
    """
    # Traverse from bottom row upward
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """
    Check the board for 4 in a row of given checker horizontally,
    vertically or diagonally.
    Returns True if checker has won, False otherwise
    """
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(columns):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(columns):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(columns - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(columns - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True

    return False


def board_full(board):
    """
    Returns True if the board is full (no spaces), False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]

        # Player input loop
        valid_move = False
        while not valid_move:
            player_prompt = f"Player {current_checker}, please enter a column: "
            column_input = input(player_prompt).strip().upper()
            if not input_valid_column(column_input, COLUMNS):
                # Invalid character or out of range
                continue

            col_index = ord(column_input) - ord('A')

            # Try placing the checker
            if not place_checker(board, col_index, current_checker):
                # Column full, player loses turn
                valid_move = True  # move "completed" but no checker placed
            else:
                valid_move = True

        # If checker was placed, check for win
        # If not placed because column full, no checker was added; no win possible.
        if valid_move:
            # Check if current player won
            if check_win(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break

        # Advance turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
