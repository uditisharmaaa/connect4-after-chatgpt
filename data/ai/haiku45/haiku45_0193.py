import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """Create and return a board with all empty spaces."""
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLS):
            board_row.append(" ")
        board.append(board_row)
    return board

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Top border
        print("+---" * COLS + "+")
        # Row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+---" * COLS + "+")

def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
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
        if col < 0 or col >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place a checker in the specified column. Returns True if successful, False if column is full."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False

def check_win(board, checker):
    """Check if the specified checker has won. Returns True if won, False otherwise."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def get_player_checkers(num_players):
    """Return the list of checkers for the given number of players."""
    return CHECKERS[:num_players]

def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get checkers for the players
    player_checkers = get_player_checkers(NUM_PLAYERS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    game_won = False
    while not game_won:
        current_checker = player_checkers[current_player_index]
        current_player_num = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        col = get_valid_column()
        
        # Try to place the checker
        if place_checker(board, col, current_checker):
            # Print the updated board
            print_board(board)
            
            # Check if current player won
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_won = True
            # Check if board is full (draw)
            elif is_board_full(board):
                print("It's a draw!")
                game_won = True
            # Move to next player
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column is full, player loses turn
            print("Column is full. You lose your turn.")
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
