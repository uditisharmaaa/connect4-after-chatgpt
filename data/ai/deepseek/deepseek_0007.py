import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print the board rows
    for row in board:
        print('+' + '---+' * BOARD_COLS)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print('+' + '---+' * BOARD_COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col.isalpha() and 65 <= ord(col) <= (65 + BOARD_COLS - 1)

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    col_idx = ord(col.upper()) - 65
    if col_idx < 0 or col_idx >= BOARD_COLS:
        return False
    
    # Find the lowest empty row in the column
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    
    return False  # Column is full

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal, vertical, and both diagonals
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and
                board[row][col+1] == checker and
                board[row][col+2] == checker and
                board[row][col+3] == checker):
                return True
    
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == checker and
                board[row+1][col] == checker and
                board[row+2][col] == checker and
                board[row+3][col] == checker):
                return True
    
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True
    
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if (board[row][col] == checker and
                board[row+1][col-1] == checker and
                board[row+2][col-2] == checker and
                board[row+3][col-3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_connect4():
    """Main function to play Connect 4."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ", end='')
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        if not place_checker(board, col, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_connect4()
