import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2

# Define the checkers based on number of players
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS_COUNT]

def initialize_board():
    """Create an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the top border
    print('+' + '---+' * COLS)
    
    for row in board:
        # Print the row content
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print the bottom border
        print('+' + '---+' * COLS)

def is_valid_column(column):
    """Check if the input column is valid."""
    if len(column) != 1:
        return False
    
    col_char = column.upper()
    if not col_char.isalpha():
        return False
    
    col_idx = ord(col_char) - ord('A')
    return 0 <= col_idx < COLS

def get_column_index(column):
    """Convert column letter to index (0-based)."""
    return ord(column.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """Place the checker in the lowest available row in the specified column."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS_COUNT - 1)
    
    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        
        # Get and validate input
        while True:
            column = input().strip()
            if not is_valid_column(column):
                print("Invalid input. Please enter a valid column (A-G): ", end='')
                continue
            
            col_idx = get_column_index(column)
            if not place_checker(board, col_idx, checker):
                print("Column is full. Please choose another column: ", end='')
                continue
            break
        
        # Check for win or draw
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
