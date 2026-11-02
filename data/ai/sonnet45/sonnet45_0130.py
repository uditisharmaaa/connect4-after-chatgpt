import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """
    Check if the input is a valid column letter and if the column is not full.
    Returns (is_valid, col_index) tuple.
    """
    # Check if input is a single character
    if len(col_letter) != 1:
        return False, -1
    
    # Check if it's an uppercase letter
    if not col_letter.isupper() or not col_letter.isalpha():
        return False, -1
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False, -1
    
    # Check if column is not full (top row must have space)
    if board[0][col_index] != " ":
        return False, -1
    
    return True, col_index

def place_checker(board, col_index, symbol):
    """
    Place a checker in the specified column at the lowest available row.
    Returns the row where the checker was placed.
    """
    # Start from bottom row and work upward
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, symbol):
    """
    Check if the given symbol has 4 in a row (horizontal, vertical, or diagonal).
    Returns True if player won, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == symbol and
                board[row + 1][col - 1] == symbol and
                board[row + 2][col - 2] == symbol and
                board[row + 3][col - 3] == symbol):
                return True
    
    return False

def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if board is full, False otherwise.
    """
    # Check if top row has any empty spaces
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Get player symbols based on number of players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get valid input from current player
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {current_symbol}, please enter a column: ")
            is_valid, col_index = is_valid_column(col_input, board)
            
            if is_valid:
                valid_input = True
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place the checker
        place_checker(board, col_index, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
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
