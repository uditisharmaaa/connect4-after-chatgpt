import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows with separators
    for row in board:
        print("+---+---+---+---+---+---+---+"[:COLS*4 + 1])
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    
    # Print the bottom border
    print("+---+---+---+---+---+---+---+"[:COLS*4 + 1])

def get_valid_move(board, current_player):
    """Prompt the player for a move and validate the input."""
    while True:
        move = input(f"Player {current_player}, please enter a column: ").upper()
        
        # Check if input is a single uppercase letter
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-" + chr(65 + COLS - 1) + ").")
            continue
        
        # Convert letter to column index
        col = ord(move) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full. Choose another column.")
            continue
        
        return col

def drop_checker(board, col, checker):
    """Drop the checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS_CHECKERS)
    print_board(board)
    
    while True:
        col = get_valid_move(board, current_player)
        drop_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch players
        next_player_idx = (PLAYERS_CHECKERS.index(current_player) + 1) % NUM_PLAYERS
        current_player = PLAYERS_CHECKERS[next_player_idx]

if __name__ == "__main__":
    play_game()
