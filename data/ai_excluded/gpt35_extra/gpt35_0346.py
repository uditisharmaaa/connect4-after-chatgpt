import os
import random

# Constants for board dimensions and players
ROWS = 6              # Number of rows (height)
COLUMNS = 7           # Number of columns (width)
MAX_COLUMNS = 26      # Maximum columns supported (for letter labeling)
NUM_PLAYERS = 2       # Number of players (between 2 and 5)
WIN_COUNT = 4         # Number of checkers in a row needed to win

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Creates an empty board as a list of lists filled with spaces.
    Each inner list represents a row.
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board with column letters on top and rows below.
    Follows the format specified in the assignment.
    """
    clear_screen()
    # Column letters from 'A'
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    
    # Print the board with horizontal separators
    separator = "+" + "---+" * len(board[0])
    for row in board:
        print(separator)
        # Each cell surrounded by pipes and spaces
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column_input(col_input, columns):
    """
    Checks if the column input is a valid uppercase letter corresponding to the board.
    """
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col_index = ord(col_input) - ord('A')
    if 0 <= col_index < columns:
        return True
    return False

def get_column_index(col_input):
    """
    Converts a column letter (A-G etc.) to column index (0-based).
    """
    return ord(col_input) - ord('A')

def place_checker(board, col_index, checker):
    """
    Places the checker in the specified column.
    The checker falls to the lowest empty row in that column.
    Returns True if placed successfully, False if column is full.
    """
    # Start checking from bottom row upwards
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """
    Checks if the given checker has 4 in a row horizontally,
    vertically, or diagonally on the board.
    Returns True if win condition is met, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    
    # Diagonal (down-right) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (up-right) check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    
    return False

def check_draw(board):
    """
    Returns True if the board is full (no empty spaces), else False.
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Validate constants (optional)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return
    if COLUMNS > MAX_COLUMNS:
        print(f"Maximum columns supported: {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly pick the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial empty board
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input loop for valid input
        while True:
            col_input = input(prompt).strip().upper()

            # Validate input
            if not is_valid_column_input(col_input, COLUMNS):
                # Invalid input, ask again
                continue

            col_index = get_column_index(col_input)

            # Check if column is full
            if not place_checker(board, col_index, current_checker):
                # Column full: turn lost
                print(f"Column {col_input} is full. Player {current_checker} loses this turn.")
                placed = False
                break
            else:
                placed = True
                break

        # Show updated board
        print_board(board)

        # If a checker was placed, check for a win
        if placed:
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
