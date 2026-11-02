import random
import os

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return an empty board with all spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLUMNS)])
    return board

def print_board(board):
    """Print the board in a formatted way."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLUMNS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
        
        # Print row border
        print("+", end="")
        for col in range(COLUMNS):
            print("---+", end="")
        print()

def get_valid_input(board, player_checker):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLUMNS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col] != " ":
            print("That column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def get_player_checkers(num_players):
    """Return the checkers for the given number of players."""
    return CHECKERS[:num_players]

def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Get player checkers
    player_checkers = get_player_checkers(NUM_PLAYERS)
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = player_checkers[current_player_index]
        
        # Get valid input from player
        col = get_valid_input(board, current_checker)
        
        # Place checker
        place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
