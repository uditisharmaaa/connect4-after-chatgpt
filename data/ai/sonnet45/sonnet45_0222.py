import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board"""
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(NUM_COLS):
        label = chr(ord('A') + col)
        print(label + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(NUM_ROWS):
        # Print top border of cells
        print("+---" * NUM_COLS + "+")
        # Print cell contents
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * NUM_COLS + "+")

def get_column_input(player_checker):
    """Get and validate column input from player"""
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= NUM_COLS:
            print("Invalid input. Column out of range.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column. Returns True if successful, False if column is full"""
    # Start from bottom row and go up
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game"""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and 
                board[row - 1][col + 1] == checker and 
                board[row - 2][col + 2] == checker and 
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)"""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
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
    game_over = False
    while not game_over:
        # Get current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get column input
        col = get_column_input(player_checker)
        
        # Try to place checker
        placed = place_checker(board, col, player_checker)
        
        if not placed:
            print("Column is full. You lose your turn.")
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print("Player " + player_checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
