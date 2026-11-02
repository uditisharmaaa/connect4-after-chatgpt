import os
import random
import string

# ------------- CONSTANTS AND GLOBALS -------------------

# Board dimensions (can be adjusted for testing)
ROW_COUNT = 6  # Number of rows
COL_COUNT = 7  # Number of columns (max 26)

# Number of players (2-5). For submission, keep this = 2
NUM_PLAYERS = 2

CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Display column labels (A, B, C, ...)
COL_LABELS = [chr(ord('A') + i) for i in range(COL_COUNT)]

# ------------- HELPER FUNCTIONS ------------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # Use 'cls' for Windows if necessary

def create_board():
    """Initializes the game board with empty spaces."""
    return [[" " for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]

def print_board(board):
    """Prints the Connect 4 board in the required format."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COL_LABELS))
    print("+" + "---+" * COL_COUNT)
    # Print rows (from top to bottom)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COL_COUNT)

def get_lowest_empty_row(board, col):
    """
    Finds the lowest available row in the column for a move.
    Returns the row index, or None if the column is full.
    """
    for row in reversed(range(ROW_COUNT)):
        if board[row][col] == " ":
            return row
    return None

def is_board_full(board):
    """Checks whether the board is completely filled."""
    for row in board:
        if " " in row:
            return False
    return True

def is_valid_column(input_col):
    """
    Checks if the user input for column is valid.
    Must be a single uppercase letter within available columns.
    """
    return len(input_col) == 1 and input_col in COL_LABELS

def place_checker(board, row, col, checker):
    """Places a player's checker at the specified row and column."""
    board[row][col] = checker

def check_win(board, checker):
    """
    Checks if the player with 'checker' has won (4 in a row).
    Checks horizontal, vertical, and diagonal directions.
    """
    # Horizontal check
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical check
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal (down-right)
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Diagonal (up-right)
    for r in range(3, ROW_COUNT):
        for c in range(COL_COUNT - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

# ------------ MAIN GAME FUNCTION --------------------

def main():
    # Initialize board
    board = create_board()
    player_symbols = CHECKERS[:NUM_PLAYERS]
    
    # Pick random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board and starting player
    print_board(board)
    print(f"Player {player_symbols[current_player]} goes first!")
    input("Press ENTER to start...")
    
    # Game loop
    while True:
        print_board(board)
        current_symbol = player_symbols[current_player]
        print(f"Player {current_symbol}, please enter a column:")

        # Input and validation loop
        while True:
            user_input = input().strip().upper()
            if not is_valid_column(user_input):
                print("Invalid column. Please enter a valid column letter (A-{}):".format(COL_LABELS[-1]))
                continue
            col = COL_LABELS.index(user_input)
            row = get_lowest_empty_row(board, col)
            if row is None:
                print("Column is full. You lose your turn!")
                row = None
                break  # End turn
            else:
                place_checker(board, row, col, current_symbol)
                break  # Valid move

        # If the move was valid (not losing due to full column), check win
        if row is not None:
            if check_win(board, current_symbol):
                print_board(board)
                print(f"Player {current_symbol} won!")
                break
        # Check for a draw
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# ------------ RUN THE GAME --------------------------

if __name__ == "__main__":
    main()
