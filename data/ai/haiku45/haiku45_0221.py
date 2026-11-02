import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create a board with all empty cells."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * COLS + "+")

def is_valid_column(col_char, board):
    """Check if the column input is valid and not full."""
    if not col_char.isalpha() or len(col_char) != 1:
        return False
    
    col = ord(col_char.upper()) - 65
    
    if col < 0 or col >= COLS:
        return False
    
    return board[0][col] == " "

def place_checker(col_char, player_checker, board):
    """Place a checker in the specified column."""
    col = ord(col_char.upper()) - 65
    
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    return False

def check_win(board, player_checker):
    """Check if the current player has won."""
    
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
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player]
        player_num = current_player + 1
        
        # Get valid input from player
        while True:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip()
            if is_valid_column(col_input, board):
                break
            print("Invalid input. Please enter a valid column letter.")
        
        # Place checker
        place_checker(col_input, player_checker, board)
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
