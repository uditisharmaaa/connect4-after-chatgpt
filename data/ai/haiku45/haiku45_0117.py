import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column headers and formatting."""
    os.system('clear')
    
    # Print column headers
    header = "  "
    for i in range(COLUMNS):
        header += chr(65 + i) + "   "
    print(header)
    
    # Print board rows
    for row in board:
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print("+---" * COLUMNS + "+")


def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        user_input = input().strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if col < 0 or col >= COLUMNS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLUMNS - 1)}.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        col = get_valid_column()
        
        # Try to place the checker
        if not place_checker(board, col, checker):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
