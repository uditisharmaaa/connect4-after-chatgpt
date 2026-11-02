import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers
    header = '  '
    for col in range(COLUMNS):
        header += f" {chr(65 + col)}  "
    print(header)
    
    # Print the board rows with separators
    separator = '+' + ('---+' * COLUMNS)
    for row in range(ROWS):
        print(separator)
        row_line = '|'
        for col in range(COLUMNS):
            row_line += f' {board[row][col]} |'
        print(row_line)
    print(separator)

def get_valid_column(board):
    """Get a valid column input from the current player."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Column out of range. Please enter a letter between A and {chr(65 + COLUMNS - 1)}.")
            continue
        if board[0][col_index] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_index

def place_checker(board, col, symbol):
    """Place a checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_winner(board, row, col):
    """Check if the last move resulted in a win."""
    symbol = board[row][col]
    
    # Check horizontal
    count = 1
    left = col - 1
    while left >= 0 and board[row][left] == symbol:
        count += 1
        left -= 1
    right = col + 1
    while right < COLUMNS and board[row][right] == symbol:
        count += 1
        right += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    up = row - 1
    while up >= 0 and board[up][col] == symbol:
        count += 1
        up -= 1
    down = row + 1
    while down < ROWS and board[down][col] == symbol:
        count += 1
        down += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == symbol:
        count += 1
        i -= 1
        j -= 1
    i, j = row + 1, col + 1
    while i < ROWS and j < COLUMNS and board[i][j] == symbol:
        count += 1
        i += 1
        j += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    i, j = row - 1, col + 1
    while i >= 0 and j < COLUMNS and board[i][j] == symbol:
        count += 1
        i -= 1
        j += 1
    i, j = row + 1, col - 1
    while i < ROWS and j >= 0 and board[i][j] == symbol:
        count += 1
        i += 1
        j -= 1
    if count >= 4:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full (a draw)."""
    for col in range(COLUMNS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main function to run the Connect 4 game."""
    global current_player
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        col = get_valid_column(board)
        row = place_checker(board, col, PLAYER_SYMBOLS[current_player])
        
        if check_winner(board, row, col):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
