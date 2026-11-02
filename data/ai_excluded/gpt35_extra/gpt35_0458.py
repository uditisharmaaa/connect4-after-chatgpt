import os
import random

# Constants for board dimensions and players
ROWS = 6              # Number of rows on the board
COLS = 7              # Number of columns on the board (max 26)
NUM_PLAYERS = 2       # Number of players (2 to 5)
WIN_LENGTH = 4        # Number of checkers in a row needed to win

# Player checkers symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal with column labels."""
    cols = len(board[0])
    rows = len(board)
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print horizontal separator line
    separator = "+" + "---+" * cols
    # Print rows from top to bottom
    for row in range(rows):
        print(separator)
        # Each row cells with vertical bars
        row_str = "| " + " | ".join(board[row][col] for col in range(cols)) + " |"
        print(row_str)
    print(separator)

def is_valid_column(col_char, cols):
    """Checks if the input column character is valid (in range A to max column)."""
    if len(col_char) != 1:
        return False
    col_num = ord(col_char) - ord('A')
    return 0 <= col_num < cols

def get_column_index(col_char):
    """Converts column letter to zero-based index."""
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    """
    Attempts to place the checker in the specified column.
    Returns True if placed, False if column is full.
    The checker falls to the lowest available cell in the column.
    """
    rows = len(board)
    # Start checking from bottom row upwards for empty space
    for row in reversed(range(rows)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """Checks if the given checker has won by forming four in a row."""
    rows = len(board)
    cols = len(board[0])

    # Helper function to check four in a direction starting at (r,c)
    def check_direction(r, c, dr, dc):
        count = 0
        for i in range(WIN_LENGTH):
            rr = r + dr * i
            cc = c + dc * i
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                return False
            if board[rr][cc] != checker:
                return False
        return True

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                # check horizontal
                if check_direction(r, c, 0, 1):
                    return True
                # check vertical
                if check_direction(r, c, 1, 0):
                    return True
                # check diagonal down-right
                if check_direction(r, c, 1, 1):
                    return True
                # check diagonal down-left
                if check_direction(r, c, 1, -1):
                    return True
    return False

def board_full(board):
    """Returns True if no empty spaces remain on the board (draw), else False."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Create game board
    board = create_board(ROWS, COLS)

    # Select random starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Clear screen and print initial board
    clear_screen()
    print_board(board)

    while True:
        # Current player info
        checker = CHECKERS[current_player_idx]
        print(f"Player {checker}, please enter a column:")

        # Input validation loop
        while True:
            col_input = input().strip().upper()
            if not is_valid_column(col_input, COLS):
                print("Invalid input. Please enter a valid column letter (A to {}):".format(chr(ord('A') + COLS - 1)))
                continue
            col_index = get_column_index(col_input)
            # Check if column is already full
            if board[0][col_index] != " ":
                # Lose turn if column full
                print(f"Column {col_input} is full. You lose your turn.")
                break
            # Place checker if possible
            placed = place_checker(board, col_index, checker)
            if not placed:
                # This theoretically shouldn't happen because we check top cell,
                # but keep safe check anyway.
                print(f"Cannot place checker in column {col_input}. Try another column:")
                continue
            # Successfully placed
            break

        # Clear screen and print updated board
        clear_screen()
        print_board(board)

        # If we placed successfully, check for win
        if board[0][col_index] == checker or (board[ROWS-1][col_index] == checker or True):
            if placed and check_win(board, checker):
                print(f"Player {checker} won!")
                break

        # Check for draw if board full
        if board_full(board):
            print("Game is a draw!")
            break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
