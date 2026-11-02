import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board(rows, cols):
    """Initialize an empty board with the given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column letters and borders."""
    # Clear the screen
    os.system('clear')
    
    # Print column letters
    col_letters = '   '.join([chr(65 + i) for i in range(len(board[0]))])
    print(f"  {col_letters}")
    
    # Print top border
    border = '+' + ('---+' * len(board[0]))
    print(border)
    
    # Print each row with borders
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(border)

def get_valid_column(board):
    """Prompt the player for a valid column input."""
    columns = [chr(65 + i) for i in range(len(board[0]))]
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if col in columns:
            col_idx = ord(col) - ord('A')
            if board[0][col_idx] == ' ':
                return col_idx
            else:
                print("Column is full. Choose another column.")
        else:
            print(f"Invalid column. Please enter a letter from A to {chr(65 + len(board[0]) - 1)}.")

def place_checker(board, col_idx, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current checker has a winning line (4 in a row)."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

# Initialize the game
board = initialize_board(NUM_ROWS, NUM_COLS)
current_player = random.choice(CHECKERS)
print_board(board)

# Main game loop
while True:
    col_idx = get_valid_column(board)
    place_checker(board, col_idx, current_player)
    print_board(board)
    
    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        break
    elif check_draw(board):
        print("Game ended in a draw!")
        break
    
    # Switch to the next player
    current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]
