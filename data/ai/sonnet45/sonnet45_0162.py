import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print(' ', end='')
    for col in range(COLS):
        print(f'  {chr(65 + col)} ', end='')
    print()
    
    # Print top border
    print('+' + '---+' * COLS)
    
    # Print each row from top to bottom
    for row in range(ROWS):
        print('|', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
        print('+' + '---+' * COLS)

def is_valid_column(col_letter, board):
    """Check if the column input is valid and has space."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space (top row must be empty)
    if board[0][col_index] != ' ':
        return False
    
    return True

def place_checker(board, col_letter, symbol):
    """Place a checker in the specified column and return the row position."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = symbol
            return row
    
    return -1  # Column is full (should not happen if validation works)

def check_win(board, symbol):
    """Check if the specified player symbol has won the game."""
    
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row][col + 1] == symbol and 
                board[row][col + 2] == symbol and 
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and 
                board[row + 1][col] == symbol and 
                board[row + 2][col] == symbol and 
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row + 1][col + 1] == symbol and 
                board[row + 2][col + 2] == symbol and 
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row - 1][col + 1] == symbol and 
                board[row - 2][col + 2] == symbol and 
                board[row - 3][col + 3] == symbol):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_input(board, player_symbol):
    """Get and validate player input for column selection."""
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        if is_valid_column(col_input, board):
            return col_input
        else:
            print("Invalid input! Please enter a valid column letter with available space.")

def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Select players for the game
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        col_letter = get_player_input(board, current_player)
        
        # Place the checker
        place_checker(board, col_letter, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
