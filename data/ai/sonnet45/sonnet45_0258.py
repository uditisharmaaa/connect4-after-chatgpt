import random
import os

# Constants for board dimensions and number of players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    """
    board = []
    for row in range(NUM_ROWS):
        board.append([" "] * NUM_COLS)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print the board with borders
    for row in range(NUM_ROWS):
        print("  " + "+---" * NUM_COLS + "+")
        print("  ", end="")
        for col in range(NUM_COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    print("  " + "+---" * NUM_COLS + "+")


def get_column_input(player_checker):
    """
    Gets and validates column input from the player.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Check if column is within board range
        if col_index < 0 or col_index >= NUM_COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + NUM_COLS)}.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    # Column is full
    return False


def check_win(board, checker):
    """
    Checks if the specified checker has won the game.
    Returns True if there are 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if all cells are filled.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = create_board()
    
    # Get player checkers based on number of players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get valid column input
        col_index = get_column_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col_index, current_checker):
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
