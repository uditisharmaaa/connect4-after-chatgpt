import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """Create and return an empty board."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        
        # Print border between rows
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()

def get_player_input(player_checker):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col

def place_checker(board, col, player_checker):
    """Place a checker in the specified column. Return True if successful, False otherwise."""
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False

def check_win(board, player_checker):
    """Check if the player has won. Return True if won, False otherwise."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full. Return True if full, False otherwise."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    # Game loop
    while True:
        player_checker = CHECKERS[current_player_index]
        
        # Get valid input and place checker
        while True:
            col = get_player_input(player_checker)
            if place_checker(board, col, player_checker):
                break
        
        print_board(board)
        
        # Check if current player won
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check if board is full (draw)
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
