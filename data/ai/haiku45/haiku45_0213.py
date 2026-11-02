import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and borders."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_column(col_input, board):
    """Check if column input is valid and not full."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    
    col = ord(col_input.upper()) - 65
    
    if col < 0 or col >= COLS:
        return False
    
    if board[0][col] != " ":
        return False
    
    return True


def get_column_index(col_input):
    """Convert column letter to index."""
    return ord(col_input.upper()) - 65


def place_checker(board, col, checker):
    """Place checker in column and return True if successful."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the checker has won the game."""
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
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLS))


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            col_input = input(f"Player {checker}, please enter a column: ").strip()
            if is_valid_column(col_input, board):
                col = get_column_index(col_input)
                place_checker(board, col, checker)
                break
            else:
                print("Invalid input. Please enter a valid column.")
        
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
