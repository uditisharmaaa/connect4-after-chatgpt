import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current board"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print board rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Check if the column input is valid"""
    # Check if column is a single character
    if len(column) != 1:
        return False
    
    # Check if column is a letter
    if not column.isalpha():
        return False
    
    # Check if column is uppercase
    if not column.isupper():
        return False
    
    # Convert column letter to index
    col_index = ord(column) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(column, checker, board):
    """Place a checker in the specified column"""
    col_index = ord(column) - 65
    
    # Find the lowest available row in the column
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_index] == " ":
            board[i][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row - 1][col + 1] == checker and 
                board[row - 2][col + 2] == checker and 
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game function"""
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get player input
        column = input("Player " + checker + ", please enter a column: ")
        
        # Validate input
        while not is_valid_column(column, board):
            print("Invalid input. Please try again.")
            column = input("Player " + checker + ", please enter a column: ")
        
        # Place checker
        place_checker(column, checker, board)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
