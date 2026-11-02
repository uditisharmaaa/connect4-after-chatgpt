import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_column_letter(col_index):
    """Converts a column index (0-25) to its corresponding uppercase letter (A-Z)."""
    if 0 <= col_index < 26:
        return chr(ord('A') + col_index)
    return ''

def get_column_index(col_letter):
    """Converts an uppercase column letter (A-Z) to its corresponding index (0-25)."""
    if 'A' <= col_letter <= 'Z':
        return ord(col_letter) - ord('A')
    return -1

def create_board(rows, cols):
    """Creates an empty Connect 4 board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    clear_screen()

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col in range(NUM_COLS):
        print(f" {get_column_letter(col)} ", end="")
    print()

    # Print board rows
    for row in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def is_valid_input(board, col_input):
    """
    Validates the player's column input.
    Returns the column index if valid, otherwise -1.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return -1

    col_input = col_input.upper()
    col_index = get_column_index(col_input)

    if not (0 <= col_index < NUM_COLS):
        print("Invalid column letter. Please choose a column between A and", get_column_letter(NUM_COLS - 1))
        return -1

    # Check if the column is full
    if board[0][col_index] != " ":
        print("Column is full. Please choose another column.")
        return -1

    return col_index

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if successful, False if the column is full (should be handled by validation).
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False # Should ideally not be reached if validation is correct

def check_win(board, checker):
    """
    Checks if the current player has won the game.
    A player wins if they have WIN_CONDITION checkers in a row horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    if NUM_COLS > 26:
        print("Error: Maximum 26 columns supported due to letter labels.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    player_checkers_in_game = PLAYER_CHECKERS[:NUM_PLAYERS]

    game_over = False

    while not game_over:
        current_checker = player_checkers_in_game[current_player_index]
        
        print_board(board)
        
        valid_turn = False
        col_index = -1
        while not valid_turn:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip()
            col_index = is_valid_input(board, user_input)
            if col_index != -1:
                valid_turn = True
            # If invalid, the prompt inside is_valid_input will guide the user.

        drop_checker(board, col_index, current_checker)
        
        print_board(board) # Print board immediately after placing checker

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
