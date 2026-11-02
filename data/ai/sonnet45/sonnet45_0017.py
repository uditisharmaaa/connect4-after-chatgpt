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
        print(chr(65 + i), end="   ")
    print()
    
    # Print rows with borders
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(board, col):
    """Check if a column is valid and not full"""
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column is empty
    if board[0][col] != " ":
        return False
    return True

def get_next_row(board, col):
    """Find the next available row in a column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won"""
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
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(board, player_checker):
    """Get and validate player input"""
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
        col = ord(user_input) - 65
        
        # Check if column is valid
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(65 + COLS - 1) + ".")
            continue
        
        # Check if column is full
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def play_game():
    """Main game loop"""
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get player input
        col = get_player_input(board, player_checker)
        
        # Place checker
        place_checker(board, col, player_checker)
        
        # Clear screen and print updated board
        os.system('clear')
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
