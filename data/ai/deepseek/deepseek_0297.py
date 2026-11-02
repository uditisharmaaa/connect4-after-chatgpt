import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print the board rows
    for row in range(ROWS):
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print the bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()

def get_valid_column():
    """Prompt the player for a column and validate the input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or ord(col) < ord('A') or ord(col) >= ord('A') + COLS:
            print("Invalid column. Please enter a letter from A to", chr(ord('A') + COLS - 1))
            continue
        
        col_index = ord(col) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col_index, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
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
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == checker and
                board[row+1][col-1] == checker and
                board[row+2][col-2] == checker and
                board[row+3][col-3] == checker):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

# Main game loop
board = initialize_board()
current_player = random.randint(0, PLAYERS - 1)
checker = CHECKERS[current_player]

print_board(board)

while True:
    col_index = get_valid_column()
    
    if place_checker(board, col_index, checker):
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS
        checker = CHECKERS[current_player]
