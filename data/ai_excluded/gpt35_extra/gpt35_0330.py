import os
import random

# Constants for the board dimensions and players
ROWS = 6          # Number of rows (height)
COLUMNS = 7       # Number of columns (width), max 26 supported
NUM_PLAYERS = 2   # Number of players (2 to 5)
WIN_LENGTH = 4    # Number of checkers in a row needed to win

# Checkers symbols for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create and return an empty board (rows x cols) filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels and horizontal separators."""
    # Column labels: A, B, C, ...
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    row_separator = "+---" * len(board[0]) + "+"
    for row in range(len(board)):
        print(row_separator)
        # Print each cell surrounded by "|"
        print("| " + " | ".join(board[row]) + " |")
    print(row_separator)

def valid_column_input(input_str, cols):
    """Check if the input is a single uppercase letter within valid column range."""
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if 'A' <= c <= chr(ord('A') + cols -1):
        return True
    return False

def get_column_index(letter):
    """Convert column letter (A-G etc.) to zero-based index."""
    return ord(letter) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in column col (0-indexed).
    The checker falls to the lowest available row in that column.
    Return True if placed successfully, False if column is full.
    """
    # Start from bottom row, go upwards
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """Check the board for 4 in a row of checker horizontally, vertically, diagonally."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal check (\ direction)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            win = True
            for offset in range(WIN_LENGTH):
                if board[r+offset][c+offset] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal check (/ direction)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            win = True
            for offset in range(WIN_LENGTH):
                if board[r - offset][c + offset] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def board_full(board):
    """Check if the board is full (no spaces left)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Initialize game variables
    board = create_board(ROWS, COLUMNS)

    # Use only the number of checkers for the players in use
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly pick the first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]

        # Prompt player input
        while True:
            player_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if not valid_column_input(player_input, COLUMNS):
                # Invalid column letter input
                continue
            col_index = get_column_index(player_input)
            # Check if column is full
            if board[0][col_index] != " ":
                # Column completely filled, player loses turn
                break  # exit input loop, losing turn
            else:
                # Valid input, column not full
                placed = place_checker(board, col_index, current_checker)
                if placed:
                    break  # input accepted and checker placed
                else:
                    # Column full (very unlikely here since we checked top cell)
                    break  # lose turn

        # If checker was placed, check for win
        if board[0][col_index] != " " and placed:
            if check_win(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                return

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            return

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
