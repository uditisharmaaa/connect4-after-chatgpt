import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))]))

    # Print board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                raise ValueError("Input must be a single letter.")

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < num_cols):
                raise ValueError("Column out of board range.")

            return col_index
        except ValueError as e:
            print(f"Invalid input: {e} Please try again.")

def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Iterate from bottom row up
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """Checks if the board is completely full (a draw)."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # Board is full

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        col_input = get_column_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_input, current_player_checker):
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                sys.exit() # End game
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                sys.exit() # End game
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_input)} is full. Please choose another column.")
            # Player does not lose turn, re-prompt for input

if __name__ == "__main__":
    main()
