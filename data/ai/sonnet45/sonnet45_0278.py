import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

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
    
    # Print board with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for col in range(COLS):
            print(board[row][col] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Check if column is within board range
    col_index = ord(col_letter) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, symbol):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return True
    
    return False

def check_win(board, symbol):
    """Check if the given player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(player_symbol, board):
    """Get valid input from the player."""
    while True:
        col = input("Player " + player_symbol + ", please enter a column: ")
        
        if is_valid_column(col, board):
            return col
        else:
            print("Invalid input. Please try again.")

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player symbol
        player_symbol = PLAYER_SYMBOLS[current_player]
        
        # Get player input
        col = get_player_input(player_symbol, board)
        
        # Place checker
        place_checker(board, col, player_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, player_symbol):
            print("Player " + player_symbol + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
