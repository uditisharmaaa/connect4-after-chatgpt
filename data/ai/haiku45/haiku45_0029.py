import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the current board state."""
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f"{chr(65 + i)}   ", end="")
    print()
    
    # Print board
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_input(column_char, board):
    """Check if input is valid."""
    if len(column_char) != 1:
        return False
    if not column_char.isalpha():
        return False
    
    col = ord(column_char.upper()) - ord('A')
    if col < 0 or col >= len(board[0]):
        return False
    
    # Check if column is not full
    if board[0][col] != " ":
        return False
    
    return True


def place_checker(board, column_char, checker):
    """Place checker in the column and return True if successful."""
    col = ord(column_char.upper()) - ord('A')
    
    # Find lowest empty row in column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if board is full."""
    return all(board[0][col] != " " for col in range(len(board[0])))


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {checkers[current_player]} starts!\n")
    
    while True:
        checker = checkers[current_player]
        
        # Get valid input
        while True:
            column = input(f"Player {checker}, please enter a column: ").strip()
            if is_valid_input(column, board):
                break
            print("Invalid input. Please enter a valid column.")
        
        # Place checker
        place_checker(board, column, checker)
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
