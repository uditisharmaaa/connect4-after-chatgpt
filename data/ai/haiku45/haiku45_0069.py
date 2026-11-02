import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def get_valid_column(player_checker):
    """Get a valid column input from the player."""
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if col_input < 'A' or col_input >= chr(65 + COLS):
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}.")
            continue
        
        col = ord(col_input) - 65
        return col

def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won."""
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
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Starting player: {checkers[current_player]}\n")
    
    while True:
        col = get_valid_column(checkers[current_player])
        
        if not place_checker(board, col, checkers[current_player]):
            print("Column is full. You lose your turn.\n")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        print_board(board)
        
        if check_win(board, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            return
        
        if is_board_full(board):
            print("Game is a draw!")
            return
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
