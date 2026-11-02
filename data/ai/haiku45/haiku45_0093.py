import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and initialize the board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board in the required format."""
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

def get_valid_column(board, current_player):
    """Get a valid column input from the player."""
    while True:
        try:
            user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            
            # Check if input is a single letter
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a single letter.")
                continue
            
            # Convert letter to column index
            col = ord(user_input) - ord('A')
            
            # Check if column is within bounds
            if col < 0 or col >= COLS:
                print(f"Invalid column. Please enter a column between A and {chr(65 + COLS - 1)}.")
                continue
            
            # Check if column is full
            if board[0][col] != " ":
                print("Column is full. Please choose another column.")
                continue
            
            return col
        except Exception:
            print("Invalid input. Please try again.")

def place_checker(board, col, current_player):
    """Place the checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return

def check_winner(board, current_player):
    """Check if the current player has won."""
    checker = CHECKERS[current_player]
    
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
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main game loop."""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        col = get_valid_column(board, current_player)
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
