import os
import random

# Constants for board dimensions (rows x columns)
ROWS = 6
COLUMNS = 7

# Constants for players and their checkers
# For this assignment, 2 players: "X" and "O"
PLAYERS = ["X", "O"]

WIN_LENGTH = 4  # Number of checkers in a row needed to win

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """
    Create and return a board initialized with spaces.
    Board is a list of lists: rows x columns
    """
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and grid as per assignment example."""
    # Column labels (A, B, C, ...)
    column_labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(column_labels))
    # Print each row from top to bottom
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        # Each cell in the row
        row_cells = []
        for col in range(COLUMNS):
            row_cells.append(f" {board[row][col]} ")
        print("|" + "|".join(row_cells) + "|")
    print("+---" * COLUMNS + "+")

def is_valid_column(column):
    """
    Check if the column character is valid input (A-G for 7 columns).
    Input should be uppercase letter corresponding to column.
    """
    if len(column) != 1:
        return False
    col_ord = ord(column)
    return ord('A') <= col_ord < ord('A') + COLUMNS

def column_index(column):
    """Convert column letter (A-G) to column index (0-based). Assumes valid input."""
    return ord(column) - ord('A')

def get_next_open_row(board, col):
    """
    Get the lowest empty row in the given column.
    Return the row index if available, else None if the column is full.
    """
    # Start from bottom row (ROWS-1) upwards
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, row, col, checker):
    """Place the player's checker on the board at the given position."""
    board[row][col] = checker

def check_winner(board, checker):
    """
    Check if the player with 'checker' has won the game by having 4 in a row.
    Check all horizontal, vertical, and diagonal directions.
    Return True if won, else False.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + offset][col] == checker for offset in range(WIN_LENGTH)):
                return True

    # Check positively sloped diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row - offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Check negatively sloped diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    """Check if the board is completely filled (no spaces left)."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board()
    
    # Randomly select the starting player index
    current_player_idx = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_checker = PLAYERS[current_player_idx]
        
        # Prompt the current player for a column until valid or skipped turn if column full
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            # Validate input: must be valid column letter
            if not is_valid_column(user_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col = column_index(user_input)
            open_row = get_next_open_row(board, col)
            
            if open_row is None:
                # Column full, player loses turn
                print(f"Column {user_input} is full, you lose your turn.")
                break
            
            # Valid move found, place checker and break input loop
            place_checker(board, open_row, col, current_checker)
            break
        
        # Check if move resulted in win (only if a checker was placed)
        if open_row is not None:
            if check_winner(board, current_checker):
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
        
        # Move to next player
        current_player_idx = (current_player_idx + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
