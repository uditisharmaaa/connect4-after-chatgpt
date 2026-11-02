import os
import random

# Constants for the game configuration
ROWS = 6              # Number of rows on the board
COLUMNS = 7           # Number of columns on the board (max 26)
NUM_PLAYERS = 2       # Number of players (between 2 and 5)
WIN_LENGTH = 4        # Number of checkers in a row required to win

# Checkers assigned by player index
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """
    Create and return an empty board as a list of lists.
    The board is ROWS x COLUMNS, each cell initialized with whitespace ' '.
    """
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """
    Print the current state of the board.
    Columns labeled A-G on top, rows unlabeled.
    Printed with row 0 at the top and row ROWS-1 at the bottom.
    """
    # Print column labels
    col_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS))
    print(col_labels)
    # Print top border of the board
    print("+" + "---+" * COLUMNS)
    # Print each row
    for row in range(ROWS):
        # Row cells formatted between | |
        row_cells = "| " + " | ".join(board[row][col] for col in range(COLUMNS)) + " |"
        print(row_cells)
        # Print row separator
        print("+" + "---+" * COLUMNS)

def is_valid_column(col_char):
    """
    Check if the input column character is a valid column letter.
    Return True if valid, else False.
    """
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    return 'A' <= col_char <= chr(ord('A') + COLUMNS - 1)

def column_index(col_char):
    """
    Convert column character to column index (0-based).
    Assumes input is valid uppercase letter.
    """
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Place the checker in the given column on the board.
    The checker falls into the lowest empty position in the column.
    Return True if placement was successful, or False if the column is full.
    """
    # Start checking from bottom row upwards
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """
    Check if the given checker has a winning sequence of length WIN_LENGTH
    horizontally, vertically, or diagonally on the board.
    Return True if won, else False.
    """
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            seq = [board[row][col + i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in seq):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            seq = [board[row + i][col] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in seq):
                return True

    # Diagonal down-right check ( / diagonal)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            seq = [board[row + i][col + i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in seq):
                return True

    # Diagonal down-left check ( \ diagonal)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            seq = [board[row + i][col - i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in seq):
                return True

    return False

def board_full(board):
    """
    Check if the board is full; no empty spaces left in any cell.
    Return True if full, else False.
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def next_player_index(current_idx):
    """Return the next player index, cycling back to 0 after the last."""
    return (current_idx + 1) % NUM_PLAYERS

def get_player_input(current_checker):
    """
    Prompt the current player to enter a column.
    Validate input: uppercase letter, in range, and return column index if valid.
    Keep asking until valid input is provided.
    """
    while True:
        inp = input(f"Player {current_checker}, please enter a column: ")
        inp = inp.strip().upper()
        if not is_valid_column(inp):
            print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLUMNS - 1)}.")
            continue
        col = column_index(inp)
        return col

def main():
    # Initialize the game board
    board = create_board()

    # Randomly select the starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        current_checker = CHECKERS[current_player]

        # Get valid column input from player
        col = get_player_input(current_checker)

        # Try to place checker in the chosen column
        if not place_checker(board, col, current_checker):
            # Column full, turn lost
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            input("Press Enter to continue...")
            # Move to next player without placing a checker
            current_player = next_player_index(current_player)
            continue

        # Check if this move wins the game
        if check_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check if board is full => draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Move to next player
        current_player = next_player_index(current_player)

if __name__ == "__main__":
    main()
