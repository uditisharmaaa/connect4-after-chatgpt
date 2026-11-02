import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels"""
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for col in range(COLS):
            print(board[row][col] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Check if the column input is valid"""
    # Check if input is a single character
    if len(column) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not column.isupper():
        return False
    
    # Convert column letter to index
    col_index = ord(column) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(column, checker, board):
    """Place the checker in the specified column"""
    col_index = ord(column) - 65
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    
    return -1, -1

def check_win(board, checker):
    """Check if the given checker has won"""
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
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == checker and 
                board[row + 1][col - 1] == checker and 
                board[row + 2][col - 2] == checker and 
                board[row + 3][col - 3] == checker):
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
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Ask for input
        column = input(f"Player {checker}, please enter a column: ")
        
        # Validate input
        while not is_valid_column(column, board):
            print("Invalid input. Please try again.")
            column = input(f"Player {checker}, please enter a column: ")
        
        # Place checker
        place_checker(column, checker, board)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
