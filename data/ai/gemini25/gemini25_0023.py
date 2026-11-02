import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def get_column_letter(col_index):
    """Converts a column index to its corresponding letter (A, B, C, ...)."""
    return chr(ord('A') + col_index)

def get_column_index(col_letter):
    """Converts a column letter to its corresponding index (0, 1, 2, ...)."""
    return ord(col_letter.upper()) - ord('A')

def create_board():
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    Returns a list of lists representing the board.
    """
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f" {get_column_letter(col_index)} ", end=" ")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and separators
    for row_index in range(NUM_ROWS):
        print("|", end="")
        for col_index in range(NUM_COLS):
            print(f" {board[row_index][col_index]} |", end="")
        print()
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

def is_valid_column_input(col_input):
    """
    Checks if the given column input is a single uppercase letter
    within the valid range of columns.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return False
    if not 'A' <= col_input.upper() <= get_column_letter(NUM_COLS - 1):
        return False
    return True

def get_player_move(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Keeps prompting until a valid input is received.
    Returns the chosen column index.
    """
    while True:
        col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
        if not is_valid_column_input(col_input):
            print("Invalid input. Please enter a single letter (e.g., A, B).")
            continue

        col_index = get_column_index(col_input)
        if not (0 <= col_index < NUM_COLS):
            print(f"Invalid column. Please enter a letter between A and {get_column_letter(NUM_COLS - 1)}.")
            continue
        return col_index

def place_checker(board, col_index, current_player_checker):
    """
    Places the current player's checker in the lowest available spot
    of the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = current_player_checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has formed a winning line (horizontal, vertical, or diagonal).
    Returns True if a win is found, False otherwise.
    """

    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive slope diagonal wins (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative slope diagonal wins (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    Returns True if it's a draw, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = ACTIVE_CHECKERS[current_player_index]
        print_board(board)

        valid_move_made = False
        while not valid_move_made:
            chosen_col_index = get_player_move(current_player_checker)
            if place_checker(board, chosen_col_index, current_player_checker):
                valid_move_made = True
            else:
                print(f"Column {get_column_letter(chosen_col_index)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        print_board(board) # Print board after checker is placed

        if check_win(board, current_player_checker):
            winner_checker = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")
    print("Game Over!")

if __name__ == "__main__":
    main()
