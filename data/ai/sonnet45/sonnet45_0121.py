import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with all spaces initialized to whitespace"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_input(column, board):
    """Check if the column input is valid"""
    # Check if column is uppercase letter
    if len(column) != 1 or not column.isupper():
        return False
    
    # Convert column letter to index
    col_index = ord(column) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top row is not full)
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column, checker):
    """Place a checker in the specified column"""
    col_index = ord(column) - 65
    
    # Find the lowest available row
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_index] == " ":
            board[i][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game"""
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i][j+1] == checker and 
                board[i][j+2] == checker and 
                board[i][j+3] == checker):
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if (board[i][j] == checker and 
                board[i+1][j] == checker and 
                board[i+2][j] == checker and 
                board[i+3][j] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i+1][j+1] == checker and 
                board[i+2][j+2] == checker and 
                board[i+3][j+3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i-1][j+1] == checker and 
                board[i-2][j+2] == checker and 
                board[i-3][j+3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)"""
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def play_game():
    """Main game loop"""
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            column = input(f"Player {checker}, please enter a column: ")
            
            if is_valid_input(column, board):
                break
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        place_checker(board, column, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
