import random
import os

# Constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and initialize an empty game board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(NUM_COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print top border
    print("+" + "---+" * NUM_COLS)
    
    # Print each row with borders
    for row in range(NUM_ROWS):
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+" + "---+" * NUM_COLS)

def is_valid_column(col_letter):
    """Check if the column input is a valid letter within board range."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isupper():
        return False
    col_index = ord(col_letter) - 65
    return 0 <= col_index < NUM_COLS

def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available position."""
    # Start from bottom row and find first empty space
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    
    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(board, player_checker):
    """Get and validate player input for column selection."""
    while True:
        col_letter = input(f"Player {player_checker}, please enter a column: ")
        
        # Validate input is a valid column letter
        if not is_valid_column(col_letter):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(col_letter) - 65
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            return None
        
        return col_index

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        player_checker = CHECKERS[current_player]
        
        # Get player input
        col_index = get_player_input(board, player_checker)
        
        # If column was full, skip turn
        if col_index is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        place_checker(board, col_index, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
