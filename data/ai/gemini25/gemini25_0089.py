import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS] # Use only required checkers
WIN_CONDITION = 4 # Number of checkers in a row to win

# --- Board Initialization and Printing ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the board.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print board content
    for r_idx, row in enumerate(board):
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()

        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()

    # Print bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

# --- Game Logic Functions ---

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        except TypeError: # This should not happen with current validation, but good practice
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    num_rows = len(board)
    for r_idx in range(num_rows - 1, -1, -1):
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker, win_condition):
    """
    Checks if the current player has won horizontally, vertically, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False # Found an empty spot, not a draw yet
    return True # No empty spots, it's a draw

# --- Main Game Loop ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)

        valid_move = False
        while not valid_move:
            col_input_index = get_column_input(current_player_checker, NUM_COLS)
            valid_move = drop_checker(board, col_input_index, current_player_checker)
            if not valid_move:
                print("Column is full. Please choose another column.")
                # The turn is not lost, player is asked again

        print_board(board) # Print board after valid move

        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
