import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_input(column_input):
    """Validate the column input."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    col_index = ord(column_input.upper()) - 65
    return 0 <= col_index < COLS


def get_column_index(column_input):
    """Convert column letter to index."""
    return ord(column_input.upper()) - 65


def place_checker(board, col_index, checker):
    """Place checker in the column and return True if successful."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely filled."""
    return all(board[0][col] != " " for col in range(COLS))


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        player_name = chr(65 + current_player) if NUM_PLAYERS > 2 else checker
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            
            if not is_valid_input(column_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = get_column_index(column_input)
            
            if place_checker(board, col_index, checker):
                break
            else:
                print("Column is full. Please choose another column.")
        
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
