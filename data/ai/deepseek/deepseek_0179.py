import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Can be changed to any value between 2 and 5

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen before printing the board
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def get_random_first_player():
    """Randomly choose the first player."""
    return random.randint(0, NUM_PLAYERS - 1)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return 'A' <= col <= chr(ord('A') + COLS - 1)

def get_column_index(col):
    """Convert the column letter to a 0-based index."""
    return ord(col.upper()) - ord('A')

def place_checker(board, col, symbol):
    """Place the checker in the lowest available row of the specified column."""
    col_idx = get_column_index(col)
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = symbol
            return True
    return False  # Column is full

def check_win(board, symbol):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row][col+1] == symbol and 
                board[row][col+2] == symbol and 
                board[row][col+3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and 
                board[row+1][col] == symbol and 
                board[row+2][col] == symbol and 
                board[row+3][col] == symbol):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row+1][col+1] == symbol and 
                board[row+2][col+2] == symbol and 
                board[row+3][col+3] == symbol):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == symbol and 
                board[row+1][col-1] == symbol and 
                board[row+2][col-2] == symbol and 
                board[row+3][col-3] == symbol):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = get_random_first_player()
    
    print("Welcome to Connect 4!")
    print_board(board)
    
    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {symbol}, please enter a column: ", end='')
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        col_idx = get_column_index(col)
        if col_idx < 0 or col_idx >= COLS:
            print("Invalid column. Please try again.")
            continue
        
        if not place_checker(board, col, symbol):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
