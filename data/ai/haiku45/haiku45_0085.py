import os
import random

# Configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  " + "   ".join([chr(ord('A') + i) for i in range(cols)]))
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+---" * cols + "+")

def is_valid_move(board, col, cols):
    """Check if a move is valid (column exists and not full)."""
    if col < 0 or col >= cols:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker, rows):
    """Place a checker in the lowest available position in a column."""
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, rows, cols, checker):
    """Check if the current player has won."""
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

def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(cols))

def get_player_input(cols):
    """Get and validate player input."""
    while True:
        user_input = input("Please enter a column (A-" + chr(ord('A') + cols - 1) + "): ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checkers = CHECKERS[:NUM_PLAYERS]
    
    print_board(board, COLS)
    
    while True:
        checker = checkers[current_player]
        print(f"Player {checker}, please enter a column:")
        
        col = get_player_input(COLS)
        
        if not is_valid_move(board, col, COLS):
            print("This column is full. Please choose another column.")
            continue
        
        place_checker(board, col, checker, ROWS)
        print_board(board, COLS)
        
        if check_win(board, ROWS, COLS, checker):
            print(f"Player {checker} won!")
            return
        
        if is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            return
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
