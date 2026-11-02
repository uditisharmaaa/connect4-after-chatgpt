import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column is empty
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, symbol):
    """Place a checker in the specified column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        user_input = input("Player " + player_symbol + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase and get column number
        user_input = user_input.upper()
        col = ord(user_input) - 65
        
        # Check if column is valid
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(65 + COLS - 1) + ".")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's symbol
        player_symbol = SYMBOLS[current_player]
        
        # Get player move
        col = get_player_move(board, player_symbol)
        
        # Place checker
        row = place_checker(board, col, player_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, player_symbol):
            print("Player " + player_symbol + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
