import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates and returns a 2D list representing the game board.
    All cells are initialized with empty spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    """
    Prints the current state of the board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the player for column input and validates it.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper() or not user_input.isalpha():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print("Invalid column. Please choose a column within the board.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Start from the bottom row and move up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False

def check_win(board, checker):
    """
    Checks if the specified checker has won the game.
    Returns True if 4 in a row found (horizontal, vertical, or diagonal).
    """
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
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if all cells are filled.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """
    Main game loop that handles the Connect 4 game flow.
    """
    # Initialize the board
    board = create_board()
    
    # Get player checkers based on number of players
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get valid column input
        col = get_column_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col, current_checker):
            print("Column is full! You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
