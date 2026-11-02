import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns an empty game board.
    Returns a 2D list with ROWS rows and COLS columns, initialized with spaces.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    """
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


def get_column_input(current_player):
    """
    Prompts the current player for a column input and validates it.
    Returns the column index (0-based) if valid.
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}.")
            continue
        
        return col_index


def place_checker(board, col, player_symbol):
    """
    Places a checker in the specified column for the current player.
    Returns True if successful, False if column is full.
    """
    # Find the lowest available row in the column (start from bottom)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return True
    
    # Column is full
    return False


def check_win(board, player_symbol):
    """
    Checks if the current player has won the game.
    Returns True if player has 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Checks if the board is completely filled (draw condition).
    Returns True if no empty spaces remain.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = create_board()
    
    # Create list of players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input from player
        col = get_column_input(current_player)
        
        # Try to place the checker
        if not place_checker(board, col, current_player):
            print("Column is full! You lose your turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check if game is a draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Start the game
if __name__ == "__main__":
    play_game()
