import os
import random

# Constants for the board dimensions and players
ROWS = 6           # Number of rows
COLS = 7           # Number of columns (max 26 as per requirement)
PLAYERS = 2        # Number of players (between 2 and 5)
WIN_COUNT = 4      # Number of connected checkers needed to win

# Checker symbols assigned by player index
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players supported

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal with column labels."""
    clear_screen()
    cols = len(board[0])
    # Column labels (A, B, C, ...)
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Separator line
    sep = "+---" * cols + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = [f" {board[r][c]} " for c in range(cols)]
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def is_valid_column_input(col_input, cols):
    """Checks if input is a valid column letter."""
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    uppercase_col = col_input.upper()
    if ord(uppercase_col) < ord('A') or ord(uppercase_col) >= ord('A') + cols:
        return False
    return True

def get_column_index(col_input):
    """Converts column letter to zero-based column index."""
    return ord(col_input.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Places the checker in the correct row inside the column.
    Returns True if checker placed, False if column full.
    """
    # Start from bottom row and go upwards
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """Checks if the given checker has four in a row anywhere."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def is_board_full(board):
    """Checks if the board is full (no spaces left)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Initialize board
    board = create_board(ROWS, COLS)
    # Select starting player randomly
    current_player = random.randint(0, PLAYERS - 1)
    players_checkers = CHECKERS[:PLAYERS]

    # Print initial board
    print_board(board)

    while True:
        checker = players_checkers[current_player]
        print(f"Player {checker}, please enter a column:")

        # Input validation loop
        while True:
            user_input = input().strip()
            if not is_valid_column_input(user_input, COLS):
                print("Invalid input. Please enter a valid column letter (A-G):")
                continue
            col_idx = get_column_index(user_input)
            # Check if column is full, if so player loses turn
            if board[0][col_idx] != " ":
                # Column full
                print(f"Column {user_input.upper()} is full. You lose your turn.")
                # Move to next player
                current_player = (current_player + 1) % PLAYERS
                print_board(board)
                break
            else:
                # Place checker and break loop for normal turn
                placed = place_checker(board, col_idx, checker)
                # This should always be True given previous check
                if placed:
                    print_board(board)
                    # Check if player won
                    if check_winner(board, checker):
                        print(f"Player {checker} won!")
                        return
                    # Check draw
                    if is_board_full(board):
                        print("The game is a draw!")
                        return
                    # Next player's turn
                    current_player = (current_player + 1) % PLAYERS
                    break

if __name__ == "__main__":
    main()
