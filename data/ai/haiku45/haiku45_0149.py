import os
import random

# Configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def create_board():
    """Create a board with all empty cells."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    # Print column labels
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print rows
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+---" * COLS + "+")

def is_valid_column(column_str, board):
    """Validate if the column input is valid and not full."""
    if len(column_str) != 1 or not column_str.isalpha():
        return False
    
    col_index = ord(column_str.upper()) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column_str, checker):
    """Place a checker in the specified column."""
    col_index = ord(column_str.upper()) - ord('A')
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonally (top-right to bottom-left)
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
    print(f"Player {CHECKERS[current_player]} starts!")
    
    while True:
        # Get valid input from player
        while True:
            column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip()
            if is_valid_column(column, board):
                break
            print("Invalid input. Please enter a valid column (A-{}).".format(chr(ord('A') + COLS - 1)))
        
        # Place checker
        place_checker(board, column, CHECKERS[current_player])
        print_board(board)
        
        # Check for win
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
