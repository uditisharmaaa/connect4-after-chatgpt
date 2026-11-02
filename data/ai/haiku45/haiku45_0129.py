import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return a 2D board initialized with empty spaces"""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * COLS + "+")

def get_column_input(current_player):
    """Get and validate column input from the current player"""
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Check if input is a single letter
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful, False if column is full"""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Please try another column.")
    return False

def check_win(board, checker):
    """Check if the given checker has won. Return True if won, False otherwise"""
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

def check_draw(board):
    """Check if the board is full (draw). Return True if full, False otherwise"""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def get_next_player(current_player_index):
    """Return the index of the next player"""
    return (current_player_index + 1) % NUM_PLAYERS

def main():
    """Main game loop"""
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = CHECKERS[current_player_index]
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get valid column input from current player
        valid_move = False
        while not valid_move:
            col = get_column_input(current_player)
            valid_move = place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check if the board is full (draw)
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player_index = get_next_player(current_player_index)
            current_player = CHECKERS[current_player_index]

if __name__ == "__main__":
    main()
