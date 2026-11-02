import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

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
    """Print the current state of the board"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column is not full)"""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def drop_checker(board, col, symbol):
    """Drop a checker in the specified column"""
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = symbol
            return i
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win"""
    
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
    """Check if the board is completely full"""
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def get_valid_input(board, player_symbol):
    """Get valid input from the player"""
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
        
        # Convert to uppercase and get column index
        user_input = user_input.upper()
        col = ord(user_input) - 65
        
        # Check if column is within range
        if col < 0 or col >= COLS:
            print("Invalid input. Column out of range.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            return -1
        
        return col

def play_game():
    """Main game loop"""
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(PLAYER_SYMBOLS[i])
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get player input
        col = get_valid_input(board, current_symbol)
        
        # If column is full, skip turn
        if col == -1:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Drop checker
        row = drop_checker(board, col, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print("Player " + current_symbol + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
