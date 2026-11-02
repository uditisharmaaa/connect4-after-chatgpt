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
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print top border
    print("+" + "---+" * COLS)
    
    # Print each row with borders
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+" + "---+" * COLS)

def is_valid_column(board, col):
    """Check if the column index is valid and has space available."""
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column is empty
    return board[0][col] == ' '

def get_next_row(board, col):
    """Find the lowest available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, col, symbol):
    """Place a checker in the specified column."""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = symbol
        return True
    return False

def check_win(board, symbol):
    """Check if the specified player has won the game."""
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
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
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
        prompt = f"Player {player_symbol}, please enter a column: "
        user_input = input(prompt)
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index (A=0, B=1, etc.)
        col_index = ord(user_input) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please choose between A and {chr(64 + COLS)}.")
            continue
        
        # Check if column has space available
        if not is_valid_column(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    # Initialize the game
    board = create_board()
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get player input
        col = get_player_input(board, current_symbol)
        
        # Place the checker
        place_checker(board, col, current_symbol)
        
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

# Run the game
if __name__ == "__main__":
    play_game()
